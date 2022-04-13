import numpy as np
import cv2

im = cv2.imread('trees/train/images/00583.jpgfliplr.rf.a975c2c255fea433bd4e1027e20501cc.jpg')
h,_,_ = im.shape

f = open('trees/train/labels/00583.jpgfliplr.rf.a975c2c255fea433bd4e1027e20501cc.txt', 'r', encoding='UTF-8')
data = f.readlines()
l = []
for li in data:
    l.append(li.split(' '))

for li in l:
    a = float(li[1])
    b = float(li[2])
    c = float(li[3])
    d = float(li[4])
    print(a,b,c,d)
    x = int((a - (c/2)) * h)
    y = int((b - (d/2)) * h)
    z = int((a + (c/2)) * h)
    w = int((b + (d/2)) * h)
    print(x,y,z,w)
    #cv2.circle(im, (int(li[1].split('.')[0]), int(li[2].split('.')[0])), min(int(li[3].split('.')[0]), int(li[4].split('.')[0])), (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)
    cv2.rectangle(im, (x,y), (z,w), (255, 255, 0))

cv2.imwrite('./test.jpg', im)

