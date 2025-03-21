FROM node:18
WORKDIR /app

COPY .env .env

COPY package.json yarn.lock ./
RUN yarn install
COPY . .
EXPOSE 3000
RUN yarn build
CMD ["yarn", "start"]