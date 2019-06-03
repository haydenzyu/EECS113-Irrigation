import threading
import time
import RPi.GPIO as GPIO
import DHT
import SenseLED as PIR

thermoPin = 11
ledPin = 12
sensorPin = 16
relayPin = 7
output = False          # system initialized to false

def loop():
    global output

    runTime = DHT.irrigationTime*60
    
    t = None
    print("starting PIR thread")
    t = threading.Thread(target=PIR.loop)
    t.daemon = True
    t.start()

    start = time.time()     # get the start time of irrigation

    output = False

    GPIO.output(relayPin, output)

    # loop to keep irrigation on
    print("Start irrigating")
    while (True):
        # if the motion sensor triggered, pause system run
        if (PIR.senvar == 1):
            print("Pause irrigation")
            output = True
            GPIO.output(relayPin, True)
            # loop to wait 1 min or until motion no longer detected
            pauseStart = time.time()

            while(True):
                # break loop and resume irrigation if 1 min exceeded
                if ((time.time()-pauseStart) > 60):
                    output = False
                    GPIO.output(relayPin, False)
                    break
                # resume irrigation if motion no longer detected
                if (PIR.senvar == 0):
                    output = False
                    GPIO.output(relayPin, False)
                    break

                runTime += 1
                #offTime = offTime - 1
                time.sleep(0.5)
            print("Resume Irrigation")

        # if irrigation pause over a minute, resume irrigating
        if ((time.time()-start) > runTime):
            output = True
            GPIO.output(relayPin, True)
            break
        
        time.sleep(0.5)        

    print("Stop irrigation")

def setup():
    # setup the board input and output pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(sensorPin, GPIO.IN)
    GPIO.setup(relayPin, GPIO.OUT)
    GPIO.setup(ledPin, GPIO.OUT)

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
