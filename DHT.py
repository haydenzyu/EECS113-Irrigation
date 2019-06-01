import time
import RPi.GPIO as GPIO
import Freenove_DHT as DHT

thermoPin = 11
localHumidity = 0
localTemp = 0
sqft = 200          # 200 square feet to be irrigated
pf = 1.0            # plant factor for lawn
conversion = 0.62   # constant conversion factor
IE = 0.75           # irrigation efficiency (suggested to use 0.75)
systemRate = 17     # 17 gallons per minute = 1020 gallons per hour

def getIrrigationTime():
    # get ET, humidity, and temp from CIMIS
    cimisHumidity = 
    cimisTemp = 
    cimisET = 

    # get humidty and temp derating factors 
    # get ET0 using these factors and CIMIS ET
    humidityDerate = localHumidity / cimisHumidity
    tempDerate = localTemp / cimisTemp
    ET0 = cimisET / (tempDerate * humidityDerate)

    # get gallons of water needed per hour (using gallons needed per day formula divided by 24)
    gallons = ((ET0 * pf * sqft *conversion) / IE) / 24
    
    # get time to run irrigation per hour
    irrigationTime = gallons / systemRate


def loop():
    dht = DHT.DHT(thermoPin)        # creates DHT class object
    count = 0

    while(True):
        if (localHumidity == 0 and localTemp == 0):
            localHumidity = dht.humidity
            localTemp = dht.temperature
        else:
            localHumidity = (localHumidity + dht.humidity)/2
            localTemp = (localTemp + dht.temperature)/2

        # check CIMIS for new data
        # if there is new data for the hour
            getIrrigationTime()
            localHumidity = 0
            localTemp = 0
        
        time.sleep(60)