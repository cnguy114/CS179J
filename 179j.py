#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import cv2
import random
import numpy as np
import matplotlib.pyplot as plt
import collections

def getColorList():
    dict = collections.defaultdict(list)
 
    # 黑色
    #lower_black = np.array([0, 0, 0])
    #upper_black = np.array([180, 255, 46])
    #color_list = []
    #color_list.append(lower_black)
    #color_list.append(upper_black)
    #dict['black'] = color_list
 
    #灰色
    lower_gray = np.array([0, 0, 46])
    upper_gray = np.array([180, 43, 220])
    color_list = []
    color_list.append(lower_gray)
    color_list.append(upper_gray)
    dict['gray']=color_list
 
    # 白色
    lower_white = np.array([0, 0, 221])
    upper_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['white'] = color_list
 
    #红色
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red']=color_list
 
    # 红色2
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red2'] = color_list
 
    #橙色
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    dict['orange'] = color_list
 
    #黄色
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['yellow'] = color_list
 
    #绿色
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['green'] = color_list
 
    #青色
    lower_cyan = np.array([78, 43, 46])
    upper_cyan = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_cyan)
    color_list.append(upper_cyan)
    dict['cyan'] = color_list
 
    #蓝色
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['blue'] = color_list
 
    # 紫色
    lower_purple = np.array([125, 43, 46])
    upper_purple = np.array([155, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(upper_purple)
    dict['purple'] = color_list
 
    return dict

img = cv2.imread("C:\\Users\\TF\\Desktop\\images\\1.jpg", 1)
h, w, _ = img.shape 
dim = (512, 512)
img = cv2.resize(img, dim)
kernel1 = np.ones((5,5),np.uint8) 
kernel2 = np.ones((2,2),np.uint8) 

h, w, _ = img.shape 
mask = np.zeros([h+2, w+2], np.uint8)
image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gau = cv2.GaussianBlur(image,(9,9),0)
sobelX = cv2.Sobel(gau,cv2.CV_64F,1,0)#x方向的梯度
sobelY = cv2.Sobel(gau,cv2.CV_64F,0,1)#y方向的梯度

sobelX = np.uint8(np.absolute(sobelX))#x方向梯度的绝对值
sobelY = np.uint8(np.absolute(sobelY))#y方向梯度的绝对值

sobelCombined = cv2.bitwise_or(sobelX,sobelY)#


canny = cv2.Canny(sobelCombined, 60, 300) 

#mask=np.zeros([h+2,w+2],np.uint8)
#cv2.floodFill(canny,mask,(0,0),255,0,254,cv2.FLOODFILL_FIXED_RANGE)

    # 由于霍夫圆检测对噪声敏感，这里用 均值偏移滤波 移除噪声
    # pyrMeanShiftFiltering(src, sp, sr[, dst[, maxLevel[, termcrit]]]) -> dst
    # 1 data 2 空间窗半径 3 色彩窗半径
canny = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel1)


(cnts, _) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in cnts:        

        Mask = np.zeros(img.shape, dtype="uint8")  #依Contours圖形建立mask

        cv2.drawContours(Mask, [c], -1, (1,1,1), -1) #255        →白色, -1→塗滿

        # show the images
        wcolor = img*Mask
        
        
maxsum = -100
color = None
color_dict = getColorList()       
hsv = cv2.cvtColor(wcolor,cv2.COLOR_BGR2HSV)

for d in color_dict:
        MASk = cv2.inRange(hsv,color_dict[d][0],color_dict[d][1])
        #cv2.imwrite(d+'.jpg',mask)
        binary = cv2.threshold(MASk, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary,None,iterations=2)
        Cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in Cnts:
            sum+=cv2.contourArea(c)
        if sum > maxsum :
            maxsum = sum
            color = d


#將mask與原圖形作AND運算

        #cv2.imshow("Image + Mask", cv2.bitwise_and(image, image, mask=mask))  

        cv2.waitKey(0)


for c in cnts:
    area = cv2.contourArea(c)


cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)

size = area/512/512*100
#cv2.floodFill(canny,mask,(256,256),(255, 255, 255), (100, 100, 100), (50, 50, 50),cv2.FLOODFILL_FIXED_RANGE)
#canny1 = cv2.morphologyEx(canny, cv2.MORPH_OPEN, kernel1)
#canny = cv2.dilate(canny,kernel2,iterations = 10)
#canny = cv2.erode(canny,kernel2,iterations = 15)
#canny = cv2.dilate(canny,kernel2,iterations = 5)
#closing = cv2.morphologyEx(canny, cv2.MORPH_OPEN, kernel2)


cv2.imshow(color,img)
print(size)

cv2.waitKey()


# In[ ]:





# In[ ]:




