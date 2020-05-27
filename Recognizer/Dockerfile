FROM tensorflow/tensorflow:1.14.0-gpu-py3

RUN apt-get update -y &&\apt-get install -y python3-pip python3-dev &&\apt-get install -y libsm6 libxext6 libxrender-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip &&\pip3 install -r requirements.txt &&\pip3 install pycocotools numpy==1.18 Flask-Threads

COPY . /app

ENTRYPOINT ["/bin/bash"]

CMD ["run_files.sh"]
