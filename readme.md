## Install Raspberry pi5 OS <br>
Install plain Raspberry pi5 OS following default instructions.<br>
After install:<br>
* open terminal<br>
* sudo raspi-config<br>
<br>
In raspi-config make sure to set:<br>
"System Options" - "Boot/AutoLogin" -> "Desktop Autologin"<br>
"Interface Options" - "SSH" -> Activate SSH server<br>
"Performance Options" - "USB current" -> Disable USB limit<br>
"Advanced Options" - "Wayland" -> X11 This will change default desktop to X11 (Needed for HDR content)<br>
Finnish and reboot!<br>
<br>

## Install controller<br>
- Create directory for source code, "mkdir source"<br>
- Change into newly created dir, "cd source"<br>
- Clone source code by using https link for this repo, "git clone https://github.com/petta69/rpi_zrct300_vlc.git"<br>
- Change into new dir, "cd rpi_zrct300_vlc"<br>
- Start installation, "./install.sh"<br>
- Reboot!<br>

You will now have two parts installed:<br>
streamdeck<br>
rpi_zrct300_vlc<br>
<br>
Both of these are services and are controlled from the systemd interface.<br>
In order to check status for the streamdeck service you type(As your ordinary user):<br>
systemd --user status streamdeck<br>
<br>
And for the rpi_zrct300_vlc service:<br>
systemd --user status rpi_zrct300_vlc<br>
<br>
In order to restart one of the services you type (As your ordinary user)<br>
systemd --user restart <service><br>
<br>

## Configure controller
Please update settings.json file with correct values for your installation<br>


## Fixes
2024-06-07 Added bootstrap to install script (To be used offline). Updated VLC to start play without title.<br>

