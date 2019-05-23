#!/usr/bin/env python
# coding: utf-8

# In[9]:


from skimage.measure import compare_ssim
import cv2
import random
import numpy as np
import math
import PIL.Image as Image
import os
import imutils
from matplotlib import pyplot as plt





img = cv2.imread("C:\\Users\\TF\\Desktop\\images\\1.jpg", 1)
sample = cv2.imread("C:\\Users\\TF\\Desktop\\images\\mask.jpg", 1)
h, w, _ = img.shape 
dim = (512, 512)
img = cv2.resize(img, dim)
kernel1 = np.ones((5,5),np.uint8) 
kernel2 = np.ones((2,2),np.uint8) 

h, w, _ = img.shape 
mask = np.zeros([h+2, w+2], np.uint8)
image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sample = cv2.cvtColor(sample,cv2.COLOR_BGR2GRAY)
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


'''
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt=contours[max_index]
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(Mask,(x,y),(x+w,y+h),(0,255,0),2)
'''
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
    #trans_img = cv2.transpose( Rotated )
    #Rotated = cv2.flip(trans_img, 1)
#print(cY)
#print(cX)
#erosion = cv2.erode(Rotated,kernel2,iterations = 10)
#Rotated = cv2.subtract(Rotated,erosion)
'''Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = min(Xs)
x2 = max(Xs)
y1 = min(Ys)
y2 = max(Ys)
hight = y2 - y1
width = x2 - x1
cropImg = Mask[y1:y1+hight, x1:x1+width]

background= np.ones((512,512),np.uint8) 
#sample = imutils.rotate(sample, -90)
rows1, cols1 = sample.shape[:2] #获取bear的高度、宽度
roi = background[0:rows1, 0:cols1]

dst = cv2.addWeighted(sample,1,roi,0,0) #图像融合
add_img1 = background.copy() #对原图像进行拷贝
add_img1[(255-rows1//2):math.ceil(255+rows1/2), (255-cols1//2):math.ceil(255+cols1/2)] = dst  # 将融合后的区域放进原图



rows2, cols2 = Rotated.shape[:2] #获取bear的高度、宽度
roi = background[0:rows2, 0:cols2]
print(rows2)
dst = cv2.addWeighted(Rotated,1,roi,0,0) #图像融合
add_img2 = background.copy() #对原图像进行拷贝
add_img2[(255-rows2//2):math.ceil(255+rows2/2), (255-cols2//2):math.ceil(255+cols2/2)] = dst  # 将融合后的区域放进原图
'''
#(score, diff) = compare_ssim(add_img1, add_img2, full=True)
#similarity = score
#print(similarity)
Mask1 = np.ones(Rotated.shape,np.uint8)
Mask2 = np.ones(sample.shape,np.uint8)

_ , binary1 = cv2.threshold(Rotated,127,255,cv2.THRESH_BINARY)
(cnt, _) = cv2.findContours(binary1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(Mask1, cnt, 0, 255, -1)

_, binary2 = cv2.threshold(sample,127,255,cv2.THRESH_BINARY)
(cnts, _) = cv2.findContours(binary2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(Mask2, cnts, 0, 255, -1)



ret = cv2.matchShapes(contours[idx], cnts[0], 1, 0.0)

#for c in idx:
    #cv2.polylines(Mask, [c], 1, 255)
    #cv2.line(Mask, [c], [c]+1, (255,255,255))
    #cv2.drawContours(Mask, [c], -1, (255,255,255), -1) 


#print(height)
#print(weight)
print(ret)
#cv2.imshow('2',sample)
#cv2.imshow('1',Rotated)
#cv2.imshow('canny',Mask1)
#cv2.imshow('Mask',Mask2)



cv2.waitKey()


# In[ ]:





# In[ ]:




