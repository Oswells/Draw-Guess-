## 关于我写了一个Draw&Guess的外挂

### 环境

我使用的python版本为3.7.3.

如果你的python版本与我相近，可直接使用以下语句安装所需库。

```shell
pip install -r requirement.txt
```

如果相差较大，可以查看requirement.txt，自行安装所需库。

### 边缘提取

我的想法是将获取得到的图片将边缘进行提取，这样就得到一个主要包含人物轮廓的图片，通过遍历图片，可以知道哪些地方需要绘画。

这里我使用了canny算子进行边缘提取操作，最终效果是将一个目录下的所有图片进行边缘提取，并保存至另一个目录下。

```python
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
        
        img = cv2.Canny(img, 80, 200,L2gradient=True) # 调用Canny函数，指定最大和最小阈值，其中apertureSize默认为3，调整两个阈值以达到较好的效果
        img = 255-img
        cv2.imwrite(os.path.join(save_path,file), img)
```



### 鼠标控制

我的想法是现在有了一个提取了边缘的灰度图，灰度图像可以通过阈值二值化，转变为一个简单的二维矩阵，随后通过控制鼠标，遇到矩阵中的有效值便按下左键，并拖动一小段距离。

这里我找到了pyautogui库，它可以实现鼠标的控制。

```python
# -*- encoding: utf-8 -*-
import os
import cv2
import numpy as np
import pyautogui as pag
pag.PAUSE = 0.005	#设置绘画速度，这个值越小，画得越快
after_path = r"C:\Users\LZD\Desktop\anything\canny\after"
img = after_path + os.sep + 'js.jpg'
screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
img = cv2.imread(img,0)		#读取灰度图
size = img.shape

#设置画布左上角
start_x = screenWidth//2 - size[1]//2
start_y = screenHeight//2 - size[0]//2

img = img>110	#阈值二值化，转变为只含有True or False的矩阵

for i in range(size[1]):
    for j in range(size[0]):
        if img[j][i] == True:
            pag.moveTo(start_x + i, start_y + j)	#移动到目标像素
            pag.dragRel(0, 1)	#按住左键向下滑动一个像素
```

### 优化

上面已经可以实现绘画了，但是实际上它的绘画效率是非常低的，因此我考虑了优化。首先是二值化后的图像矩阵的每一列都会有很多点是连在一起的，因此可以考虑一笔画完这些点，而不需要一个像素一个像素地画，其次，画笔是有粗细的，那么就不需要绘画原矩阵的每一列，只需要每隔多少列画一列即可。下面就是按照这两个想法修改的代码。

```python
# -*- encoding: utf-8 -*-
import os
import cv2
import numpy as np
import pyautogui as pag
px = 4              #画笔像素大小、画笔的粗细
pag.PAUSE = 0.005	#设置绘画速度，这个值越小，画得越快
after_path = r"C:\Users\LZD\Desktop\anything\canny\after"
img = after_path + os.sep + 'jinx.jpg'
screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
img = cv2.imread(img,0)		#读取灰度图
img = np.array(img).astype(np.uint8)
size = img.shape

#处理过大的图片
while size[0]>1000 or size[1]>1000:
    img = cv2.resize(img,(size[0]//2,size[1]//2))
    size = img.shape

#设置画布左上角
start_x = screenWidth//2 - size[1]//2
start_y = screenHeight//2 - size[0]//2

delete = [i for i in range(size[1]) if i%px]
img = np.delete(img, delete, axis=1)
size = img.shape

img = img>110	#阈值二值化，转变为只含有True or False的矩阵
n_img = np.zeros(size).astype(np.uint8)
for i in range(size[1]):
    for j in range(size[0]):
        if img[j][i] == True:
            for k in range(size[0]-j):
                if img[j+k][i] == True:
                    n_img[j][i] += 1
                else:
                    break
                    
for i in range(size[1]):
    for j in range(size[0]):
        if n_img[j][i] != 0:
            for k in range(1,n_img[j][i]):
                n_img[j+k][i] = 0
            pag.moveTo(start_x + i*px, start_y + j)	#移动到目标像素
            pag.dragRel(0, n_img[j][i])	#按住左键向下滑动多个像素

```



