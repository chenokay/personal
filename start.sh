nginx -c /etc/nginx/nginx.conf -p /root/webpy-skeleton
nohup python app.py 9003 fastcgi & 
