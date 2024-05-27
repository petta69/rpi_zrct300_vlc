#!/bin/bash -x

## Make sure we use the display of logged in user
export DISPLAY=:0
export CONTROLLER_HOME=$PWD
cd $CONTROLLER_HOME

## Prepare python env
sudo apt install virtualenv
virtualenv .venv

## Start the virtual environment
VIRTUAL_ENV="$CONTROLLER_HOME/.venv"
export VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate

## Install python modules:
python3 -m pip install --upgrade pip
if [ -f requirements.txt ] 
then
    python3 -m pip install -r requirements.txt
else
    echo "ERROR: Could not find required file"
    exit 10    
fi

## Streamdeck
sudo apt install libhidapi-libusb0 libxcb-cursor0
PATH=$PATH:$HOME/.local/bin
sudo sh -c 'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fd9\", TAG+=\"uaccess\"" > /etc/udev/rules.d/70-streamdeck.rules'
sudo udevadm trigger
python3 -m pip install streamdeck-ui


## Define default config file for streamdeck
export STREAMDECK_UI_CONFIG="$CONTROLLER_HOME/streamdeck_ui_export.json"

## Set correct CONTROLLER_HOME variable in startup script
cd $CONTROLLER_HOME
if [ -f start_controller.sh ]
then
    sed -i "s|REPLACE|$CONTROLLER_HOME|g" start_controller.sh
fi
## Same thing for the service script
USER=$USER
if [ -f system/rpi_xrct300_vlc.service ]
then
    sed -i "s|USER|$USER|g" rpi_zrct300_vlc.service
    sed -i "s|REPLACE|$CONTROLLER_HOME|g" rpi_zrct300_vlc.service
fi

sudo ln -s $CONTROLLER_HOME/system/rpi_zrct300_vlc.service /lib/systemd/system/rpi_zrct300_vlc.service
sudo systemctl daemon-reload
sudo systemctl enable rpi_zrct300_vlc
sudo systemctl restart rpi_zrct300_vlc

exit 0
