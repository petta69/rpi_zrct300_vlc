## Install Raspberry pi5 OS 
Install plain Raspberry pi5 OS following default instructions.
After install:
* open terminal
* sudo raspi-config

In raspi-config amke sure to set:
"System Options" - "Boot/AutoLogin" -> "Desktop Autologin"
"Interface Options" - "SSH" -> Activate SSH server
"Performance Options" - "USB current" -> Disable USB limit
"Advanced Options" - "Wayland" -> X11 This will change default desktop to X11 (Needed for HDR content)
Finnish and reboot!






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
