# OTA_process

+ files can be reached on LAN via an nginx sharing the source code tree
  - url path: /<device_hostname>/
  - example: http://192.168.1.12/DC32ProOne/
  - root path links doesn't

## dev notes

+ copy nginx docker default config file:
  - `docker run --name tmp-nginx-container -d nginx`
  - `docker cp tmp-nginx-container:/etc/nginx/nginx.conf /host/path/nginx.conf`
+ modify it (add autoindex, for example), then use it

+ autoindex:
location /{ 
   root /home/yozloy/html/; 
   index index.html; 
   autoindex on;
}
