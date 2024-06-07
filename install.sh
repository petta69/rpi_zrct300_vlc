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


## Bootstrap (For the webserver part)
cd $CONTROLLER_HOME/static
wget https://github.com/twbs/bootstrap/releases/download/v5.3.3/bootstrap-5.3.3-dist.zip
bootstrap_file=$(find -type f -name "bootstrap*.zip")
unzip $bootstrap_file
bootstrap_dir=$(find -type d -name "bootstrap*")
ln -s $bootstrap_dir bootstrap


## Define default config file for streamdeck
export STREAMDECK_UI_CONFIG="$CONTROLLER_HOME/streamdeck_ui_export.json"

## Set correct CONTROLLER_HOME variable in startup script
cd $CONTROLLER_HOME
if [ -f start_controller.sh ]
then
    sed -i "s|REPLACE|$CONTROLLER_HOME|g" start_controller.sh
fi
if [ -f start_streamdeck.sh ]
then
    sed -i "s|REPLACE|$CONTROLLER_HOME|g" start_streamdeck.sh
fi

## Same thing for the service scripts
if [ -f system/streamdeck.service ]
then
    sed -i "s|REPLACE|$CONTROLLER_HOME|g" system/streamdeck.service
fi
if [ -f system/rpi_zrct300_vlc.service ]
then
    sed -i "s|REPLACE|$CONTROLLER_HOME|g" system/rpi_zrct300_vlc.service
fi


## Now prepare dir for user service script
if [ ! -d $HOME/.local/share/systemd/user/default.target ]
then
	mkdir -p $HOME/.local/share/systemd/user/default.target
fi

ln -s $CONTROLLER_HOME/system/rpi_zrct300_vlc.service $HOME/.local/share/systemd/user/default.target/rpi_zrct300_vlc.service
ln -s $CONTROLLER_HOME/system/streamdeck.service $HOME/.local/share/systemd/user/default.target/streamdeck.service
systemctl --user daemon-reload
systemctl --user enable streamdeck
systemctl --user enable rpi_zrct300_vlc
systemctl --user start streamdeck
systemctl --user start rpi_zrct300_vlc

echo ""
echo "INFO: Install is now complete. Please reboot and make sure everything is working as expected"
echo ""

exit 0

