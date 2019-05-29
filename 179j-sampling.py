#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import numpy as np
import scipy.io as sio
import glob
from PIL import Image
import cv2
from skimage.measure import compare_ssim
import random
import math
import imutils
from matplotlib import pyplot as plt

path_to_dataset = 'C:\\Users\\TF\\Desktop\\data\\'

label = []
feature = []
categories = sorted(os.listdir(path_to_dataset))
for i,c in enumerate(categories):    
        path_to_images = sorted(glob.glob(os.path.join(path_to_dataset,c) + '/*.jpg'))
        for p in path_to_images:
          # FILL IN TO LOAD IMAGE, PREPROCESS, EXTRACT FEATURES.
            img = cv2.imread(p)
            #t_img = transform_test(img)
            h, w, _ = img.shape
            dim = (512, 512)
            img = cv2.resize(img, dim)
            kernel1 = np.ones((5,5),np.uint8) 
            kernel2 = np.ones((2,2),np.uint8) 

            h, w, _ = img.shape 
            mask = np.zeros([h+2, w+2], np.uint8)
            image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gau = cv2.GaussianBlur(image,(5,5),0)
            sobelX = cv2.Sobel(gau,cv2.CV_64F,1,0)#x方向的梯度
            sobelY = cv2.Sobel(gau,cv2.CV_64F,0,1)#y方向的梯度

            sobelX = np.uint8(np.absolute(sobelX))#x方向梯度的绝对值
            sobelY = np.uint8(np.absolute(sobelY))#y方向梯度的绝对值

            sobelCombined = cv2.bitwise_or(sobelX,sobelY)#


            canny = cv2.Canny(sobelCombined, 50, 150) 


            canny = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel1)


            (contours, _) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            areas = list()
            for i, cnt in enumerate(contours):
                areas.append((i, cv2.contourArea(cnt)))#面积大小

            #
            a2 = sorted(areas, key=lambda d: d[1], reverse=True)

            Mask = np.ones((512,512),np.uint8) 

            idx = a2[0][0]
            cv2.drawContours(Mask, contours, idx, 255, -1)

            rect = cv2.minAreaRect(contours[idx])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            #print(box)
            height = np.uint16(math.ceil(np.linalg.norm(box[0]-box[1])))
            weight = np.uint16(math.ceil(np.linalg.norm(box[0]-box[3])))

            Box = box.copy()

            Box[0] = box[1]
            Box[1] = box[2]
            Box[2] = box[3]
            Box[3] = box[0]


            four_points= np.array(((0, 0),
                                   (weight - 1, 0),
                                   (weight - 1,height - 1 ),
                                   (0, height - 1)),
                                np.float32)
            target_points = np.array(Box, np.float32)#统一格式
            M = cv2.getPerspectiveTransform(target_points, four_points)
            Rotated= cv2.warpPerspective(Mask, M, (weight,height))




            #test = np.ones((512,512),np.uint8) 
            #test = cv2.drawContours(test, cnt,1, 255, -1)
            m = cv2.moments(contours[idx])
            cX = int(m["m10"] / m["m00"])
            cY = int(m["m01"] / m["m00"])
            #cv2.circle(Rotated, (cX, cY), 20, (1, 227, 254), -1)


            #print(Rotated.shape[0])
            (h, w) = Rotated.shape 
            center = (w // 2, h // 2) 
            if (cX*2) < Rotated.shape[1]:
                row,col = Rotated.shape[:2]
            #第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
                m = cv2.getRotationMatrix2D((col/2,row/2),180,1)
            #第三个参数：变换后的图像大小
                Rotated = cv2.warpAffine(Rotated,m,(col,row))
                
            Mask1 = np.ones(Rotated.shape,np.uint8)

            _ , binary1 = cv2.threshold(Rotated,127,255,cv2.THRESH_BINARY)
            (cnt, _) = cv2.findContours(binary1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(Mask1, cnt, 0, 255, -1)
                   
        #label = inference(extractor, t_img)
            F = cnt[0]#extract_feature(extractor, t_img)
      # OUTPUT VARIABLE F EXPECTED TO BE THE FEATURE OF THE IMAGE OF DIMENSION (2048,)
            feature.append(F)
        #print(F.size)
            label.append(categories.index(c))   
sio.savemat('sample.mat', mdict={'feature': feature, 'label': label})


# In[ ]:




