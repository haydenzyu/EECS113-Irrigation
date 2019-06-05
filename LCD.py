#!/usr/bin/env python3
########################################################################
# Filename    : LCD.py
# Description : Use the LCD display data
# Author      : Hayden Yu
# modification: 6/2/19
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime
import threading
import DHT
import Relay
 
def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S\n')
    
def loop():
    #print("hi")
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):         
        lcd.clear()
        lcd.setCursor(0,0)  # set cursor position
        lcd.message( 'CPU: ' + get_cpu_temp()+'\n' )# display CPU temperature
        lcd.message( get_time_now() )   # display the time
        sleep(1)	
	
def display_cimis():#local_temp, local_hum, c_temp, c_hum, local_ET, cimis_ET, water_saving, addi_water):
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    mode = None
    sleep(1) #wait for DHT thread to start
    while True:
#Create strings for the variables
        #print(Relay.output)
        if(Relay.output==False):
            mode = 'On'
        else:
            mode = 'Off'
        relay_str = 'Water: ' + mode + ' '
        local_temp_str = 'Local Temp: ' + str(DHT.localTemp) + ' '
        local_hum_str = 'Local Humidity: ' + str(DHT.localHumidity) + ' '
        c_temp_str = 'CIMIS Temp: ' + str(DHT.cimisTemp) + ' '
        c_hum_str = 'CIMIS Humidity: ' + str(DHT.cimisHumidity) + ' '
        local_ET_str = 'Local ET:' + str(DHT.ET0) + ' '
        cimis_ET_str = 'CIMIS ET:' + str(DHT.cimisET) + ' '
        water_saving_str = 'Water Saved: ' + str(0) + ' '
        addi_water_str = 'Additional Water Used: ' + str(0) + ' '
        #print(DHT.display)
        top_line = relay_str + local_temp_str + local_hum_str #concatenate strings for top line on LCD
        if(DHT.ET0>0 or DHT.cimisET>0):
            bot_line = c_temp_str + c_hum_str + local_ET_str + cimis_ET_str + water_saving_str + addi_water_str #concatenate strings for bottom line on LCD
            while DHT.display:
                lcd.setCursor(0,0) # cursor top line
                lcd.message(top_line[:16])
                lcd.setCursor(0,1) # cursor bottom line
                lcd.message(bot_line[:16])# display bottom line
                top_line = top_line[1:]+top_line[0]# send first char to last 
                bot_line = bot_line[1:]+bot_line[0]# send first char to last
                sleep(0.1)
        else:
            while DHT.display:
                lcd.setCursor(0,0) # cursor top line
                lcd.message(top_line[:16])
                top_line = top_line[1:]+top_line[0]# send first char to last 
                sleep(0.1)
                
        sleep(1) #DHT time buffer
#end of create strings
		
                
def destroy():
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

