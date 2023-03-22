sudo systemctl stop nginx
sudo apt remove nginx --purge -y
sudo rm -r /data/www/mbot
sudo rm -r /data/mbot
sudo rm /usr/local/bin/mbot-cli