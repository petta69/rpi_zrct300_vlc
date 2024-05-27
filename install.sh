#!/bin/bash -x

## Make sure we use the display of logged in user
export DISPLAY=:0

export HOME=$PWD
VIRTUAL_ENV="$HOME/.venv"
export VIRTUAL_ENV
## Define default config file for streamdeck
export STREAMDECK_UI_CONFIG="$HOME/streamdeck_ui_export.json"

## Start the virtual environment
source $VIRTUAL_ENV/bin/activate

cd $HOME

## Prepare python env
sudo apt install virtualenv

## Install python modules:
if [ -f requirements.txt ] 
then
    pip install -r requirements.txt
else
    echo "ERROR: Could not find required file"
    exit 10    
fi


