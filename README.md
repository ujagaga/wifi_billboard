# WiFi Billboard

WiFi accessible billboard to display text via HDMI TV and talk to an AI chat bot. When there is something to write, 
this device will take over the HDMI display and output text in chromium web browser.

## Setting up the device

I am using "Orange Pi 5" as a multimedia device connected to my TV. This is convenient to display this billboard on TV.

Next steps:

1. Install v4l-utils so you have cec-ctl app to command HDMI:

       sudo apt install v4l-utils

3. To list HDMI devices:

       sudo cec-ctl --list-devices

    Please note the HDMI monitor/TV:
    - device ID (/dev/cec0)
    - Physical Address (1.0.0.0)
    - Logical Addresses (0)
4. To configure the HDMI monitor for first use:

       sudo cec-ctl -d/dev/cec0 --playback -S

5. To steal the HDMI TV focus, this app will use a command:

       cec-ctl -d/dev/cec0 -t0 --active-source phys-addr=1.0.0.0

    so please make sure the correct device parameters are set in "config.py"



## NOTE

So far the billboard is working. Need to add AI interface.


