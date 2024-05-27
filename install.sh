#!/bin/bash -x

## Make sure we use the display of logged in user
export DISPLAY=:0
export HOME=$PWD
cd $HOME

## Prepare python env
sudo apt install virtualenv
virtualenv .env

## Start the virtual environment
VIRTUAL_ENV="$HOME/.venv"
export VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate

## Install python modules:
if [ -f requirements.txt ] 
then
    pip install -r requirements.txt
else
    echo "ERROR: Could not find required file"
    exit 10    
fi

## Define default config file for streamdeck
export STREAMDECK_UI_CONFIG="$HOME/streamdeck_ui_export.json"

