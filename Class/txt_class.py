import json
import sys

from torch import classes
from Class import dir_class

class txt_class():

    def make_yaml(self, BASE_OUTPUT_PATH, classes, class_cnt):

        YAML_PATH = 'train: {}/train/images\nval: {}/valid/images\nnc: {}\nnames: {}'.format(BASE_OUTPUT_PATH, BASE_OUTPUT_PATH, class_cnt, classes)
        with open(BASE_OUTPUT_PATH + '/data.yaml', mode='w') as f:
            f.write(YAML_PATH)

    def make_points_file(self, jsondata, kind, class_dict, rsize, BASE_OUTPUT_PATH, name='', options=''):
        OUTPUT_PATH = BASE_OUTPUT_PATH + '/' + kind + '/labels'

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
            reg_class = reg['tags'][0]
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

                if options == '': f.write('{} {} {} {} {}\n'.format(class_dict[reg_class], xm/rsize, ym/rsize, width/rsize, height/rsize))
                elif options == 'fliplr': f.write('{} {} {} {} {}\n'.format(class_dict[reg_class], (1-xm/rsize), ym/rsize, width/rsize, height/rsize))
        print('【 Success 】Create {}'.format(OUTPUT_PATH + '/' + name + '.rf.' + id + '.txt'))
        return name, id