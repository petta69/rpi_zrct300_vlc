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

## Configure controller
Please update settings.json file with correct values for your installation<br>



