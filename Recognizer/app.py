from flask import Flask, render_template, Response , request , after_this_request
import sys 
sys.path.append("src/")
from s7 import SkeletonsGenerator 
import cv2 
import time 
import socket 
import threading 
from flaskthreads import AppContextThread 




def get_time(ob):
    while(True):
        time.sleep(1)
        
        if time.time() - ob.curr_time > 2:
            print("SHUTTING DOWN CAM")
            ob.images_loader._video.release()
            return 
    




app = Flask(__name__)




@app.route('/')

def index():
    return render_template("index.html")


def gen(skeleton_generator):
            
    while(True):
        frame = skeleton_generator.generate_frames()
        ret,frame = cv2.imencode('.jpg',frame) 
        frame = frame.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    print("AFTER LOOP")




@app.route("/video_feed")
def video_feed():
    
    ob = SkeletonsGenerator()
    while(True):
        t = AppContextThread(target = get_time,args=[ob])
        return Response(gen(ob),mimetype='multipart/x-mixed-replace;boundary=frame') , t.start()

    
    '''def exit_cv2_window():
        print("CLOSED WEBCAM")
        ob.images_loader._video.release()'''



if __name__ == '__main__':

    
    app.run(host='0.0.0.0',port='80',debug=True)
    
    
    
    

















