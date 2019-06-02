#!/usr/bin/python
# Assignment 4 #

### import Python Modules ###
import threading
import RPi.GPIO as GPIO
import time
from datetime import datetime
import DHT

thermoPin = 11  # pin for the thermo sensor
sensorPin = 13  # pin for the motion sensor

def setup():
    # setup the board input and output pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(sensorPin, GPIO.IN)

def loop():
    t = None
    print("starting DHT thread")
    t = threading.Thread(target=DHT.loop)
    t.daemon = True
    t.start()
    # DHT.loop()
    while(True):
        # if (DHT.irrigationTime != 0):
        #    print("Irrigation Time: %f", DHT.irrigationTime)
        time.sleep(10)

# main function to start program
if __name__ == '__main__':
    print("Program starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
