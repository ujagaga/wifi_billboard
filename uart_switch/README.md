# Uart Switch #

This is an Arduino project to add a scrool wheel and buttons to the display. The command is passed via UART at baud 115200.

I am using AtTiny85, but you could use any micro controller with at least 5 pins available (2 pins for scrool wheel, 2 pins for two buttons, plus 1 pin for UART TX).
My Digistump board has an LED connected to pin B1 and GND, so the buttons are connected to Vcc and using external pull down resistors. 
Alternatively, you can remove the LED and use internal pull up resistors.


## Contact ##

* web: http://www.radinaradionica.com
* email: ujagaga@gmail.com

