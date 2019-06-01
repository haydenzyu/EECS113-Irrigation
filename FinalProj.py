#!/usr/bin/python
# Assignment 4 #

### import Python Modules ###
import threading
import RPi.GPIO as GPIO
import time
from datetime import datetime
import Freenove_DHT as DHT

thermoPin = 11  # pin for the thermo sensor
sensorPin = 13  # pin for the motion sensor

def setup():
    # setup the board input and output pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensorPin, GPIO.IN)

# main function to start program
if __name__ == '__main__':
    print("Program starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
