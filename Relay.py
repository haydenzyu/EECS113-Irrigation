import threading
import time
import RPi.GPIO as GPIO
import DHT
import SenseLED as PIR

relayPin = 15

systemState = False     # system initialized to off

def loop():
    global systemState

    runTime = DHT.irrigationTime*60
    
    t = None
    print("starting PIR thread")
    t = threading.Thread(target=PIR.loop)
    t.daemon = True
    t.start()

    #while(True):
    #    offTime = 60*(60 - DHT.irrigationTime)
        
    #    if (systemState):
    start = time.time()     # get the start time of irrigation

    GPIO.output(relayPin, GPIO.HIGH)
    # loop to keep irrigation on
    while (True):
        # if the motion sensor triggered, pause system run
        if (PIR.senvar == 1):
            # loop to wait 1 min or until motion no longer detected
            pauseStart = time.time()

            while(True):
                # break loop and resume irrigation if 1 min exceeded
                if ((time.time()-pauseStart) > 60):
                    GPIO.output(relayPin, GPIO.HIGH)
                    break
                # resume irrigation if motion no longer detected
                if (PIR.senvar == 0):
                    GPIO.output(relayPin, GPIO.HIGH)
                    break

                runTime += 1
                #offTime = offTime - 1
                time.sleep(1)

        # if irrigation pause over a minute, resume irrigating
        if ((time.time()-start) > runTime):
            GPIO.output(relayPin, GPIO.LOW)
            break
        
        time.sleep(1)        

        #time.sleep(offTime)

thermoPin = 11  # pin for the thermo sensor
ledPin = 12     # pin for motion LED
sensorPin = 16  # pin for the motion sensor
relayPin = 15

def setup():
    # setup the board input and output pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(sensorPin, GPIO.IN)
    GPIO.setup([relayPin, ledPin], GPIO.OUT)

def destroy():
    GPIO.output([relayPin, ledPin], GPIO.LOW)
    GPIO.cleanup()

# main function to start program
if __name__ == '__main__':
    global systemState
    print("Program starting...")
    setup()
    try:
        systemState = True
        loop()
    except KeyboardInterrupt:
        destroy()
        exit()
