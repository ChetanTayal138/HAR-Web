import numpy as np 
import cv2 
import os 
import matplotlib.pyplot as plt 


BASE = "../dataset/"
folders = os.listdir(BASE)
print(folders)


def get_clips(label,images):
    dic = {"stan":0, "kick":1 ,"punc":2}
    k = []
    y = []
    count = 0 
    for i in range(0,len(images)):
        
        if (len(images)-i) >= 5 :
            count += 1 
            k.append(images[i:i+5])
            y.append(dic[label])

    
    return np.vstack(k),y 


def get_labels_images():
    
    labels = []
    images_list = [] 

    for folder in folders:
        label = folder[:4]
        print("LABEL IS " + str(label))
        FOLDER_PATH = BASE + folder  
        images_in_folder = sorted(os.listdir(FOLDER_PATH))
        folder_image = []
        print("LEN IS " + str(len(images_in_folder)))
        for images in images_in_folder[:40]:           
            img = cv2.imread(FOLDER_PATH + "/" + images, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (480,360), interpolation=cv2.INTER_AREA)
            folder_image.append(img)
        
        x,y = get_clips(label,folder_image)
        print(x.shape)
        
        images_list.append(x)
        labels.append(y)
        
    x = np.vstack(images_list)
    
    

    return np.array(labels).reshape(432,1), x.reshape(432,5,360,480, 1)/255.0



if __name__ == "__main__":
    y, x = get_labels_images()
    print(y)
    print(x.shape)
    for i in range(5):
        plt.imshow(x[20][i].reshape(360,480))
        plt.show()


