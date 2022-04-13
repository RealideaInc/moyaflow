import os
import argparse

class arg_class:
    def get_args(self):
        parser = argparse.ArgumentParser(description="Convert json file created by VoTT to yolov5 format.")
        parser.add_argument('INPUT_JSON', help="Please set the json directory.")
        parser.add_argument('INPUT_IMAGE', help="Please set the image directory.")
        parser.add_argument('-s', '--size', help='Option when you want to set image size.', type=int, default=640)
        parser.add_argument('-d', '--DataArgment', 
            help='Option when you want to "Data Argmentation". The types are now salt noise, pepper noise, smoothing noise, fliplr. For example, if you want to use salt noise and smooth noise, use "-d salt smooth". (It\'s okay to shorten it like "-d sa sm")', nargs='*')
        args = parser.parse_args()

        return(args)

    def check_INPUT(self, INP):
        if not os.path.isdir(INP):
            return False, '【 Error 】directory({}) does not exist.'.format(INP)
        return True, ''