# Piicodev-Temperature-Logger
First attempt a Pico programming 

You need a Raspberry Pi 4B to start with.

I purchased a PiicoDev starter Kit and a Raspberry Pi Pico. see links below.  

-Raspberry Pi Pico H (With Headers) - https://core-electronics.com.au/raspberry-pi-pico-h-with-headers.html
-PiicoDev Starter Kit for Raspberry Pi Pico - https://core-electronics.com.au/piicodev-starter-kit-for-raspberry-pi-pico.html

Next I read the following Guide:

PiicoDev OLED Module SSD1306 - Raspberry Pi Pico Guide - 
https://core-electronics.com.au/guides/raspberry-pi-pico/piicodev-oled-ssd1306-raspberry-pi-pico-guide/#download

Then I assembled the starter PiicoDev kit with the RP Pico plugged into the PiicoDev LiPo Expansion Board and connected the OLED Module, the Atmospheric sensor module, the Buzzer module, the RGB lights module and the capacitive tough sensor module on the PiccoDev platform. As per attached picture.

I then played with the example code to get the desired display with the temperature plotter, the traffic lights going green when the temp rises, amber when steady and red when falling. I also setup the buzzer to beep a high frequency note/tone when temp went up and lower note when temp went down, but my wife got annoyed by this so i progammed the touch buttons to control the sound on or off.

It worked really well and inspired me to build the smaller in field version "Wazza's Thermal Detector"

See pics and code. 
