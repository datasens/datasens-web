FROM nginx:1.19.0-alpine
LABEL maintainer = "natig.aminov@gmail.com"

RUN apk update && apk upgrade && apk add bash

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d