import os
import json
import glob
import argparse
import numpy as np
import cv2
import random, string
from PIL import Image
from .. import moyaflow as mf
from . import dir_class

class txt_class():

    def make_yaml(self):
        YAML_PATH = 'train: {}/train/images\nval: {}/valid/images\nnc: 1\nnames: [\'Tree\']'.format(mf.BASE_OUTPUT_PATH, mf.BASE_OUTPUT_PATH)
        with open(mf.BASE_OUTPUT_PATH + '/data.yaml', mode='w') as f:
            f.write(YAML_PATH)

    def make_points_file(self,jsondata, TTVPATH, rsize, name='', options=''):
        if TTVPATH == 'train': OUTPUT_PATH = mf.BASE_OUTPUT_PATH + '/train/labels'
        elif TTVPATH == 'test': OUTPUT_PATH = mf.BASE_OUTPUT_PATH + '/test/labels'
        elif TTVPATH == 'valid': OUTPUT_PATH = mf.BASE_OUTPUT_PATH + '/valid/labels'
        else:
            print('【error】') 
            return
        DirClass = dir_class()

        DirClass.make_dir(OUTPUT_PATH)

        first = True
        file = open(jsondata , 'r')
        jsonfile = json.load(file)
        if name == '': name = jsonfile['asset']['name']
        id = jsonfile['asset']['id']
        img_width = jsonfile['asset']['size']['width']
        img_height = jsonfile['asset']['size']['height']
        for reg in jsonfile['regions']:
            mode = 'a'
            if first:
                mode = 'w'
                first = False

            points = reg['points']
            # x2 > x1, y2 > y1
            x2 = max(points[0]['x'], points[1]['x'])
            x1 = min(points[0]['x'], points[1]['x'])
            y2 = max(points[0]['y'], points[2]['y'])
            y1 = min(points[0]['y'], points[2]['y'])

            width = x2 - x1
            height = y2 - y1
            xm, ym = x1 + (width / 2), y1 + (height / 2)

            with open(OUTPUT_PATH + '/' + name + '.rf.' + id + '.txt', mode=mode) as f:
                # [oject-class] [x_center] [y_center] [width] [height]
                if img_width > img_height:
                    ym = ym + (img_width - img_height)/2
                    ym = ym * (rsize/img_width)
                    xm = xm * (rsize/img_width)
                    width = width * (rsize/img_width)
                    height = height * (rsize/img_width)
                elif img_width <= img_height:
                    xm = xm + (img_height - img_width)/2 
                    ym = ym * (rsize/img_height)
                    xm = xm * (rsize/img_height)
                    width = width * (rsize/img_height)
                    height = height * (rsize/img_height)

                if options == '': f.write('0 {} {} {} {}\n'.format(xm/rsize, ym/rsize, width/rsize, height/rsize))
                elif options == 'fliplr': f.write('0 {} {} {} {}\n'.format((1-xm/rsize), ym/rsize, width/rsize, height/rsize))
        print('【 Success 】Create {}'.format(OUTPUT_PATH + '/' + name + '.rf.' + id + '.txt'))
        return name, id