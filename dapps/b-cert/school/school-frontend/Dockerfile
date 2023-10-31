# build environment
FROM node:14.16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3003
RUN npm run build
CMD [ "npm", "run", "start" ]
