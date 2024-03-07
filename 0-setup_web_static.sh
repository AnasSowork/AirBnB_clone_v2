#!/bin/bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file for testing
echo "<html><head><title>Test Page</title></head><body><h1>This is a test page</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership of /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
nginx_alias="location /hbnb_static/ { alias /data/web_static/current/; }"
if ! grep -qF "$nginx_alias" "$nginx_config"; then
    sudo sed -i "/^\s*server\s*{/,/^\s*}/ { /^\s*}/ i \\\t$nginx_alias\n}" "$nginx_config"
fi

# Restart Nginx
sudo service nginx restart
