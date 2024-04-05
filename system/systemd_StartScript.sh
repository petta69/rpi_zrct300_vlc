#!/bin/sh -x

##
## VLC
##

## Make sure we use the display of logged in user
export DISPLAY=:0

## Check we have vlc installed on the machine
VLC=$(which cvlc)
if $VLC == ""
then
    echo "ERROR: Could not find vlc"
    exit 10
fi

## Start vlc with telnet interface and make available for localhost
$VLC '--intf rc --rc-host 127.0.0.1:44500 &'


##
## Uvicorn (APIServer)
##

exit 0
