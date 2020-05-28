# Introduction 
HAR-Web is a web application that can be utilized to carry out the task of Human Activity Recognition in real time on the web using GPU-enabled devices. The web application is based on a micro service architecture where the project has been divided into 4 basic services, each running on a different port and deployed using Docker containers. I would like to add support for Kubernetes but as of now it doesn't support native hardware access like Docker-Swarm. One way of solving this would be to write a host device plugin like https://github.com/honkiko/k8s-hostdev-plugin but specifically for webcam access. If anyone has an idea on how to enable local webcam access on K8S, I would love to hear about it. 


# Microservices Architecture

## Services

#### *Frontend Service* 
Initial page for the app that gives the user the option to train their own model or use existing model and routes to the appropriate service accordingly. (plan to add presets) 

#### *Recorder Service* 
Video recording service written in NodeJS that allows user to record videos and then store it for training. By default the videos are recorded at 10 FPS and a total of 300 frames are recorded to generate a good enough amount of training data for each action. 

#### *Recognizer Service* 
Contains serialized model deployed using Flask and streams the predictions in real time after capturing video feed from a webcam in real time.

#### *Training Service*
Modifies the config file with the appropriate labels and model of choice and then starts the training process in the background which consists of generating heatmaps. 

## Architecture

Each service has been containerised using Docker. You can find the dockerfile for each service in their respective folder. In order to start the entire system together, we can simply use the [docker-compose file](https://github.com/ChetanTayal138/HAR-Web/blob/master/docker-compose.yml) which describes all the dependencies and commands to build and start each container.  
Ports for the different services in the docker-compose file are listed below:  

| Service | Port |
| ------- | ---- | 
| Frontend | 5000 |
| Recorder | 5001|
| Trainer  | 5002 |
| Recognizer | 5003 |



# 1. Recognizer 

## 1.1 Human Activity Recognition

Human Activity Recognition is a domain in Computer Vision that deals with identifying what action is being performed by a human entity in a video feed. 
Deep Learning approaches to carry out human activity recognition has been typically been tackled using 3D-CNNs, LRCNNs and also the widely adopted 2-Stream Architecture https://github.com/jeffreyyihuang/two-stream-action-recognition that uses both RGB-images and optical flow. 

HAR-Web is based on the project by https://github.com/felixchenfy/Realtime-Action-Recognition that utilizes Human Pose Estimation to generate 2D-Skeletons and use skeleton coordinates to classify actions. A big advantage of this approach is the reduced computation needed to carrying out action recognition making it a much viable approach when it comes to identifying human actions in a real time basis.


## 1.2 Human Pose Estimation 

Human 2D pose estimation deals with localization of different key human parts and using these localized points to construct a pose for the human. HAR-Web uses https://github.com/ildoonet/tf-pose-estimation to generate the 2D-Poses which is 
an implementation of OpenPose(written in Caffe) in TensorFlow. 

The model developed by CMU uses Part-Affinity Fields ( https://arxiv.org/pdf/1611.08050.pdf ) and has a t stage, two branch process of generating the predictions for poses. In the first stage, a neural network is used to carry out two simultaneous predictions : A set 'S' of 2D confidence maps for body part locations and a set 'L' of 2D vector fields of part affinities, which encode the degree of association between different body parts. 

The two branches use feature maps F generated using the first 10 layers of VGG-19 as their inputs, with the first branch predicting the set S and the second branch predicting the set L. Subsequent stages use these predictions and concatenate with the original feature map F and used iteratively to produce refined productions. 

## 1.3 Skeleton Data To Actions

The skeleton generated by OpenPose has 18 joints and each joint has 2 coordinates(x,y) associated with it. Preprocessing is then done to :-
  1. Scale the x and y coordinates as OpenPose has different scales for these.
  2. Removal of joints on the head. 
  3. Get rid of frames with no necks or thigh detected.
  4. Filling of missing joints 
  
  Features are then extracted by concatenating the skeleton data from a window of 5 frames at a time. The exact feature extraction has been described in the original [report](https://github.com/felixchenfy/Data-Storage/blob/master/EECS-433-Pattern-Recognition/FeiyuChen_Report_EECS433.pdf) that also talks about specific feature selection that were the most effective for training. 

A total feature vector of dimension 314 is created and reduced to 50 dimensions using PCA. This 50 dimension network is finally used to classify different actions using a neural network with 3 hidden layers of 100 nodes each. 


# 2. Recorder  

Built using [opencv4nodejs](https://www.npmjs.com/package/opencv4nodejs), which is an API for native OpenCV for NodeJS.   this service deals with recording the video of a person and stores it as frames for our training data. The base image that I used for creating the docker container that had a working and compatible version of opencv4nodejs is available [here](https://hub.docker.com/layers/justadudewhohacks/opencv4nodejs-ci/3.4.6-contrib-node8/images/sha256-e591cbe4842e821d97accdf04d4e6723c04d0955a0893a2863cbdcee45fa74d1?context=explore) on DockerHub.

A big advantage of using opencv4nodejs over using simply Flask for a task like this was because it provides an asynchronous API that allows built in multithreading and doesn't have to rely on something like Flask-Threads to avoid non-blocking calls.
This is important in our application because it allows us to save record and save the frames on two seperate threads and leads to performance gains. 





## References and Links 

| Title | Link | 
| ------ | ----- | 
| 2 Stream Convolution | http://papers.nips.cc/paper/5353-two-stream-convolutional
| Temporal Segment Networks | https://link.springer.com/chapter/10.1007/978-3-319-46484-8_2 |
| TS-LSTM  | https://arxiv.org/abs/1703.10667 | 
| Human activity recognition from skeleton poses  | https://arxiv.org/pdf/1908.08928v1.pdf |


