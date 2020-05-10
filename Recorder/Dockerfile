FROM justadudewhohacks/opencv4nodejs-ci:3.4.6-contrib-node8

WORKDIR /app

COPY package.json /app

RUN npm install

RUN export NODE_PATH=/usr/lib/node_modules

RUN apt-get update

COPY . /app

CMD node index.js

EXPOSE 80
           
