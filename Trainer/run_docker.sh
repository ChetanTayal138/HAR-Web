docker run -d --gpus all -v ~/container-data/image_data:/app/data/custom_images -v ~/container-data/config:/app/config -v ~/container-data/model:/app/model -p 5002:80 trainer:latest
