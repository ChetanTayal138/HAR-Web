from flask import Flask , render_template , redirect , url_for
import os 
import threading 
from flaskthreads import AppContextThread
import time 
import multiprocessing 

app = Flask(__name__)



@app.route('/')
def train():
    os.system("bash run_files.sh")
    '''i = 0
    while(i<10):
        print(i)
        time.sleep(0.5)
        i = i + 1'''
    return render_template("redir.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
