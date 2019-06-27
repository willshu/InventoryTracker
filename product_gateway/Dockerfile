FROM nginx
RUN apt-get update && apt-get install -y iputils-ping
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN nginx