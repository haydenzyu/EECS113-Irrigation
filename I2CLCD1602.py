#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime
 
def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):         
        #lcd.clear()
        lcd.setCursor(0,0)  # set cursor position
        lcd.message( 'CPU: ' + get_cpu_temp()+'\n' )# display CPU temperature
        lcd.message( get_time_now() )   # display the time
        sleep(1)
		
def display_temp_hum(tempurature, humidity):
	mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
	lcd.setCursor(0,0)  # set cursor to first row
	lcd.message( 'Tempurature: ' + temperature +'\n' )# display temperature
	lcd.setCursor(0,1) # set cursor to second row
    lcd.message( 'Humidity: ' + humidity + '\n' )   # display humidity
	
def display_cimis(temperature, humidity, local_ET, cimis_ET, water_saving, addi_water):
	mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
	temperature_str = 'CIMIS Tempurature: ' + temperature + ' '
	humidity_str = 'CIMIS Humidity: ' + humidity + ' '
	local_ET_str = 'Local ET:' + local_ET + ' '
	cimis_ET_str = 'CIMIST ET:' + cimis_ET + ' '
	water_saving_str = 'Water Saved: ' + water_saving + ' '
	addi_water_str = 'Additional Water Used: ' + addi_water + ' '
	top_line = #concatenate strings for top line on LCD
	bot_line = #concatenate strings for bottom line on LCD
	while True:
		lcd.setCursor(0,0)  # cursor top line
		lcd.message(top_line[:16])# display top line
		lcd.setCursor(0,1) # cursor bottom line
		lcd.message(bot_line[:16])# display bottom line
		top_line = top_line[1:]+top_line[0]# send first char to last 
		bot_line = bot_line[1:]+bot_line[0]# send first char to last testing git
		
		
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

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

