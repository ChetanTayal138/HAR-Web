docker run -d -v ~/container-data/config:/app/config -v ~/container-data/model:/app/model --gpus all --device=/dev/video0 --rm -p 5003:80 recognizer:latest
