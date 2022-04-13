import os
import json
import glob
import argparse
import numpy as np
import cv2
import random, string
from PIL import Image

class image_class:

    def expand2square(self, cv2_img, background_color):
        width, height, _ = cv2_img.shape
        if width == height:
            return cv2_img
        elif width > height:
            result = np.zeros((width, width, 3))
            result += [background_color[0],background_color[1],background_color[2]][::-1]
            result[0:width, (width - height)//2:((width - height) // 2) + height] = cv2_img
            return result
        else:
            result = np.zeros((height, height, 3))
            result += [background_color[0],background_color[1],background_color[2]][::-1]
            result[(height - width) // 2:((height - width) // 2) + width, 0:height] = cv2_img
            return result
    
    def resize_image(self, img, c, rsize):
        # return self.expand2square(img, c).resize((rsize, rsize))
        return cv2.resize(self.expand2square(img, c), dsize=(rsize, rsize))