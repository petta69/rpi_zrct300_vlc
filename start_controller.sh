#!/bin/bash -x

## Make sure we use the display of logged in user
export DISPLAY=:0

export CONTROLLER_HOME=$PWD
VIRTUAL_ENV="$CONTROLLER_HOME/.venv"
export VIRTUAL_ENV
## Define default config file for streamdeck
export STREAMDECK_UI_CONFIG="$CONTROLLER_HOME/streamdeck_ui_export.json"

## Start the virtual environment
source $VIRTUAL_ENV/bin/activate

cd $CONTROLLER_HOME



##
## Streamdeck
##
python3 .venv/bin/streamdeck &




##
## Start the FastAPI server
##
python3 ./main.py


exit 0
