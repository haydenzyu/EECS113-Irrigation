#!/usr/bin/python
# Assignment 4 #

### import Python Modules ###
import threading
import RPi.GPIO as GPIO
import time
from datetime import datetime
import DHT
#import Relay
import LCD
import SenseLED

thermoPin = 11  # pin for the thermo sensor
sensorPin = 13  # pin for the motion sensor
relayPin = 15

def setup():
    # setup the board input and output pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(sensorPin, GPIO.IN)
    GPIO.setup(relayPin, GPIO.OUT)

def loop():
    t_DHT = None
    print("starting DHT thread")
    t_DHT = threading.Thread(target=DHT.loop)
    t_DHT.daemon = True
    t_DHT.start()
    t_relay = None
   # print("starting Relay thread")
   # t_relay = threading.Thread(target=Relay.loop)
   # t_relay.daemon = True
   # t_relay.start()
    print("starting LCD Thread")
    t_LCD = threading.Thread(target=LCD.display_cimis)
            #args=(DHT.localTemp[DHT.hour], DHT.localHumidity[DHT.hour], DHT.ET0, 
             #   DHT.cimisHumidity[DHT.hour], DHT.cimisTemp[DHT.hour], DHT.cimisET[DHT.hour], 0, 0))
    t_LCD.daemon = True
    t_LCD.start()
    # DHT.loop()
    while(True):
        # if (DHT.irrigationTime != 0):
        #    print("Irrigation Time: %f", DHT.irrigationTime)
        #print(DHT.localTemp[DHT.hour])
        time.sleep(0.1)

def destroy():
    GPIO.output(relayPin, GPIO.LOW)
    GPIO.cleanup()

# main function to start program
if __name__ == '__main__':
    print("Program starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        LCD.destroy()
        destroy()
        exit()
