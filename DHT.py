#!/usr/bin/env python3
########################################################################
# Filename    : DHT.py
# Description : Use the DHT to get local humidity and temperature data
#               Use this data to calculate irrigation time
# Author      : Sienna Ballot
# modification: 6/3/19
########################################################################

import threading
import time
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import Relay
import csv
import CIMIS

thermoPin = 11
localHourly = []
localHumidity = 0.0
localTemp = 0.0
irrigationTime = 0.0
sqft = 200          # 200 square feet to be irrigated
pf = 1.0            # plant factor for lawn
conversion = 0.62   # constant conversion factor
IE = 0.75           # irrigation efficiency (suggested to use 0.75)
systemRate = 17     # 17 gallons per minute = 1020 gallons per hour
ET0 = 0             # variable for calculated ET0
cimisHumidity = 0   # variables to store the pulled CIMIS data
cimisTemp = 0
cimisET = 0
additionalWater = 0
waterSaved = 0

display = False     # to control LCD display
displaycimis = False

def getIrrigationTime():
    global irrigationTime
    global ET0
    global cimisET
    global cimisHumidity
    global cimisTemp
    global localHumidity
    global localTemp

    # get ET, humidity, and temp from CIMIS
    #cimisHumidity = 76 #[76, 71, 65]
    #cimisTemp = 61.3 #[61.3, 63.8, 66.8]
    #cimisET = 0.01 #[0.01, 0.02, 0.03]

    # get humidty and temp derating factors 
    # get ET0 for the 3 hours using these factors and CIMIS ET
    # for i in range(0, 2):
    #     humidityDerate = localHumidity[i] / cimisHumidity[i]
    #     tempDerate = localTemp[i] / cimisTemp[i]
    #     ET0 = ET0 + (cimisET[i] / (tempDerate * humidityDerate))
    
    # get date and hour to search for CIMIS data
    # format month for date string
    result = time.localtime(time.time())
    # if (result.tm_mon/10 == 0):                 
    #     month = '0'+str(result.tm_mon)
    # else:
    #     month = str(result.tm_mon)
    # # format day for date string
    # if (result.tm_mday/10 == 0):                
    #     day = '0'+str(result.tm_mday)
    # else:
    #     day = str(result.tm_mday)
    # # formulate date string and send as argument to CIMIS function
    # date = str(result.tm_year)+'-'+month+'-'+day
    
    CIMIS.getcimisdata(localHourly[0][0], localHourly[0][1])#result.tm_hour, date)

    if (not cimisET):
        cimisET = None
        cimisHumidity = None
        cimisTemp = None
        gallons = None
        irrigationTime = None
        additionalWater = 0
        waterSaved = 1020
    else:
        displaycimis = True
        while True:
            # get cimis data for the next hour in the list
            CIMIS.getHourData(localHourly[0][0], localHourly[0][1])
            #CIMIS.getcimisdata(localHourly[0][0], localHourly[0][1])
            # if the cimis has not been updated for that hour then break
            if (not cimisET or len(localHourly) == 0):
                break
        
            humidityDerate = cimisHumidity / localHourly[0][2]
            tempDerate = localHourly[0][3] / cimisTemp
            currET = cimisET * (tempDerate * humidityDerate)
            ET0 = ET0 + (cimisET * (tempDerate * humidityDerate))
            localHourly.remove(0)

        # get derating factors for humidity and temp and apply to the ET0 to get local average
        # humidityDerate = cimisHumidity / localHumidity
        # tempDerate = localTemp / cimisTemp
        # ET0 = cimisET * (tempDerate * humidityDerate)

        print("ET0: ", ET0)

        # get gallons of water needed per hour (using gallons needed per day formula divided by 24)
        gallons = ((ET0 * pf * sqft * conversion) / IE) / 24
        print("Gallons Total Needed: ", gallons)

        galHour = ((currET * pf * sqft * conversion) / IE) / 24
        print("Gallons for only this hour: ", galHour)

        # additional water is the total water needed minus the required water for that hour 
        additionalWater = gallons - galHour

        # water saved is the rate of water per hour minus the total water used
        waterSaved = 1020 - gallons

        # get time to run irrigation in minutes
        # gallons needed / (gallons per min) = minutes needed to run 
        irrigationTime = gallons / systemRate
        print("Irrigation Time (min): ", irrigationTime)

        # signal relay to turn on and start relay thread
        Relay.systemState = True
        t = None
        print("starting Relay/Motor thread")
        t = threading.Thread(target=Relay.loop)
        t.daemon = True
        t.start()

    # open output file to store information for the hour
    date = str(result.tm_mon)+'/'+str(result.tm_mday)+'/'+str(result.tm_year)
    #t = str(result.tm_hour)+':'+str(result.tm_min)+'.'+str(result.tm_sec)
    row = [date, str(tm_hour), str(ET0), str(localHumidity), str(localTemp), str(cimisET), str(cimisHumidity), str(cimisTemp), str(gallons), str(irrigationTime), str(additionalWater), str(waterSaved)]

    with open('output.csv', mode='a') as outputFile:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(row)

    outputFile.close()


def loop():
    global localHumidity
    global localTemp
    global display

    
    row = ['Date (MM/DD/YYYY)','Hour','Local ET0', 'Local Humidity', 'Local Temp(F)', 'CIMIS ET0', 'CIMIS Humidity', 'CIMIS Temp (F)', 'Gallons Needed (gal/hr)', 'Time Needed (min)', 'Additional Water (per hour)', 'Water Saved (per hour)']

    with open('output.csv', mode='a') as outputFile:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(row)

    outputFile.close()

    dht = DHT.DHT(thermoPin)        # creates DHT class object
    count = 0                       # initialize minute count for an hour

    while(True):
        chk = dht.readDHT11()
        print("Check DHT: ", chk)

        # CONVERT CELSIUS TO FAHRENHEIT
        if (chk is dht.DHTLIB_OK):
            # if the start of an hour, do not need to average 2 values
            if (localHumidity == 0 and localTemp == 0):
                localHumidity = dht.humidity
                localTemp = 32 + (1.8*dht.temperature)
            # otherwise avergae the new data with the past averages of the hour
            else:
                localHumidity = (localHumidity + dht.humidity)/2
                localTemp = (localTemp + (32+(1.8*dht.temperature)))/2
        
        count += 1
        print("Local Humidity: ", localHumidity)
        print("Local Temperature: ", localTemp)
        display = True #enable LCD to display
        
        # check CIMIS for new data
        # if there is new data for the hour
        result = time.localtime(time.time())
        if (count >= 5 or result.tm_min == 59):
            # format month for date string
            if (result.tm_mon/10 == 0):                 
                month = '0'+str(result.tm_mon)
            else:
                month = str(result.tm_mon)
            # format day for date string
            if (result.tm_mday/10 == 0):                
                day = '0'+str(result.tm_mday)
            else:
                day = str(result.tm_mday)
            # formulate date string and send as argument to CIMIS function
            date = str(result.tm_year)+'-'+month+'-'+day
            
            data = [result.tm_hour, date, localHumidity, localTemp]
            localHourly.append(data)

            getIrrigationTime()

            localHumidity = 0
            localTemp = 0
            count = 0
        
        # sleep for 1 minute
        time.sleep(60)
        display = False #disable LCD to display
        time.sleep(0.6)

