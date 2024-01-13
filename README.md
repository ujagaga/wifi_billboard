# WiFi Billboard

WiFi accessible billboard to display text via HDMI TV and talk to an AI chat bot. When there is something to write, 
this device will take over the HDMI display and output text in the main console.

## Setting up the device

I am using "Raspberry Pi Zero W" with "Raspbian Lite OS" installed. A convenience is that the pi user can execute sudo without password, 
so if using another linux environment, please note that this might differ. This is done by placing a text file like 
"/etc/sudoers.d/010_pi-nopasswd" with content:

       pi ALL=(ALL) NOPASSWD: ALL

Next steps:

1. Install Raspbian Lite to a micro SD card and setup WiFi connection
2. All the text will be written to the main console "/dev/tty0", so previewable on HDMI monitor. To setup console font, you can use:

       sudo dpkg-reconfigure console-setup

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

Just starting the project, so not yet usable


