import cv2
import random
import numpy as np
import math
import PIL.Image as Image
import os
from matplotlib import pyplot as plt
import scipy.io as sio
#import picamera
from classify import classifyObject as co

def takePic():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
        #plt.imshow(frame)
    path = './179jGit/temp.jpg'
    cv2.imwrite(r'./179jGit/temp.jpg', frame)
    #print (frame)
    label = co(path)
    print (label)
    return label


