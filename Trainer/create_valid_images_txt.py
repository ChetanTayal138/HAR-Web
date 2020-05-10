import os 

PATH = "data/custom_images/"
classes = os.listdir(PATH)


with open(os.path.join(PATH,"valid_images.txt"), 'w+') as f:
    for class_ in classes:
        if("txt" not in class_):
            f.write(f"{class_}\n20 280\n")

print("FINISHED WRITING")


