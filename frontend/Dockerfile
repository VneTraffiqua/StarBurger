FROM node:16-alpine as build

WORKDIR /starburger
RUN npm install -g parcel@latest
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm ci --include=dev
COPY ./bundles-src/ ./bundles-src/
ENTRYPOINT ./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
