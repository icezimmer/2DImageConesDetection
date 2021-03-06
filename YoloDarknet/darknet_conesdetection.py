# -*- coding: utf-8 -*-
"""DarkNet_ConesDetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j_Z-uiDR4nf-SzXXbRC5jab2ZU9p0Sda
"""

import cv2
import numpy as np
import string as st

from google.colab import drive
drive.mount('/content/drive')

!nvidia-smi

"""**Download darknet**



"""

!git clone https://github.com/AlexeyAB/darknet.git

"""**Compile darknet with NVIDIA GPU**"""

# Commented out IPython magic to ensure Python compatibility.
# %cd darknet
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!make

"""**Download the pretrained weights**"""

!wget https://pjreddie.com/media/files/darknet53.conv.74

"""**Create files Train and Validate .txt for obj.data**"""

fname_tr = "/content/drive/MyDrive/Data/FaSTDa_2020_Train.txt"
fname_vl = "/content/drive/MyDrive/Data/FaSTDa_2020_Validate.txt"
deleteContent(fname_tr)
deleteContent(fname_vl)
#print(file_len(fname))
n = 600
l = 600 * (80/100)
i = 0
text = '/content/drive/MyDrive/Data/FaSTDa_2020/image%d.jpg' %i
with open(fname_tr, "a") as f_tr, open(fname_vl, "a") as f_vl:
  for i in range(n):
    if i < l:
      f_tr.write(text+'\n')
      text = text.replace('image%d' %i, 'image%d' %(i+1))
    else:
      f_vl.write(text+'\n')
      text = text.replace('image%d' %i, 'image%d' %(i+1))

"""**Extracting images**"""

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/MyDrive/Data'
!p7zip -d '/content/drive/MyDrive/Data/TRset.7z'
#!unzip mydrive /content/drive/MyDrive/Data/images

import glob
images_list = glob.glob("/content/drive/MyDrive/Data/TRset/*.jpg")
#print(images_list)

#create trainng.txt file
file = open('/content/drive/MyDrive/Data/TR.txt', 'w')
file.write("\n".join(images_list))
file.close()

"""**Training**"""

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/darknet

!./darknet detector train /content/drive/MyDrive/obj.data /content/drive/MyDrive/yolo-obj.cfg /content/darknet/darknet53.conv.74 -dont_show -mjpeg_port 8090 -map

"""**Computing mAP**"""

!./darknet detector map /content/drive/MyDrive/obj.data /content/drive/MyDrive/yolo-obj.cfg /content/drive/MyDrive/backup/yolo-obj_last.weights -dont_show

"""**Re-Training**"""

!./darknet detector train /content/drive/MyDrive/obj.data /content/drive/MyDrive/yolo-obj.cfg /content/drive/MyDrive/backup/yolo-obj_last.weights -dont_show -map

"""**Testing (test a single img)**"""

!./darknet detector test /content/drive/MyDrive/obj.data /content/drive/MyDrive/yolo-obj.cfg /content/drive/MyDrive/backup/yolo-obj_last.weights -dont_show -ext_output

"""**Testing (test multiple images)**"""

!./darknet detector test /content/drive/MyDrive/obj.data /content/drive/MyDrive/yolo-obj.cfg /content/drive/MyDrive/backup/yolo-obj_last.weights -dont_show -ext_output < /content/drive/MyDrive/Data/FaSTDa_2020_Validate.txt > /content/drive/MyDrive/Data/result1.txt

"""**Post-processing (OpenCV)**"""

net = cv2.dnn.readNet('/content/drive/MyDrive/backup/yolo-obj_last.weights', '/content/drive/MyDrive/yolo-obj.cfg')

classes = ['OR', 'or', 'y', 'b']
layers_names = net.getLayerNames()
outputlayers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
#colors in BGR
colors = ((0, 69, 255), (0, 69, 255), (0, 255, 255), (255, 0, 0))

img_path = '/content/drive/MyDrive/test1.jpg'
img = cv2.imread(img_path)
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channel = img.shape
#print(width, height, img.shape)

yolo_width = 608
yolo_height = 608
blob = cv2.dnn.blobFromImage(img, 0.00392, (yolo_width,yolo_height), (0,0,0), True, crop=False)
net.setInput(blob)

outs = net.forward(outputlayers)

class_ids = []
confidences = []
boxes = []

"""**Ignoring weak detections (confidence < 0.5)**"""

for out in outs:
  for detection in out:
    #print(detection)
    scores = detection[5:]
    class_id = np.argmax(scores)
    confidence = scores[class_id]
    if confidence > 0.5:
      center_x = int(detection[0] * width)
      center_y = int(detection[1] * height)
      w = int(detection[2] * width)
      h = int(detection[3] * height)

      x = int(center_x - w /2)
      y = int(center_y - h /2)

      boxes.append([x, y, w, h])
      confidences.append(float(confidence))
      class_ids.append(class_id)

      #cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

"""**Applying non-max suppression**"""

conf_threshold = 0.5
nms_threshold = 0.4
indexes = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
print(indexes)
print(boxes)
print(class_ids)
print(classes)
print(confidences)
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
  if i in indexes: #prende solo quelli con una certa confidenza
    x, y, w, h = boxes[i]
    label = str(classes[class_ids[i]])
    color = colors[class_ids[i]]
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)
    cv2.putText(img, label, (x, y+30), font, 2, color, 1)

import matplotlib.pyplot as plt
#print image transforming BGR-->GBR
plt.figure(figsize = (16,9))
imgplot = plt.imshow(img[...,::-1])

from google.colab.patches import cv2_imshow
cv2_imshow(img)
cv2.waitKey(0)

