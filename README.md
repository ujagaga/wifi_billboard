# WiFi Billboard

WiFi accessible billboard to display text via HDMI TV and talk to an AI chat bot. When there is something to write, 
this device will take over the HDMI display and output text in chromium web browser.

## Setting up the device

I am using "Orange Pi 5" as a multimedia device connected to my TV. This is convenient to display this billboard on TV.

Next steps:

1. Install v4l-utils so you have cec-ctl app to command HDMI:

       sudo apt install v4l-utils

2. To list HDMI devices:

       sudo cec-ctl --list-devices

    Please note the HDMI monitor/TV:
    - device ID (/dev/cec0)
    - Physical Address (1.0.0.0)
    - Logical Addresses (0)
3. To configure the HDMI monitor for first use:

       sudo cec-ctl -d/dev/cec0 --playback -S

4. To steal the HDMI TV focus, this app will use a command:

       cec-ctl -d/dev/cec0 -t0 --active-source phys-addr=1.0.0.0

    so please make sure the correct device parameters are set in "config.py"

5. To install this app as a service, just run the install.sh. To run it without installing, you will need to install dependencies:

       sudo apt -y install -y v4l-utils python3-fastapi uvicorn python3-selenium python3-webdriver-manager

On device, other than Orange pi 5, which might not have all these deb packages prepared, you might need to install 
a virtual environment and install packages like:

       VENV_PATH=venv
       python3 -m venv $VENV_PATH
       $VENV_PATH/bin/pip install fastapi selenium webdriver-manager

6. After this, if running as root, run your server like: 

       ./run.sh

If running as user, you can use ./run-dev.sh as it will run on port 8000 instead of 80
