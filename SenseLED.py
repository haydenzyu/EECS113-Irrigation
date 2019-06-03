import RPi.GPIO as GPIO

ledPin = 12
sensorPin = 16
senvar = 0

def setup():
    print('IR Program is starting...')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.setup(sensorPin, GPIO.IN)

def loop():
    global senvar

    while True:
        if GPIO.input(sensorPin) == GPIO.HIGH:
            GPIO.output(ledPin, GPIO.HIGH)
            senvar = 1
            #print(senvar)
        else:
            GPIO.output(ledPin, GPIO.LOW)
            senvar = 0
            #print(senvar)
        #print(senvar)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
                    
    
