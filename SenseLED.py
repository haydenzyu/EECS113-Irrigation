import RPi.GPIO as GPIO
import time

ledPin = 12
sensorPin = 16
senvar = 0
start = True

def setup():
    print('IR Program is starting...')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.setup(sensorPin, GPIO.IN)

def loop():
    global senvar

    while start:
        i = GPIO.input(sensorPin)
        if i == GPIO.HIGH:
            GPIO.output(ledPin, GPIO.HIGH)
            senvar = 1
            #print(senvar)
        elif i == GPIO.LOW:
            GPIO.output(ledPin, GPIO.LOW)
            senvar = 0
            #print(senvar)
        #print(senvar)
        time.sleep(0.1)
    GPIO.output(ledPin, GPIO.LOW)
    senvar = 0
    return

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
                    
    
