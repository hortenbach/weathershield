#!/bin/sh

# run this script to setup Donnerwetter weathershield on your RaspberryPi.
# usage:
# sudo ./install.sh

echo 'install Donnerwetter weathershield'
mkdir /opt/Donnerwetter
chmod -R u+x *
echo 'make dir /opt/weathershield ...'
cp -ar ../weathershield/ /opt/
echo 'cp contend from this folder into /opt/Donnerwetter ...'
cp /opt/weathershield/bash/weathershield_cron_hourly.sh /etc/cron.hourly/
cp ./bash/weathershield_cron_hourly.sh /etc/cron.hourly/
echo 'setting cronjob in /etc/cron.hourly ...'
