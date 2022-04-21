import numpy as np
import cv2

color = [(255,255,0), (255,0,255), (0,255,255), (255,255,0), (0,0,255), (255,0,0),(0,255,0)]

im = cv2.imread('trees/test/images/snoopy00004.jpg.rf.d55ee07d43dad4c7cd9f3d3ccc3d4d1a.jpg')
h,_,_ = im.shape

f = open('trees/test/labels/snoopy00004.jpg.rf.d55ee07d43dad4c7cd9f3d3ccc3d4d1a.txt', 'r', encoding='UTF-8')
data = f.readlines()
l = []
for li in data:
    l.append(li.split(' '))

for li in l:
    clss = int(li[0])
    a = float(li[1])
    b = float(li[2])
    c = float(li[3])
    d = float(li[4])
    print(clss, a,b,c,d)
    x = int((a - (c/2)) * h)
    y = int((b - (d/2)) * h)
    z = int((a + (c/2)) * h)
    w = int((b + (d/2)) * h)
    print(x,y,z,w)
    #cv2.circle(im, (int(li[1].split('.')[0]), int(li[2].split('.')[0])), min(int(li[3].split('.')[0]), int(li[4].split('.')[0])), (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)
    cv2.rectangle(im, (x,y), (z,w), color[clss])

cv2.imwrite('./test.jpg', im)

