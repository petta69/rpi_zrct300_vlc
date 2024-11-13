#!/bin/bash -x

## Make sure we use the display of logged in user
export DISPLAY=:0
export CONTROLLER_HOME=$PWD
cd $CONTROLLER_HOME

RSYNC=/usr/bin/rsync

## Turn off screensaver and blanking
xset -dpms
xset s off

## First make sure system is up to date
sudo apt update && sudo apt -y upgrade && sudo apt -y autoremove

## Prepare python env
sudo apt -y install virtualenv
virtualenv .venv

## Start the virtual environment
VIRTUAL_ENV="$CONTROLLER_HOME/.venv"
export VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate

## Copy our streamdeck setting file
file="streamdeck_ui_export.json"
org_linecount=$(wc -l $file | cut -f1 -d\ )
$RSYNC -av $file /tmp/

## Update git
/usr/bin/git pull

## Check if we have updated streamdeck settings
new_linecount=$(wc -l $file | cut -f1 -d\ )
if [ $new_linecount -ne $org_linecount ]; then
    $RSYNC -av /tmp/$file .
fi
python3 correct_streamdeckSerial.py

## Restart services to apply new files
systemctl --user restart streamdeck.service
systemctl --user restart rpi_zrct300_vlc.service

echo ""
echo "Update complete...."
echo ""

exit 0
