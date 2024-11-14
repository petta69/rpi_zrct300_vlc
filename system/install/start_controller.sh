#!/bin/bash -x

export CONTROLLER_HOME="REPLACE"

VIRTUAL_ENV="$CONTROLLER_HOME/.venv"
export VIRTUAL_ENV

## Make sure we use the display of logged in user
export DISPLAY=:0

## Turn off screensaver and blanking
xset -dpms
xset s off

## Define default config file for streamdeck
export STREAMDECK_UI_CONFIG="$CONTROLLER_HOME/streamdeck_ui_export.json"

## Start the virtual environment
source $VIRTUAL_ENV/bin/activate

cd $CONTROLLER_HOME



##
## Start the FastAPI server
##
python3 ./main.py


exit 0
