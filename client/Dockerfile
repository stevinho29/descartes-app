FROM node:20-alpine as builder

WORKDIR /app

COPY ./ /app

RUN npm install --legacy-peer-deps

#RUN npm run build


CMD ["npm", "run", "start"]