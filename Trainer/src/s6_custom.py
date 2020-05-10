#!/usr/bin/env python3 



import numpy as np
import cv2
import sys 
import os 


sys.path.append("../")

import utils.lib_images_io as lib_images_io 
import utils.lib_plot as lib_plot 
import utils.lib_commons as lib_commons 
from utils.lib_openpose import SkeletonDetector
from utils.lib_tracker import Tracker 
from utils.lib_classifier import *
import pickle 









SRC_DATA_TYPE = "webcam"
SRC_MODEL_PATH = "../model/trained_classifier.pickle"


DST_FOLDER_NAME = lib_commons.get_time_string()


cfg_all = lib_commons.read_yaml("../config/config.yaml")
cfg = cfg_all["s5_test.py"]

CLASSES = np.array(cfg_all["classes"])
print("CLASSES ARE " + str(CLASSES))
SKELETON_FILENAME_FORMAT = cfg_all["skeleton_filename_format"]

WINDOW_SIZE = int(cfg_all["features"]["window_size"])

SRC_WEBCAM_MAX_FPS = float(cfg["settings"]["source"]["webcam_max_framerate"])


OPENPOSE_MODEL = cfg["settings"]["openpose"]["model"]
OPENPOSE_IMG_SIZE = cfg["settings"]["openpose"]["img_size"]

# Display settings
img_disp_desired_rows = int(cfg["settings"]["display"]["desired_rows"])



loaded_model = pickle.load(open(SRC_MODEL_PATH, "rb"))
print(loaded_model)



images_loader = lib_images_io.ReadFromWebcam(SRC_WEBCAM_MAX_FPS, 0)












from s5_test import MultiPersonClassifier , remove_skeletons_with_few_joints , draw_result_img


skeleton_detector = SkeletonDetector(OPENPOSE_MODEL, OPENPOSE_IMG_SIZE)

multiperson_tracker = Tracker()
multiperson_classifier = MultiPersonClassifier(SRC_MODEL_PATH, CLASSES)

images_displayer = lib_images_io.ImageDisplayer()


if __name__ == "__main__":
    ith_img = -1 
    while images_loader.has_image():
        img = images_loader.read_image()
        ith_img += 1 
        img_displayed = img.copy()
        humans = skeleton_detector.detect(img)
        skeletons, scale_h = skeleton_detector.humans_to_skels_list(humans)
        skeletons = remove_skeletons_with_few_joints(skeletons)

            # -- Track people
        dict_id2skeleton = multiperson_tracker.track(
                skeletons)  # int id -> np.array() skeleton

            # -- Recognize action of each person
        if len(dict_id2skeleton):
            dict_id2label = multiperson_classifier.classify(
                     dict_id2skeleton)

            # -- Draw
        img_displayed = draw_result_img(img_displayed, ith_img, humans, dict_id2skeleton,skeleton_detector, multiperson_classifier,dict_id2label,scale_h)

        if len(dict_id2skeleton):
            min_id = min(dict_id2skeleton.keys())
            print(f"LABEL PREDICTED IS {dict_id2label[min_id]}")
        

        if dict_id2label[min_id] == "slap":
            cv2.imwrite("saved_image.png" , img_displayed)
            #cv2.imshow("DISPLY", img_displayed)
            print(img_displayed.shape)
            break
            
        #images_displayer.display(img_displayed,wait_key_ms=1)
    
