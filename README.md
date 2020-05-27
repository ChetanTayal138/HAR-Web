# 1. Introduction 

HAR-Web is a web application that can be utilized to carry out the task of Human Activity Recognition in real time on the web using GPU-enabled devices. 

## 1.1 Human Activity Recognition

Human Activity Recognition is a domain in Computer Vision that deals with identifying what action is being performed by a human entity in a video feed. 
Deep Learning approaches to carry out human activity recognition has been typically been tackled using 3D-CNNs, LRCNNs and also the widely adopted 2-Stream Architecture https://github.com/jeffreyyihuang/two-stream-action-recognition that uses both RGB-images and optical flow. 

HAR-Web is based on the project by https://github.com/felixchenfy/Realtime-Action-Recognition that utilizes Human Pose Estimation to generate 2D-Skeletons and use skeleton coordinates to classify actions. A big advantage of this approach is the reduced computation needed to carrying out action recognition making it a much viable approach when it comes to identifying human actions in a real time basis.


## 1.2 Human Pose Estimation 

Human 2D pose estimation deals with localization of different key human parts and using these localized points to construct a pose for the human. HAR-Web uses https://github.com/ildoonet/tf-pose-estimation to generate the 2D-Poses which is 
an implementation of OpenPose(written in Caffe) in TensorFlow. 

The model developed by CMU uses Part-Affinity Fields ( https://arxiv.org/pdf/1611.08050.pdf ) and has a t stage, two branch process of generating the predictions for poses. In the first stage, a neural network is used to carry out two simultaneous predictions : A set 'S' of 2D confidence maps for body part locations and a set 'L' of 2D vector fields of part affinities, which encode the degree of association between different body parts. 

The two branches use feature maps F generated using the first 10 layers of VGG-19 as their inputs, with the first branch predicting the set S and the second branch predicting the set L. Subsequent stages use these predictions and concatenate with the original feature map F and used iteratively to produce refined productions. 













## References and Links 
| Title | Link | 
| ------ | ----- | 
| 2 Stream Convolution | http://papers.nips.cc/paper/5353-two-stream-convolutional
| Temporal Segment Networks | https://link.springer.com/chapter/10.1007/978-3-319-46484-8_2 |
| TS-LSTM  | https://arxiv.org/abs/1703.10667 | 
| Human activity recognition from skeleton poses  | https://arxiv.org/pdf/1908.08928v1.pdf |


