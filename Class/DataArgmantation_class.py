import os
import json
import glob
import argparse
import numpy as np
import cv2
import random, string
from PIL import Image

class DataArgmantation_class:

    def Salt_noise(self, path, amount=0.015):
        src = cv2.imread(path, 1)
        s_vs_p = 0.5
        sp_img = src.copy()
        num_salt = np.ceil(amount * src.size * s_vs_p)
        coords = [np.random.randint(0, i-1 , int(num_salt)) for i in src.shape]
        sp_img[tuple(coords[:-1])] = (255,255,255)
        return sp_img

    def Pepper_noise(self, path, amount=0.015):
        src = cv2.imread(path, 1)
        s_vs_p = 0.5
        sp_img = src.copy()
        num_pepper = np.ceil(amount* src.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i-1 , int(num_pepper)) for i in src.shape]
        sp_img[tuple(coords[:-1])] = (0,0,0)
        return sp_img

    def Smooth_noise(self, path):
        average_square = (10,10)
        src = cv2.imread(path, 1)
        blur_img = cv2.blur(src, average_square)
        return blur_img

    def flip_lr(self, path):
        src = cv2.imread(path, 1)
        flip_lr_img = cv2.flip(src, 1)
        return flip_lr_img
