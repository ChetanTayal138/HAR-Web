import tensorflow as tf 
import numpy as np 
import cv2 









def load_model(view=False):
    new_model = tf.keras.models.load_model("saved_model/my_model")
    if(view):
        new_model.summary()

    return new_model 


if __name__ == "__main__":
    diz = {0:"stand", 1:"kick" , 2:"slap"}
    model = load_model()
    cap = cv2.VideoCapture(0)


    groups = []
    while(True):
      
    # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = gray.reshape(gray.shape[0],gray.shape[1],1)
        img = cv2.resize(img, (480,360))
        img = img.T
        img = img.reshape(360,480,1)/255.0
        groups.append(img)
        if(len(groups) == 5):
            groups = np.array(groups).reshape(1,5,360,480,1)
            #print(model.evaluate(groups,np.array(1).reshape(1,1)))
            print(diz[np.argmax(model.predict(groups,batch_size=1,verbose=1))])
            groups = []
            
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()






