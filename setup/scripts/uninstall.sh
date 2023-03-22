sudo systemctl stop nginx
sudo systemctl stop mbotapi.service
sudo apt remove nginx --purge -y
sudo rm /etc/systemd/system/mbotapi.service
sudo rm -r /data/www/mbot
sudo rm -r /data/mbot
sudo rm /usr/local/bin/mbot-cli