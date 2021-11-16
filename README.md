# 2D Image Cones Detection

Cone Detection of 2D Images:
1.	Clone this repository;
2.	Load the dataset compressed in format '.7z' (i.e. *'ConeDataset.7z'*) in the *'Dataset'* folder; the dataset must contain the images and the annotation files (for each image a file .txt with the annotation of the cones);
3.	Run it.

# Skeleton

```
2DImageConesDetection
│	README.md
│	hogenize.py
│
└───YoloDarknet
	│	DarkNet_Conedetection.ipynb
	│	obj.data
	|	obj.names
	│	test.jpg
	│	yolo-obj.cfg
	│
	└───Dataset
		│   ...
		backup
			...
```

# Files

**DarkNet_Conedetection.ipynb**

Notebook: Training, testing with darknet (yolov3) and post-proceccing with OpenCV.

**obj.data**

It specify number of classes and paths of training and testing set, and paths of obj.names and backup folder. 

**obj.names**

Names of classes labels.

**yolo-obj.cfg**

Yolo configuration file.

**homogenize.py**

Label homogenizer.


# Cone detection

## Introduction

In order to implement the driverless part, one of the tasks to solve is the 2D image cone detection.

The cone detection means the automatic detection of the cone in the path that the car must do during the race.

To do this, we implemented some tests a deep convolutional-based neuralnetworks (DarkNet).

Python was used as a programming language and Colab notebook (GPU based cloud computing
platform) for the implementation and execution of the neural networks.

## Preliminary Solution Analysis

First of all, we collected the data needed for the training and test of our neural networks. The data
was shared by several Teams participating in the Competition.

All data, utils and info are available in the following repository https://github.com/ddavid/fsoco.
Every team has used a number to identify a given class, but these numbers can be diﬀerent in each annotation.
Therefore, in order to homogenize the labels, we used the script *homogenize.py*.

The data set selected consists of ca. 8000 images and the respective annotation ﬁles in which the cones
are classiﬁed according to colour and size. To improve learning, the collected images have diﬀerent
characteristics. Some images have cones of the same color, other images have cones of
distinct colors and sizes. Most of the photos are taken from the car, so they have cones arranged in
a regular way to form the track limits. Other photos, instead, are taken by people and have cones
arranged in an irregular manner. Finally, the photos were taken in diﬀerent weather conditions and
in diﬀerent resolutions.

We chose what kind of pre-trained networks to train, and we tested some of these networks
in order to select the best one in terms of accuracy on the test set. For our task we trained the
DarkNet (YOLOv3) and CenterNet network.

## Final Project

### Design

####DarkNet (Yolov3)

YOLOv3 is an object detector that takes the detection procedure as a regression task.

YOLOv3 is anchor-based: it places a set of rectangles with pre-deﬁned sizes, and regressed them to the desired
place with the help of ground-truth objects. This method increases the speed of detection and
accepts input pictures of diﬀerent sizes. YOLOv3 use DarkNet-53 for performing feature extraction.
It uses multi-scale prediction, which means it is detected on multiple scale feature maps.
For this reason, the accuracy of target detection is improved.
DarkNet is an open source neural network framework written in C and CUDA.
It is fast, easy to install, and supports CPU and GPU computation.
The source can be found on GitHub https://github.com/pjreddie/darknet.
YOLOv3 requires the annotation information in the form of text ﬁle.

For training, we need to create a text ﬁle corresponding to each image.
The name of the text ﬁle should be the same as the image ﬁle with a *.txt* extension.
Suppose the image name is *sample.png* then it’s text ﬁle name *sample.txt*.

Each line of the text ﬁle will have below format:

```
<object-class> <x_center> <y_center> <width> <height>.
```

Object-Class is a number which represents the class of the object and ranges from 0 to (number ofclasses – 1);

*x_center*, *y_center* are the x and y coordinates of the cente;

*width* and *height* are the height and width of the boundary box (it can ranges [0.0, 1.0]).

First of all, the repository is been cloned inside the project folder (at the same level as the data folder):

```
git clone https://github.com/AlexeyAB/darknet.git
```

Taking advantage of an nvidia gpu based machine and cuda installed, darknet was compiled via the Makeﬁle with these parameters:

```
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile
make
```

For training, convolution weights have been used that are pretrained on the ImageNet dataset.

The weight ﬁle has been downloaded inside the data folder using the command given below:

```
wget https://pjreddie.com/media/files/darknet53.conv.74
```

To train the network with our dataset the conﬁguration ﬁle has been modiﬁed. First, the *yolo-obj.cfg* ﬁle
has been created inside darknet/cfg folder, and then copied and pasted the content from *yolov3.cfg*.
1.	We changed the number of classes according to our dataset. We have 4 classes then *classes = 4* was set.

2.	*Max Batches* (the maximum number of batches for training) can’t be less than 4000 even you are using 1 class.If you are using k classes then it should be k × 2000. So it has been set:

```
max\_batches = (number of classes) * 2000
```

3.	Steps should be 80% and 90% of the max batches. If the max\_batches=8000 then steps would be:

```
steps = 6400, 7200
```

4.	Finally the number of ﬁlters in [convolutional] section just before [yolo] section has been modiﬁed:

```
filters = (classes + 5) * 3
```

For training and testing, the lists of images have been provided in the text ﬁles.
Two ﬁles *TR.txt*, and *TS.txt* has been created inside the data folder (80% of the total images has
been put into the *TR.txt* and rest 20% into *TS.txt*).

These ﬁles will have the path of the images and path should relative to the darknet executable.

```
[your_path]/001.jpg
[your_path]/002.jpg
[your_path]/003.jpg
[your_path]/004.jpg
```

Then, we created a ﬁle *obj.names* containing the name of all the classes:

```
bigOrangeCone
orangeCone
yellowCone
blueCone
```

Finally, we created a ﬁle obj.data. This ﬁle contains the paths of other ﬁles, the path of the
backup directory and the info about the number of classes:

```
classes = 4
train = .../TR.txt
valid = .../TS.txt
names= .../obj.names
backup = .../backup/
```

####DarkNet (Yolov3)

After conﬁguring Darknet, we ﬁrst trained it using pre-trained weights for the object detection task.

In particular we used *darknet53.conv.74*. For the ﬁrst training we ran the command:

```
./darknet detector train .../obj.data .../yolo-obj.cfg .../darknet53.conv.74
```

where we speciﬁed our conﬁguration ﬁles e the pre-trained weights.

This training keeps saving the weights after every 100 iterations in the backup folder,
and after reaching 1000 iterations, it saves the wheights 1000 iterations.

To restart the training, we ran the train command specifying the last weights saved in the backup directory:

```
./darknet detector train .../obj.data .../yolo-obj.cfg .../backup/yolo-obj\_last.weights
```

To compute the Precision and Recall, the mAP and other values useful for the analysis and validation of the model we run:

```
./darknet detector map .../obj.data .../yolo-obj.cfg .../backup/yolo-obj\_last.weights
```

The detector map compute mAP at IoU threshold of 0.50 by default.

## Conclusions

We created a labeled cone dataset with the help of several Teams participating at the Competition.
We conﬁgured the deep convolutional neural network DarkNet for our purpose and
ﬁnally we tested the performances by computing and analysing some measure and score.

To improve the results we recommend creating a dataset that is as heterogeneous as possible
(climatic conditions, quantity of light, resolution, etc.), but at the same time equally distributed by type of cone.
To comply with this, it may be useful to apply a data augmentation
(e.g. applying horizontal ﬂip, rotation, ZCA withening) to the train dataset.
