import numpy
import tensorflow as tf
from load_data import get_labels_images, get_clips
import os
from sklearn.model_selection import train_test_split, KFold 
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier 
import matplotlib.pyplot as plt 



BASE = "../dataset/"
folders = os.listdir(BASE)

y,x = get_labels_images()

print(y)





x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.05, shuffle=True)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

for i in range(5):
    plt.imshow(x_train[10][i].reshape(360,480))
    plt.show()


def get_model():

    model = tf.keras.Sequential([
        tf.keras.layers.Conv3D(filters=4, kernel_size = (1,3,3),padding='valid',input_shape=(5,360,480,1) ,data_format="channels_last",activation = "relu"),
        tf.keras.layers.Conv3D(filters=8, kernel_size = (1,3,3),padding='valid',activation='relu'),
        tf.keras.layers.Conv3D(filters=16, kernel_size = (1,3,3),padding='valid',activation='relu'),
        tf.keras.layers.MaxPooling3D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64,activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])


    #model.summary()

    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy'])


    return model 


model = get_model()
model.fit(x_train,y_train, epochs=1, batch_size=1)
print(model.evaluate(x_test,y_test,batch_size=1))
model.save("saved_model/my_model")







