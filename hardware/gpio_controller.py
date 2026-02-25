import RPi.GPIO as GPIO
import time

    
#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

successLed = 17
failLed = 16
buzzer = 21

def success():
    GPIO.setup(successLed, GPIO.OUT)
    GPIO.output(successLed, 1)
    time.sleep(1)
    GPIO.output(successLed, 0)
    

def failure():
    GPIO.setup(failLed, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)

    GPIO.output(failLed, 1)
    GPIO.output(buzzer, True)
    print("Failure detected!")
    print("Buzzer On")
    time.sleep(1)
    GPIO.output(failLed, 0)
    GPIO.output(buzzer, False)
    print("Buzzer Off")



def cleanup():
    GPIO.cleanup()

#success()
#time.sleep(2)
#failure()
#GPIO.cleanup()