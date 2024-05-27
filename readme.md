## Install Raspberry pi5 OS <br>
Install plain Raspberry pi5 OS following default instructions.<br>
After install:<br>
* open terminal<br>
* sudo raspi-config<br>
<br>
In raspi-config amke sure to set:<br>
"System Options" - "Boot/AutoLogin" -> "Desktop Autologin"<br>
"Interface Options" - "SSH" -> Activate SSH server<br>
"Performance Options" - "USB current" -> Disable USB limit<br>
"Advanced Options" - "Wayland" -> X11 This will change default desktop to X11 (Needed for HDR content)<br>
Finnish and reboot!<br>
<br>






Install python modules:
pip install -r requirements.txt

Start with gunicorn:
gunicorn --config gunicorn_config.py app:app


Streamdeck:
https://github.com/timothycrosley/streamdeck-ui

sudo apt install libhidapi-libusb0
PATH=$PATH:$HOME/.local/bin
python3 -m pip install --upgrade pip
sudo sh -c 'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fd9\", TAG+=\"uaccess\"" > /etc/udev/rules.d/70-streamdeck.rules'
sudo udevadm trigger
python3 -m pip install streamdeck-ui --user
