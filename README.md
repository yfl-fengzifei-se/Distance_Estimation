# Distance_Estimation
Opencv 3.2.0 project with python 2.7 under Ubuntu Mate 16.04 !  

My main goal is to estimate the distance from object(vehicles) to ths monocular camera.  

Before that, I do some practices and record it to purchase my goal.

## How to use the code?

1. Prepare the environment

Folowing the [tutorial](https://paper.dropbox.com/doc/Single-Shot-Mutilbox-Detector-Environment-built-in-Ubuntu16.04-Caffe-Cuda8.0-python-2.7-Opencv3.2.0-P8eT6TMnbJSw5DzUOgrli)
 , you can build the caffe, CUDA 8.0, cuDNN v5.1, Python2.7 + Opencv v3.2.0


2. Run the code!

#### Local machine version
If you only want to use for local machine. please prepare the environment and a webcam connected to the computer.
($ means that command in the terminal)

```
# Assume you already enter the depository
$ python ssd_local.py
```
#### For remote version
![architecture](/socket.png)

* under the server
```
$ python ssd_TCP_server.py
# Then enter the IP(Static) and port
```
* under the client
```
$ python ssd_TCP_client.py
# Then enter the IP and port same as server
```



## Folder Introduction 

### Base_implement
- There are some basic implements for opencv. Such as **Calibrate the camera**, **Haar-feature for face or car detection**, **save video**, and **socket programing**...etc.

### caffe
- It's a deep-learning library. I use it for object detection and recognizing. Single shot multibox detector is the most popular implement for computer vision. Due to its high accuracy and speed, decide to use it for my project!


```
In the end. Thanks very much to Mr. Wei Liu for his great ssd tutorial and resources.
@inproceedings{liu2016ssd,
  title = {{SSD}: Single Shot MultiBox Detector},
  author = {Liu, Wei and Anguelov, Dragomir and Erhan, Dumitru and Szegedy, Christian and Reed, Scott and Fu, Cheng-Yang and Berg, Alexander C.},
  booktitle = {ECCV},
  year = {2016}
}
```
