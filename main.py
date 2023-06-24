#Wazzas Thermal Buster v1.0 

import sys
import select
import machine
from machine import WDT
from PiicoDev_SSD1306 import *
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_RGB import PiicoDev_RGB
from PiicoDev_Buzzer import PiicoDev_Buzzer
from PiicoDev_CAP1203 import PiicoDev_CAP1203
from PiicoDev_Unified import sleep_ms

#wdt = WDT(timeout=5000)

sensor = PiicoDev_BME280() # initialise the sensor
display = create_PiicoDev_SSD1306() #init oled display
touchSensor = PiicoDev_CAP1203()

red = [255,0,0]
amber = [225,165,0]
green = [0,255,0]
tempC, presPa, humRH = sensor.values()
initTemp = tempC
tempC1 = initTemp
graph1 = display.graph2D(height=43, minValue=18, maxValue=22) # create graph2D objects
tempUp = 0
tempDn = 0 
led = machine.Pin('LED', machine.Pin.OUT) #configure LED Pin as an output pin
buzz = PiicoDev_Buzzer(volume=2)
buzz.pwrLED(False)
trafficA = PiicoDev_RGB()
trafficA.pwrLED(False)
statusBuzz = 0
xfactor = 0
f = 0 

#set xfactor
xfactor = initTemp -20
     
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

while True:
    # Print data main loop
    led.toggle()
    tempC, presPa, humRH = sensor.values() # read all data from the sensor
    pres_hPa = presPa / 100 # convert air pressurr Pascals -> hPa (or mbar, if you prefer)
    print(str(tempC)+" °C  " + str(pres_hPa)+" hPa  " + str(humRH)+" %RH")
   
    # check the buttons for Buzzer on/off
    status = touchSensor.read()
        
    if status[1] == 1:
        statusBuzz = 1
        buzz.tone(1500, 250)
    if status[2] == 1:
        statusBuzz = 2
        buzz.tone(300, 250)
    if status[3] == 1:
        statusBuzz = 0
        buzz.tone(100, 250)
     
    # traffic lights - green = temp going up, red = temp going down
    if tempC1 > tempC:
        trafficA.clear()
        trafficA.setPixel(2, red); trafficA.show()
        tempUp = 0
        tempDn = tempDn + 1
        if tempDn > 3 and statusBuzz == 1: # if temp increases 5 times in a row sound buzzer
            buzz.tone(300, 500)
    elif tempC1 == tempC:
        tempDn = 0
        tempUp = 0
        trafficA.clear()
        trafficA.setPixel(1, amber); trafficA.show();
    else:
        trafficA.clear()
        trafficA.setBrightness = 0
        trafficA.setPixel(0, green); trafficA.show()
        tempDn = 0
        tempUp = tempUp + 1
        if tempUp > 3 and statusBuzz >= 1: # if temp increases 5 times in a row sound buzzer
            buzz.tone(1500, 500)
   
    #OLED Display Text
    newtemp = str(tempC + 2)+"C"
    newpres = str(truncate(pres_hPa, 2))
    newRH = str(truncate(humRH, 2))+"RH"
    
    display.fill(0)
    display.text(newtemp, 0,0, 1) # print a variable
    display.text(newpres, 60,0, 1) # print a variable
    display.text(newRH, 0,10, 1) # print a variable
    
    # running diplay
    display.circ(65, 14, 4, f, 1) # un/filled circle
    f = not f
  
    #temp up, down, steady
    if tempDn > 0:
        display.text("vvv", 100, 10, 1)
    elif tempUp > 0:
        display.text("^^^", 100, 10, 1)
    else:
        display.text("---", 100, 10, 1)
        
    # OLED Graph display  
    y = tempC - xfactor
    
    #print(tempC, xfactor, initTemp, y)
    # reboot if out of range
    if y > 22 or y < 18:
        display.text("Temp > 2", 60, 40, 1)
        initTemp = tempC
        tempC1 = initTemp
        xfactor = initTemp -20   # break
    
    z = pres_hPa
    b = humRH
    tempC1 = tempC
    display.updateGraph2D(graph1, y)
    display.hline(0,20,128,1) # draw top line
    display.hline(0,63,128,1) # draw bottom line
    display.show()
    
    #press Enter to exit
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        trafficA.clear()
        display = create_PiicoDev_SSD1306()
        break
    
    sleep_ms(1000)
    #wdt.feed()
