#!/usr/bin/python
# Assignment 4 #

### import Python Modules ###
import threading
import RPi.GPIO as GPIO
import time
from datetime import datetime
import DHT
import Relay

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
    print("starting DHT thread")
    t_relay = threading.Thread(target=Relay.loop)
    t_relay.daemon = True
    t_relay.start()
    # DHT.loop()
    while(True):
        # if (DHT.irrigationTime != 0):
        #    print("Irrigation Time: %f", DHT.irrigationTime)
        time.sleep(10)

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
        destroy()
        exit()
