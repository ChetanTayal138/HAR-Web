#!/bin/bash



python3 create_valid_images_txt.py
python3 modify_config.py
python3 src/s1_get_skeletons_from_training_imgs.py;
python3 src/s2_put_skeleton_txts_to_a_single_txt.py;
python3 src/s3_preprocess_features.py;
python3 src/s4_train.py
echo "Finished Training"
exit

