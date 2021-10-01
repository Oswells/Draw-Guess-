'''
Author: your name
Date: 2021-09-30 14:24:42
LastEditTime: 2021-09-30 16:27:19
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \canny算子\canny.py
'''
import cv2,os
import numpy as np

# Read the image
try:
    path = r'C:\Users\LZD\Desktop\anything\canny'
except:
    print("Path doesn't exist!")
img_path = os.path.join(path,'pre')
save_path = os.path.join(path,'after')
save_img = os.listdir(save_path)
for file in os.listdir(img_path):
    if file not in save_img:
        img = cv2.imread(os.path.join(img_path,file), flags=1)
        shape = img.shape

        while shape[0]>1000 or shape[1]>1000:
            img = cv2.resize(img,(shape[0]//2,shape[1]//2))
            shape = img.shape
        img = cv2.GaussianBlur(img,(1,1),0) # 用高斯平滑处理原图像降噪。若效果不好可调节高斯核大小
        
        img = cv2.Canny(img, 80, 200,L2gradient=True)     # 调用Canny函数，指定最大和最小阈值，其中apertureSize默认为3。
        img = 255-img
        cv2.imwrite(os.path.join(save_path,file), img)
