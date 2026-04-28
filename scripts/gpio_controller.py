import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# L293D Pin Mapping
ENABLE_PIN = 22  # Connected to L293D Pin 1 (1,2EN)
INPUT1     = 27  # Connected to L293D Pin 2 (1A)
INPUT2     = 17  # Connected to L293D Pin 7 (2A)

# Feedback Pins (Moved successLed to avoid GPIO 17 conflict)
SUCCESS_LED = 23 
FAIL_LED    = 16
BUZZER      = 21

def init_gpio():
    """Run this once at start to prevent motor jitter"""
    pins = [ENABLE_PIN, INPUT1, INPUT2, SUCCESS_LED, FAIL_LED, BUZZER]
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def spinMotor():
    """Turns on the fan in a forward direction"""
    print("🌀 Fan: Starting (Forward)")
    GPIO.output(INPUT1, GPIO.HIGH)
    GPIO.output(INPUT2, GPIO.LOW)
    GPIO.output(ENABLE_PIN, GPIO.HIGH) # Enable the bridge

def stopMotor():
    """Cuts power to the motor immediately"""
    print("🛑 Fan: Stopping")
    # Setting Enable to LOW is the safest way to cut power on an L293D
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    GPIO.output(INPUT1, GPIO.LOW)
    GPIO.output(INPUT2, GPIO.LOW)

# Initialize on import
init_gpio()