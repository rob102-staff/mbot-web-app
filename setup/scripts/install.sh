sudo apt update
sudo apt install nginx
sudo apt install python3
sudo apt install python3-pip

# Create ~/tmp/mbot-install
mkdir -p ~/tmp/mbot-install
cd ~/tmp/mbot-install

# Clone mbot repository
git clone "https://github.com/rob102-staff/mbot-web-app.git"
cd mbot-web-app

# Create directory for mbot persistent storage api
sudo mkdir -p /data/www/mbot

# the directories for the mbot web application
sudo mkdir -p /data/www/mbot/app-skeleton/
sudo mkdir -p /data/www/mbot/packages/

# the directories for mbot git repositories
sudo mkdir -p /data/mbot/git/

sudo chmod -R a+rwx /data/www/mbot

echo "Setting up Nginx"
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/nginx.conf
sudo cp ~/tmp/mbot-install/mbot-web-app/setup/config/nginx.conf /etc/nginx/nginx.conf

sudo systemctl restart nginx

# setup the mbot cli
sudo mkdir /data/mbot/cli
sudo cp ~/tmp/mbot-install/mbot-web-app/mbot-web-app-cli/*.py /data/mbot/cli
sudo python3 -m pip install -r ~/tmp/mbot-install/mbot-web-app/mbot-web-app-cli/requirements.txt
sudo chmod a+x /data/mbot/cli/cli.py
sudo ln -s /data/mbot/cli/cli.py /usr/local/bin/mbot-cli

echo "Installed the mbot cli. Execute 'mbot-cli --help' for information on how to use it."

# add app-skeleton to mbot 
sudo cp -r ~/tmp/mbot-install/mbot-web-app/setup/packages/app-skeleton /data/mbot/app-skeleton

# add settings-page to mbot
cd ~/tmp/mbot-install/mbot-web-app/setup/packages/settings-page
mbot-cli install

# add drive-and-map-package to mbot
cd ~/tmp/mbot-install/mbot-web-app/setup/packages/drive-and-map-package
mbot-cli install

# add home-page to mbot
cd ~/tmp/mbot-install/mbot-web-app/setup/packages/home-page
mbot-cli install

sudo rm -r ~/tmp/mbot-install