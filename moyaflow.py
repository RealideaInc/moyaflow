import glob
import cv2
import random
import json
from Class import arg_class, dir_class, image_class, DataArgmantation_class, txt_class
#import class
ArgClass = arg_class.arg_class()
DirClass = dir_class.dir_class()
ImgClass = image_class.image_class()
DaClass= DataArgmantation_class.DataArgmantation_class()
txtClass = txt_class.txt_class()

args = ArgClass.get_args()
IMAGE_SIZE = args.size
INPUT_JSON = args.INPUT_JSON
INPUT_IMAGE = args.INPUT_IMAGE
DATA_ARGMENT = args.DataArgment
BASE_OUTPUT_PATH = args.path

train_rate = 7
test_rate = 2
vaild_rate = 1

def class_count(json_list):
    classes = set()
    for i in range(len(json_list)):
        file = open(json_list[i] , 'r')
        jsonfile = json.load(file)
        for reg in jsonfile['regions']:
            classes.add(reg['tags'][0])
        class_cnt = len(classes)
        classes = list(classes)
        lst0_classcnt = list(range(class_cnt))
        class_dict = dict(zip(classes, lst0_classcnt))

        print("Number of detected classes：", class_cnt)
        print("Class type：", class_dict)
        print('\n')
        
        return classes, class_dict, class_cnt

def make_tree(json_list, kind, class_dict, num1,num2=0):
    for i in range(num2,num1):
        name, id = txtClass.make_points_file(json_list[i], kind,class_dict, IMAGE_SIZE, BASE_OUTPUT_PATH)
        im = cv2.imread(INPUT_IMAGE + '/' + name)
        im_new = ImgClass.resize_image(im, (0, 0, 0), IMAGE_SIZE)
        cv2.imwrite(BASE_OUTPUT_PATH + '/' + kind + '/images/' + name + '.rf.' + id + '.jpg', im_new)
        if DATA_ARGMENT is not None:
            if not {'salt', 'sal', 'sa'}.isdisjoint(set(DATA_ARGMENT)):
                txtClass.make_points_file(json_list[i], kind, class_dict,IMAGE_SIZE,BASE_OUTPUT_PATH, name + 'salt')
                salt_im = DaClass.Salt_noise(INPUT_IMAGE + '/' + name)
                salt_new_im = ImgClass.resize_image(salt_im, (0, 0, 0), IMAGE_SIZE)
                cv2.imwrite(BASE_OUTPUT_PATH + '/' + kind + '/images/' + name + 'salt.rf.' + id + '.jpg', salt_new_im)

            if not {'pepper', 'peppe', 'pepp', 'pep', 'pe'}.isdisjoint(set(DATA_ARGMENT)):
                txtClass.make_points_file(json_list[i], kind, class_dict, IMAGE_SIZE,BASE_OUTPUT_PATH, name + 'pepper')
                pep_im = DaClass.Pepper_noise(INPUT_IMAGE + '/' + name)
                pep_new_im = ImgClass.resize_image(pep_im, (0, 0, 0), IMAGE_SIZE)
                cv2.imwrite(BASE_OUTPUT_PATH + '/' + kind + '/images/' + name + 'pepper.rf.' + id + '.jpg', pep_new_im)

            if not {'smooth', 'smoot', 'smoo', 'smo', 'sm'}.isdisjoint(set(DATA_ARGMENT)):
                txtClass.make_points_file(json_list[i], kind, class_dict, IMAGE_SIZE,BASE_OUTPUT_PATH, name + 'smooth')
                smooth_im = DaClass.Smooth_noise(INPUT_IMAGE + '/' + name)
                smooth_new_im = ImgClass.resize_image(smooth_im, (0, 0, 0), IMAGE_SIZE)
                cv2.imwrite(BASE_OUTPUT_PATH + '/' + kind + '/images/' + name + 'smooth.rf.' + id + '.jpg', smooth_new_im)

            if not {'fliplr', 'flipl', 'flip', 'fli', 'fl'}.isdisjoint(set(DATA_ARGMENT)):
                txtClass.make_points_file(json_list[i], kind, class_dict, IMAGE_SIZE,BASE_OUTPUT_PATH, name + 'fliplr', 'fliplr')
                flip_im = DaClass.flip_lr(INPUT_IMAGE + '/' + name)
                flip_new_im = ImgClass.resize_image(flip_im, (0, 0, 0), IMAGE_SIZE)
                cv2.imwrite(BASE_OUTPUT_PATH + '/' + kind + '/images/' + name + 'fliplr.rf.' + id + '.jpg', flip_new_im)

def main():

    input_ok, waring_str = ArgClass.check_INPUT(INPUT_JSON)
    if not input_ok:
        print(waring_str)
        return

    input_ok, waring_str = ArgClass.check_INPUT(INPUT_IMAGE)
    if not input_ok:
        print(waring_str)
        return

    DirClass.make_tree_dir(BASE_OUTPUT_PATH)

    json_list = glob.glob(INPUT_JSON + '/*.json')
    image_list = glob.glob(INPUT_IMAGE + '/*.jpg')

    jsonnum = len(json_list)
    trainnum = (jsonnum * train_rate) // 10
    testnum = (jsonnum * test_rate) // 10

    classes, class_dict, class_cnt = class_count(json_list)

    txtClass.make_yaml(BASE_OUTPUT_PATH, classes, class_cnt)

    image_list.sort()
    random.shuffle(json_list)
    make_tree(json_list, 'train', class_dict, trainnum)
    make_tree(json_list, 'test',class_dict, trainnum+testnum, trainnum)
    make_tree(json_list, 'valid',class_dict, jsonnum, trainnum+testnum)


if __name__ == '__main__':
    main()
