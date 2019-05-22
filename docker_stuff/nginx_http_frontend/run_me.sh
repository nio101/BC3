docker run --rm -d -p 80:80 -v /home/nio/code/BC3/ESP32:/usr/share/nginx/html -v /home/nio/code/BC3/docker_stuff/nginx_http_frontend/nginx.conf:/etc/nginx/nginx.conf nginx:alpine
