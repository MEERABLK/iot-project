import RPi.GPIO as GPIO
import time

    
#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

successLed = 17
failLed = 16
buzzer = 21
Motor1 = 22 # Enable Pin
Motor2 = 27 # Input Pin
Motor3 = 17 # Input Pin



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

def spinMotor():
    print("Turning on fan")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Motor1,GPIO.OUT)
    GPIO.setup(Motor2,GPIO.OUT)
    GPIO.setup(Motor3,GPIO.OUT)
    GPIO.output(Motor1,GPIO.HIGH)
    GPIO.output(Motor2,GPIO.HIGH)
    GPIO.output(Motor3,GPIO.LOW)

def stopMotor():
    print("Stopping fan")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.output(Motor1,GPIO.LOW)
    GPIO.output(Motor2,GPIO.LOW)
    GPIO.output(Motor3,GPIO.LOW)

def cleanup():
    GPIO.cleanup()

#success()
#time.sleep(2)
#failure()
# spinMotor()
# stopMotor()
GPIO.cleanup()