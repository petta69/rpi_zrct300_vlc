## Install Raspberry pi5 OS <br>
Install plain Raspberry pi5 OS following default instructions.<br>
After install:<br>
* open terminal<br>
* sudo raspi-config<br>
<br>
In raspi-config make sure to set:<br>
"System Options" - "Boot/AutoLogin" -> "Desktop Autologin"<br>
"Interface Options" - "SSH" -> Activate SSH server<br>
"Interface Options" - "RPI connect" -> Activate "Remote shell access"<br>
"Performance Options" - "USB current" -> Disable USB limit<br>
"Advanced Options" - "Wayland" -> X11 This will change default desktop to X11 (Needed for HDR content)<br>
Finnish and reboot!<br>
<br>

## Install controller<br>
- First make sure you have your streamdeck panel connected<br>
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
systemctl --user status streamdeck<br>
<br>
And for the rpi_zrct300_vlc service:<br>
systemctl --user status rpi_zrct300_vlc<br>
<br>
In order to restart one of the services you type (As your ordinary user)<br>
systemctl --user restart <service><br>
<br>

## Configure controller
Start web browser and navigate to http://<ip address>:5000 and goto the settings tab.<br>
This will update the settings.json file with correct values for your installation<br>

## Raspberry Network Settings
In the upper right corner you can left-click on the network icon and select "Advanced network"<br>
Then select to edit. Select your wired interface and do the neccessary changes<br>

## Git updates
In the installation folder there is a script named "update.sh"<br>
Execute this by typing "./update.sh" and tit will update your rpi as well as the installation for you.

## Fixes
2024-12-16  Added Power schedule for the ZRCT-300 and have done many fixes.
2024-07-08  webUI: Added settings page. Updated status text for zrct-300 page.<br>
2024-06-28  Updated streamdeck layout. Added return text from controller to API. Added webUI for the ZRCT-300.
2024-06-18  Added missing input changes for DP/HDMI over ADCP. Updated installer to deal with serial number for<br>
            streamdeck panel.<br>
2024-06-07  Added bootstrap to install script (To be used offline). Updated VLC to start play without title.<br>
            Updated systemctl config<br>    

