from yaml import load, dump 
import yaml 
import os 

print(yaml.__version__)



with open("config/config.yaml", 'r') as stream :
    data_loaded = yaml.safe_load(stream)

classes = list(set(os.listdir("./data/custom_images/")))
print("CLASSES FOUND " + str(classes)) 
classes.remove("valid_images.txt")
for i in range(len(classes)):
    classes[i] = classes[i][:-1]
    
print("NEW CLASSES " + str(classes))
data_loaded["classes"] = classes 



with open("config/config.yaml",'w') as f:
    yaml.dump(data_loaded,f)


print("UPDATED CONFIG FILE")


