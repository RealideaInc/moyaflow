import os
import json
import glob
import argparse
import numpy as np
import random, string
from PIL import Image

BASE_OUTPUT_PATH = "./trees"
train_rate = 7
test_rate = 2
vaild_rate = 1

def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

class arg_class:
    def get_args(self):
        parser = argparse.ArgumentParser(description="Convert json file created by VoTT to yolov5 format.")
        parser.add_argument('INPUT_JSON', help="Please set the json directory.")
        parser.add_argument('INPUT_IMAGE', help="Please set the image directory.")
        parser.add_argument('-s', '--size', help='Option when you want to set image size.', type=int, default=640)
        args = parser.parse_args()

        return(args)

    def check_INPUT(self, INP):
        if not os.path.isdir(INP):
            return False, '【 Error 】directory({}) does not exist.'.format(INP)
        return True, ''

class dir_class:

    def make_dir(self, PATH):
        if not os.path.exists(PATH):
            print('【 Notice 】Create an {} directory.'.format(PATH))
            os.makedirs(PATH)

    def make_tree_dir(self):
        self.make_dir(BASE_OUTPUT_PATH + '/test/images')
        self.make_dir(BASE_OUTPUT_PATH + '/test/labels')
        self.make_dir(BASE_OUTPUT_PATH + '/train/images')
        self.make_dir(BASE_OUTPUT_PATH + '/train/labels')
        self.make_dir(BASE_OUTPUT_PATH + '/valid/images')
        self.make_dir(BASE_OUTPUT_PATH + '/valid/labels')

def make_yaml():
    YAML_PATH = 'train: {}/train/images\nval: {}/valid/images\nnc: 1\nnames: [\'Tree\']'.format(BASE_OUTPUT_PATH, BASE_OUTPUT_PATH)
    with open(BASE_OUTPUT_PATH + '/data.yaml', mode='w') as f:
        f.write(YAML_PATH)

class image_class:

    def expand2square(self, pil_img, background_color):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result
    
    def resize_image(self, img, c, rsize):
        return self.expand2square(img, c).resize((rsize, rsize))
  

def make_points_file(jsondata, TTVPATH, rsize):
    if TTVPATH == 'train': OUTPUT_PATH = BASE_OUTPUT_PATH + '/train/labels'
    elif TTVPATH == 'test': OUTPUT_PATH = BASE_OUTPUT_PATH + '/test/labels'
    elif TTVPATH == 'valid': OUTPUT_PATH = BASE_OUTPUT_PATH + '/valid/labels'
    else:
        print('【error】') 
        return
    ArgClass = arg_class()
    DirClass = dir_class()
    
    DirClass.make_dir(OUTPUT_PATH)

    first = True
    file = open(jsondata , 'r')
    jsonfile = json.load(file)
    name = jsonfile['asset']['name']
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

            f.write('0 {} {} {} {}\n'.format(xm/rsize, ym/rsize, width/rsize, height/rsize))
    print('【 Success 】Create {}'.format(OUTPUT_PATH + '/' + name + '.rf.' + id + '.txt'))
    return name, id

def main():
    ArgClass = arg_class()
    DirClass = dir_class()
    ImgClass = image_class()
    args = ArgClass.get_args()
    image_size = args.size

    INPUT_JSON = args.INPUT_JSON
    INPUT_IMAGE = args.INPUT_IMAGE

    input_ok, waring_str = ArgClass.check_INPUT(INPUT_JSON)
    if not input_ok:
        print(waring_str)
        return 

    input_ok, waring_str = ArgClass.check_INPUT(INPUT_IMAGE)
    if not input_ok:
        print(waring_str)
        return 

    DirClass.make_tree_dir()
    make_yaml()

    json_list = glob.glob(INPUT_JSON + '/*.json')
    image_list = glob.glob(INPUT_IMAGE + '/*.jpg')
    jsonnum = len(json_list)
    trainnum = (jsonnum * train_rate) // 10
    testnum = (jsonnum * test_rate) // 10

    image_list.sort()
    random.shuffle(json_list)
    for i in range(trainnum):
        name, id = make_points_file(json_list[i], 'train', image_size)
        im = Image.open(INPUT_IMAGE + '/' + name)
        im_new = ImgClass.resize_image(im, (0, 0, 0), image_size)
        im_new.save(BASE_OUTPUT_PATH + '/train/images/' + name + '.rf.' + id + '.jpg', quality=95)
    for i in range(trainnum, trainnum + testnum):
        name, id = make_points_file(json_list[i], 'test',image_size)
        im = Image.open(INPUT_IMAGE + '/' + name)
        im_new = ImgClass.resize_image(im, (0, 0, 0), image_size)
        im_new.save(BASE_OUTPUT_PATH + '/test/images/' + name + '.rf.' + id + '.jpg', quality=95)
    for i in range(trainnum + testnum, jsonnum):
        name, id = make_points_file(json_list[i], 'valid', image_size)
        im = Image.open(INPUT_IMAGE + '/' + name)
        im_new = ImgClass.resize_image(im, (0, 0, 0), image_size)
        im_new.save(BASE_OUTPUT_PATH + '/valid/images/' + name + '.rf.' + id + '.jpg', quality=95)

if __name__ == '__main__':
    main()
