FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json /app
COPY src /app/src
COPY public /app/public

RUN npm install --legacy-peer-deps

#RUN npm run build


CMD ["npm", "run", "start"]