FROM node:14.16-alpine3.10

WORKDIR /front-end-v2

COPY package*.json ./

COPY . .

RUN npm install
# RUN npm run build
RUN npm install -g serve

# EXPOSE 5000
# CMD [ "serve", "-s","-l","tcp://0.0.0.0", "dist" ]