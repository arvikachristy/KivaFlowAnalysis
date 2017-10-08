FROM node:latest

COPY package.json /workspace/
COPY *.js /workspace/
WORKDIR /workspace

RUN npm install

ENTRYPOINT ["node", "index.js"]
