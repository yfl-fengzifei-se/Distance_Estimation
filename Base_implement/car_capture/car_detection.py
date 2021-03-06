'''
 * Copyright 2017 Distance Measurement, EE, NCKU. All rights reserved. 
 * File : car_detection.py 
 * User : Syuan Jhao 
 * Date : 2017/3/16 
 * Version : 1.0
 * OS : Ubuntu Mate 16.04 LTS
 * Tools : Python 2.7 + Opencv 3.2.0
 * Introduction : Detect the vehicle by Haar-feature
 * Guide : python car_detection.py /path/to/cascadefile.xml /path/to/image
'''

import cv2
import numpy as np
import sys
from scipy.spatial import distance as dist

#focal length
focal_length = 818.0

#car's real width(cm)
car_width = 170.0

#car pic detection
#   Get User supplied values
cascPath  = sys.argv[1]
imgPath = sys.argv[2]

img = cv2.imread(imgPath)
car_cascade = cv2.CascadeClassifier(cascPath)
height, width = img.shape[:2]
print(height)
#faceCascade = cv2.CascadeClassifier(cascPath)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# create a mask
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:400] = 255
masked_img = cv2.bitwise_and(img,img,mask = mask)
# Calculate histogram with mask and without mask
# Check third argument for mask
hist_full = cv2.calcHist([img],[0],None,[256],[0,256])
hist_mask = cv2.calcHist([img],[0],mask,[256],[0,256])
cv2.imshow('mask', mask)
cv2.imshow('mask_img', masked_img)
cv2.imshow('hist', hist_mask)

cars = car_cascade.detectMultiScale(gray, 1.3, 1)
rows, cols = gray.shape
sobel_vertical = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize = 5)
canny = cv2.Canny(gray, 50, 240)
print("Founded {0} cars!".format(len(cars)))
for(x, y, w, h) in cars:
	cv2.rectangle(img, (x,y), (x+w,y+h), (0, 0, 255), 2)
	distance = (focal_length * car_width)/w
	print(distance, "cm")
cv2.imshow('car edge', sobel_vertical)
cv2.imshow('canny', canny)
cv2.imshow('car detection', img)
cv2.imwrite("cars_detection.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()