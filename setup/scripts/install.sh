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
sudo mkdir -p /data/mbot

# the directories for the mbot web application
sudo mkdir -p /data/mbot/app-skeleton/
sudo mkdir -p /data/mbot/packages/

# the directories for mbot git repositories
sudo mkdir -p /data/mbot/git/

sudo chmod -R a+rwx /data/mbot

echo "Setting up Nginx"
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/nginx.conf

sudo cp ~/tmp/mbot-install/mbot-web-app/setup/config/nginx.conf /etc/nginx/nginx.conf

# setup the mbot cli
sudo mkdir /data/mbot/cli
sudo cp ~/tmp/mbot-install/mbot-web-app-cli/*.py /data/mbot/cli
sudo python3 -m pip install -r ~/tmp/mbot-install/mbot-web-app-cli/requirements.txt
sudo chmod a+x /data/mbot/cli/cli.py
sudo ln -s /data/mbot/cli/cli.py /usr/local/bin/mbot-cli

echo "Installed the mbot cli. Execute 'mbot-cli --help' for information on how to use it."

# remove tmp directory
cd ~
rm -rf ~/tmp/mbot-install