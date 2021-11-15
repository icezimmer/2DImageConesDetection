# 2D Image Cones Detection

Cone Detection of 2D Images. Load the dataset compressed '.7z' in Dataset folder.
The dataset must contain the images and the annotation files (for each image a file .txt with the annotation of the cones).

# Skeleton

```
2DImageConesDetection
│	README.md
│	hogenize.py
│
└───YoloDarknet
	│   DarkNet_Conedetection.ipynb
	│   obj.data
	│	obj.data
	│	test.jpg
	│	yolo-obj.cfg
	│
	└───Dataset
		│   ...
		backup
			...
```

# Files



## DarkNet_Conedetection.ipynb

Notebook: Training, testing with darknet (yolov3) and post-proceccing with OpenCV.

## obj.data

It specify number of classes and paths of training and testing set, and paths of obj.names and backup folder. 

## obj.names

Names of classes labels.

## yolo-obj.cfg

Yolo configuration file.

## homogenize.py

Label homogenizer.
