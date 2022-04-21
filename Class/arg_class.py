import os
import argparse

class arg_class:
    def get_args(self):
        tp = lambda x:list(map(int, x.split(',')))
        parser = argparse.ArgumentParser(description="Convert json file created by VoTT to yolov5 format.")
        parser.add_argument('INPUT_JSON', help="Please set the json directory.")
        parser.add_argument('INPUT_IMAGE', help="Please set the image directory.")
        parser.add_argument('-r', '--rate',
         help='This is an option for the usage rate of train, test, and valid data. Specify it so that it is separated by \',\' and added up to 10. The default is [train, test, valid] = [7,2,1].',
         type=tp, default=[7,2,1])
        parser.add_argument('-s', '--size', help='Option when you want to set image size.', type=int, default=640)
        parser.add_argument('-p', '--path', help='You can specify where the test, train, valid directories will be created. The default is\'./yolov5_anotation_data\'',default='./yolov5_anotation_data')
        parser.add_argument('-d', '--DataArgment',
            help='Option when you want to "Data Argmentation". The types are now salt noise, pepper noise, smoothing noise, fliplr. For example, if you want to use salt noise and smooth noise, use "-d salt smooth". (It\'s okay to shorten it like "-d sa sm")', nargs='*')
        args = parser.parse_args()

        return(args)

    def check_INPUT(self, INP):
        if not os.path.isdir(INP):
            return False, '【 Error 】directory({}) does not exist.'.format(INP)
        return True, ''