
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