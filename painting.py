'''
Author: Junjie Zhang
Date: 2021-09-03 14:55:45
LastEditor: Junjie Zhang
LastEditTime: 2021-09-09 20:30:09
Operating System: Linux Deepin 20
Description: 
'''
# -*- encoding: utf-8 -*-
import os
import cv2
import sys
import numpy as np
import pyautogui as pag
def painting(argv):
	px = 4              #画笔像素大小、画笔的粗细
	pag.PAUSE = 0.005	#设置绘画速度，这个值越小，画得越快
	after_path = r'.\after'
	img = after_path + os.sep + argv + '.jpg'
	screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
	img = cv2.imread(img,0)		#读取灰度图
	img = np.array(img).astype(np.uint8)
	size = img.shape

	#处理过大的图片
	while size[0]>1000 or size[1]>1000:
	    img = cv2.resize(img,(size[0]//2,size[1]//2))
	    size = img.shape
	print(size)
	#设置画布左上角
	start_x = screenWidth//2 - size[1]//2
	start_y = screenHeight//2 - size[0]//2

	delete = [i for i in range(size[1]) if i%px]
	img = np.delete(img, delete, axis=1)
	size = img.shape
	print(size)
	img = img>100	#阈值二值化，转变为只含有True or False的矩阵
	n_img = np.zeros(size).astype(np.uint8)
	for i in range(size[1]):
	    for j in range(size[0]):
	        if img[j][i] == True:
	            for k in range(size[0]-j):
	                if img[j+k][i] == True:
	                    n_img[j][i] += 1
	                else:
	                    break
	try:
	    for i in range(size[1]):
	        for j in range(size[0]):
	            if n_img[j][i] != 0:
	                for k in range(1,n_img[j][i]):
	                    n_img[j+k][i] = 0
	                pag.moveTo(start_x + i*px, start_y + j)	#移动到目标像素
	                pag.dragRel(0, n_img[j][i])	#按住左键向下滑动多个像素
	except KeyBoardError:
	    sys.exit(0)

if __name__ == "__main__":
   painting(sys.argv[1])