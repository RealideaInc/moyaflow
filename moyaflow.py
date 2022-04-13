import os
import json
import glob
import argparse
import numpy as np
import cv2
import random, string
from PIL import Image
from Class import arg_class, dir_class, image_class, DataArgmantation_class, txt_class
BASE_OUTPUT_PATH = "./trees"
train_rate = 7
test_rate = 2
vaild_rate = 1

def main():
    ArgClass = arg_class()
    DirClass = dir_class()
    ImgClass = image_class()
    DaClass= DataArgmantation_class()
    txtClass = txt_class()
    args = ArgClass.get_args()
    image_size = args.size
    INPUT_JSON = args.INPUT_JSON
    INPUT_IMAGE = args.INPUT_IMAGE
    data_argment = args.DataArgment
    print(data_argment)
    input_ok, waring_str = ArgClass.check_INPUT(INPUT_JSON)
    if not input_ok:
        print(waring_str)
        return

    input_ok, waring_str = ArgClass.check_INPUT(INPUT_IMAGE)
    if not input_ok:
        print(waring_str)
        return

    DirClass.make_tree_dir()
    txtClass.make_yaml()

    json_list = glob.glob(INPUT_JSON + '/*.json')
    image_list = glob.glob(INPUT_IMAGE + '/*.jpg')
    jsonnum = len(json_list)
    trainnum = (jsonnum * train_rate) // 10
    testnum = (jsonnum * test_rate) // 10

    image_list.sort()
    random.shuffle(json_list)
    for i in range(trainnum):
        name, id = txtClass.make_points_file(json_list[i], 'train', image_size)
        im = cv2.imread(INPUT_IMAGE + '/' + name)
        im_new = ImgClass.resize_image(im, (0, 0, 0), image_size)
        cv2.imwrite(BASE_OUTPUT_PATH + '/train/images/' + name + '.rf.' + id + '.jpg', im_new)
        if data_argment is not None:
            if not {'salt', 'sal', 'sa'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'train', image_size, name + 'salt')
                salt_im = DaClass.Salt_noise(INPUT_IMAGE + '/' + name)
                salt_new_im = ImgClass.resize_image(salt_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/train/images/' + name + 'salt.rf.' + id + '.jpg', salt_new_im)

            if not {'pepper', 'peppe', 'pepp', 'pep', 'pe'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'train', image_size, name + 'pepper')
                pep_im = DaClass.Pepper_noise(INPUT_IMAGE + '/' + name)
                pep_new_im = ImgClass.resize_image(pep_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/train/images/' + name + 'pepper.rf.' + id + '.jpg', pep_new_im)

            if not {'smooth', 'smoot', 'smoo', 'smo', 'sm'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'train', image_size, name + 'smooth')
                smooth_im = DaClass.Smooth_noise(INPUT_IMAGE + '/' + name)
                smooth_new_im = ImgClass.resize_image(smooth_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/train/images/' + name + 'smooth.rf.' + id + '.jpg', smooth_new_im)

            if not {'fliplr', 'flipl', 'flip', 'fli', 'fl'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'train', image_size, name + 'fliplr', 'fliplr')
                flip_im = DaClass.flip_lr(INPUT_IMAGE + '/' + name)
                flip_new_im = ImgClass.resize_image(flip_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/train/images/' + name + 'fliplr.rf.' + id + '.jpg', flip_new_im)


    for i in range(trainnum, trainnum + testnum):
        name, id = txtClass.make_points_file(json_list[i], 'test',image_size)
        im = cv2.imread(INPUT_IMAGE + '/' + name)
        im_new = ImgClass.resize_image(im, (0, 0, 0), image_size)
        cv2.imwrite(BASE_OUTPUT_PATH + '/test/images/' + name + '.rf.' + id + '.jpg', im_new)
        if data_argment is not None:
            if not {'salt', 'sal', 'sa'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'test', image_size, name + 'salt')
                salt_im = DaClass.Salt_noise(INPUT_IMAGE + '/' + name)
                salt_new_im = ImgClass.resize_image(salt_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/test/images/' + name + 'salt.rf.' + id + '.jpg', salt_new_im)

            if not {'pepper', 'peppe', 'pepp', 'pep', 'pe'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'test', image_size, name + 'pepper')
                pep_im = DaClass.Pepper_noise(INPUT_IMAGE + '/' + name)
                pep_new_im = ImgClass.resize_image(pep_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/test/images/' + name + 'pepper.rf.' + id + '.jpg', pep_new_im)

            if not {'smooth', 'smoot', 'smoo', 'smo', 'sm'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'test', image_size, name + 'smooth')
                smooth_im = DaClass.Smooth_noise(INPUT_IMAGE + '/' + name)
                smooth_new_im = ImgClass.resize_image(smooth_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/test/images/' + name + 'smooth.rf.' + id + '.jpg', smooth_new_im)

            if not {'fliplr', 'flipl', 'flip', 'fli', 'fl'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'test', image_size, name + 'fliplr','fliplr')
                flip_im = DaClass.flip_lr(INPUT_IMAGE + '/' + name)
                flip_new_im = ImgClass.resize_image(flip_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/test/images/' + name + 'fliplr.rf.' + id + '.jpg', flip_new_im)


    for i in range(trainnum + testnum, jsonnum):
        name, id = txtClass.make_points_file(json_list[i], 'valid', image_size)
        im = cv2.imread(INPUT_IMAGE + '/' + name)
        im_new = ImgClass.resize_image(im, (0, 0, 0), image_size)
        cv2.imwrite(BASE_OUTPUT_PATH + '/valid/images/' + name + '.rf.' + id + '.jpg', im_new)
        if data_argment is not None:
            if not {'salt', 'sal', 'sa'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'valid', image_size, name + 'salt')
                salt_im = DaClass.Salt_noise(INPUT_IMAGE + '/' + name)
                salt_new_im = ImgClass.resize_image(salt_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/valid/images/' + name + 'salt.rf.' + id + '.jpg', salt_new_im)

            if not {'pepper', 'peppe', 'pepp', 'pep', 'pe'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'valid', image_size, name + 'pepper')
                pep_im = DaClass.Pepper_noise(INPUT_IMAGE + '/' + name)
                pep_new_im = ImgClass.resize_image(pep_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/valid/images/' + name + 'pepper.rf.' + id + '.jpg', pep_new_im)

            if not {'smooth', 'smoot', 'smoo', 'smo', 'sm'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'valid', image_size, name + 'smooth')
                smooth_im = DaClass.Smooth_noise(INPUT_IMAGE + '/' + name)
                smooth_new_im = ImgClass.resize_image(smooth_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/valid/images/' + name + 'smooth.rf.' + id + '.jpg', smooth_new_im)

            if not {'fliplr', 'flipl', 'flip', 'fli', 'fl'}.isdisjoint(set(data_argment)):
                txtClass.make_points_file(json_list[i], 'valid', image_size, name + 'fliplr','fliplr')
                flip_im = DaClass.flip_lr(INPUT_IMAGE + '/' + name)
                flip_new_im = ImgClass.resize_image(flip_im, (0, 0, 0), image_size)
                cv2.imwrite(BASE_OUTPUT_PATH + '/vaild/images/' + name + 'fliplr.rf.' + id + '.jpg', flip_new_im)


if __name__ == '__main__':
    main()
