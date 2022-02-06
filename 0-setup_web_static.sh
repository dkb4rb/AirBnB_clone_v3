#!/usr/bin/env bash
# This script install and configure new web static fake page

#new simbolic link to page current
function symbol_link(){
        ln -sf /data/web_static/releases/test/ /data/web_static/current
}

#create new file fake  index html
function new_fake_page(){
        echo -ne "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" | sudo tee /data/web_static/releases/test/index.html 
}


#create new dirextories to web static pages
function new_dirs(){
        mkdir -p /data/web_static/releases/test/
        mkdir -p /data/web_static/shared/
}

#comprove all dependences to server
# execute one update first
function dependences(){
        apt-get update
        apt-get install -y nginx
        service nginx start
}

# The function execute one configuration to nginx server to http response
# to curl comman the result is Hello World!
function config_response(){
        touch /var/www/html/index.html
        echo "Hello World" > /var/www/html/index.html
        printf %s "server {
             listen      80 default_server;
             listen      [::]:80 default_server;
             root        /var/www/html;
             index       index.html index.html;
        }
        " > /etc/nginx/sites-available/default
        service nginx restart
}

#Function main is the init to all functions
function main(){
        dependences;
#       config_response;
        new_dirs;
        new_fake_page;
        symbol_link;
# Giving Ownership and permissions
        chown -R ubuntu:ubuntu /data/
# Creating alias for location in nginx conf
        sed -i '48i \\tlocation /hbnb_static {\n\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
# Restarting nginx
        service nginx restart
}

# Declare the flush to progam
main;
