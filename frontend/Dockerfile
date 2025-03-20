FROM node:18

WORKDIR /app

COPY .env .env

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

EXPOSE 3000


CMD ["yarn", "dev"]