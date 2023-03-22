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
sudo mkdir -p /data/www/mbot/git/
sudo chmod -R a+rwx /data/www/mbot
sudo chmod -R a+rwx /data/mbot

echo "Setting up Nginx"
sudo rm /etc/nginx/nginx.conf
sudo cp ~/tmp/mbot-install/mbot-web-app/setup/config/nginx.conf /etc/nginx/nginx.conf

sudo systemctl restart nginx

# setup the mbot cli
sudo mkdir /data/mbot/cli
sudo cp ~/tmp/mbot-install/mbot-web-app/mbot-web-app-cli/*.py /data/mbot/cli
python3 -m pip install -r ~/tmp/mbot-install/mbot-web-app/mbot-web-app-cli/requirements.txt
sudo chmod a+x /data/mbot/cli/cli.py
sudo ln -s /data/mbot/cli/cli.py /usr/local/bin/mbot-cli

echo "Installed the mbot cli. Execute 'mbot-cli --help' for information on how to use it."

# add app-skeleton to mbot 
cd ~/tmp/mbot-install/mbot-web-app/setup/packages/app-skeleton
sudo cp -r * /data/www/mbot/app-skeleton

# add settings-page to mbot
cd ~/tmp/mbot-install/mbot-web-app/setup/packages/settings-page
mbot-cli install

# add drive-and-map-package to mbot
cd ~/tmp/mbot-install/mbot-web-app/setup/packages/drive-and-map-package
mbot-cli install

# add home-page to mbot
cd ~/tmp/mbot-install/mbot-web-app/setup/packages/home-page
mbot-cli install

# now we can setup the api
# The api is run by the mbot user, which we must create
# sudo useradd -r mbot # create a user without a home directory
sudo mkdir /data/www/mbot/api
sudo cp ~/tmp/mbot-install/mbot-web-app/setup/config/mbotapi.service /etc/systemd/system/mbotapi.service
sudo cp ~/tmp/mbot-install/mbot-web-app/api/*.py /data/www/mbot/api
sudo cp ~/tmp/mbot-install/mbot-web-app/api/requirements.txt /data/www/mbot/api
#sudo mkdir /home/mbot
#sudo chown mbot:mbot /home/mbot
#cd /data/www/mbot/api && python3 -m pip install -r requirements.txt
#sudo su mbot -c "cd /data/www/mbot/api && python3 -m pip install -r requirements.txt"
cd ~/tmp/mbot-install/mbot-web-app/api && python3 -m pip install -r requirements.txt
cd ~/tmp/mbot-install/mbot-web-app/setup/config
python3 generate_service_file.py
sudo cp mbotapi.service /etc/systemd/system/mbotapi.service

sudo systemctl daemon-reload
sudo systemctl enable mbotapi.service
sudo systemctl start mbotapi.service

sudo rm -r ~/tmp/mbot-install