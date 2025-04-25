#!/bin/bash -x

export CONTROLLER_HOME="REPLACE"

VIRTUAL_ENV="$CONTROLLER_HOME/.venv"
export VIRTUAL_ENV

## Make sure we use the display of logged in user
export DISPLAY=:0

## Turn off screensaver and blanking
xset -dpms
xset s off

## Start the virtual environment
source $VIRTUAL_ENV/bin/activate

cd $CONTROLLER_HOME



##
## Start the deconz Webhook app
##
python3 ./deconz_lightsensor.py


exit 0
