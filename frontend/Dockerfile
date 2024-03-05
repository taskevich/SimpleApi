FROM node:18-buster as builder

COPY package*.json .

RUN npm i

COPY . .

RUN npm run build

EXPOSE 80

CMD ["npm", "run", "start"]