import threading
import time
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import Relay
import csv

thermoPin = 11
localHumidity = 0.0
localTemp = 0.0
hour = 0
irrigationTime = 0.0
sqft = 200          # 200 square feet to be irrigated
pf = 1.0            # plant factor for lawn
conversion = 0.62   # constant conversion factor
IE = 0.75           # irrigation efficiency (suggested to use 0.75)
systemRate = 17     # 17 gallons per minute = 1020 gallons per hour
ET0 = 0
cimisHumidity = 0
cimisTemp = 0
cimisET = 0

display = False

def getIrrigationTime():
    global irrigationTime
    global ET0
    global cimisET
    global cimisHumidity
    global cimisTemp

    # get ET, humidity, and temp from CIMIS
    cimisHumidity = 76 #[76, 71, 65]
    cimisTemp = 61.3 #[61.3, 63.8, 66.8]
    cimisET = 0.01 #[0.01, 0.02, 0.03]

    # get humidty and temp derating factors 
    # get ET0 for the 3 hours using these factors and CIMIS ET
    # for i in range(0, 2):
    #     humidityDerate = localHumidity[i] / cimisHumidity[i]
    #     tempDerate = localTemp[i] / cimisTemp[i]
    #     ET0 = ET0 + (cimisET[i] / (tempDerate * humidityDerate))

    humidityDerate = localHumidity / cimisHumidity
    tempDerate = localTemp / cimisTemp
    ET0 = cimisET * (tempDerate * humidityDerate)

    print("ET0: ", ET0)

    # get gallons of water needed per hour (using gallons needed per day formula divided by 24)
    gallons = ((ET0 * pf * sqft *conversion) / IE) / 24
    #gallons = 3 * gallons
    print("Gallons Needed: ", gallons)

    # get time to run irrigation in minutes
    irrigationTime = (gallons/60) / systemRate
    print("Irrigation Time: ", irrigationTime)

    # signal relay to turn on
    Relay.systemState = True
    t = None
    print("starting Relay/Motor thread")
    t = threading.Thread(target=Relay.loop)
    t.daemon = True
    t.start()

    # open file to write information

    row = ['Local ET0', 'Local Humidity', 'Local Temp (F)', 'CIMIS ET0', 'CIMIS Humidity', 'CIMIS Temp (F)']
    row2 = [str(ET0), str(localHumidity), str(localTemp), str(cimisET), str(cimisHumidity), str(cimisTemp)]
    row3 = ['Gallons Needed (gal/hr)', 'Time Needed (min)']
    row4 = [str(gallons), str(irrigationTime)]

    with open('output.csv', mode='a') as outputFile:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(time.ctime(time.time()))
        outputWriter.writerow(row)
        outputWriter.writerow(row2)
        outputWriter.writerow(row3)
        outputWriter.writerow(row4)


    outputFile.close()


def loop():
    global hour
    global localHumidity
    global localTemp
    global display

    row = ['Local ET0', 'Local Humidity', 'Local Temp', 'CIMIS ET0', 'CIMIS Humidity', 'CIMIS Temp']

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
        # check CIMIS for new data
        # if there is new data for the hour
        if (count == 1 and hour == 2):
            getIrrigationTime()

            # clear the past 3 hours of data
            # for i in range (0, 2):
            #     localHumidity[i] = 0
            #     localTemp[i] = 0
            localHumidity = 0
            localTemp = 0

        print("Local Humidity: ", localHumidity)
        print("Local Temperature: ", localTemp)
        
        display = True #enable LCD to display
        # sleep for 1 minute
        time.sleep(10)
        display = False #disable LCD to display
        time.sleep(0.6)

        if (count >= 3):
            count = 0
            hour = (hour + 1) % 3
