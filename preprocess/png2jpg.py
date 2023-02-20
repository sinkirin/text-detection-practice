#!/usr/bin/env python
from glob import glob
import cv2
pngs = glob('/SVHN/VOC2007/test/*.png')

for j in pngs:
    img = cv2.imread(j)
    cv2.imwrite(j[:-3] + 'jpg', img)
