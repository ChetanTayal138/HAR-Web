#!/usr/bin/env python3 

import numpy as np
import cv2 
import sys 
import os 
sys.path.append("utils/")
import lib_images_io
import lib_plot 
import lib_commons 
from lib_openpose import SkeletonDetector
from lib_tracker import Tracker 
from lib_classifier import * 
from s5_test import MultiPersonClassifier , remove_skeletons_with_few_joints, draw_result_img
import time 



class SkeletonsGenerator :

    def __init__(self):
        self.DATA_TYPE = "webcam"
        self.MODEL_PATH = "model/trained_classifier.pickle"
        self.cfg_all = lib_commons.read_yaml("config/config.yaml")
        self.set = False
        self.cfg = self.cfg_all["s5_test.py"]
        self.classes = np.array(self.cfg_all["classes"])
        self.SKELETON_FILENAME_FORMAT = self.cfg_all["skeleton_filename_format"]
        self.WINDOW_SIZE = int(self.cfg_all["features"]["window_size"])
        self.SRC_WEBCAM_MAX_FPS = float(self.cfg["settings"]["source"]["webcam_max_framerate"])
        self.OPENPOSE_MODEL = self.cfg["settings"]["openpose"]["model"]
        self.OPENPOSE_IMG_SIZE = self.cfg["settings"]["openpose"]["img_size"]
        self.img_disp_desired_rows = int(self.cfg["settings"]["display"]["desired_rows"])
        self.images_loader = lib_images_io.ReadFromWebcam(self.SRC_WEBCAM_MAX_FPS,0)
        self.skeleton_detector = SkeletonDetector(self.OPENPOSE_MODEL, self.OPENPOSE_IMG_SIZE)
        self.multiperson_tracker = Tracker()
        self.multiperson_classifier = MultiPersonClassifier(self.MODEL_PATH,self.classes)
        self.curr_time = time.time() 

    def generate_frames(self):

        ith_img = -1 

        while self.images_loader.has_image():
            img = self.images_loader.read_image()
            self.curr_time = time.time() 
            print("TIME CAPTURED" + str(self.curr_time))                
            ith_img += 1 
            img_displayed = img.copy()
            humans= self.skeleton_detector.detect(img)
            skeletons,scale_h = self.skeleton_detector.humans_to_skels_list(humans)
            skeletons = remove_skeletons_with_few_joints(skeletons)

            dict_id2skeleton = self.multiperson_tracker.track(skeletons)

            if len(dict_id2skeleton):

                dict_id2label = self.multiperson_classifier.classify(dict_id2skeleton)

                img_displayed = draw_result_img(img_displayed, ith_img, humans, dict_id2skeleton, self.skeleton_detector, self.multiperson_classifier, dict_id2label, scale_h)

            
            return img_displayed
        


if __name__ == "__main__":
    c1 = SkeletonsGenerator()
    while(True):
        print(c1.generate_frames())

