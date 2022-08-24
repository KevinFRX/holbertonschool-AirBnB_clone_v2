#!/usr/bin/env bash
# Sets up webservers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
sudo mkdir -p /data/web_static/{releases/test,shared}
sudo echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\
\t</body>\n</html>"| sudo tee /data/web_static/releases/test/index.html >/dev/null
# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Adjust permissions
sudo chown ubuntu:ubuntu -R /data
sudo sed -i '/listen 80 default_server/a \\tlocation /hbnb_static/ {\n\t alias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
# Restart nginx
sudo service nginx restart
# Exit with 0 code
exit 0
