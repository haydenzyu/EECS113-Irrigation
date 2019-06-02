import time
import RPi.GPIO as GPIO
import DHT

relayPin = 15

systemState = False     # system initialized to off

def loop():

    while(True):
        
