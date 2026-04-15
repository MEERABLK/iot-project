from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import Device

# Set the pin factory to Mock AND enable PWM support
Device.pin_factory = MockFactory(pin_class=MockPWMPin)

# Now your imports will work
from gpiozero import LED, Buzzer, Motor
from time import sleep

# Change one of these to an unused GPIO pin
success_led = LED(17) 
fail_led = LED(16)
buzzer = Buzzer(21)

# If the motor is actually on Pin 23 instead of 17:
fan = Motor(forward=27, backward=23, enable=22)

def success():
    success_led.on()
    sleep(1)
    success_led.off()

def failure():
    print("Failure detected!")
    fail_led.on()
    buzzer.on()
    print("Buzzer On")
    sleep(1)
    fail_led.off()
    buzzer.off()
    print("Buzzer Off")

def spin_motor():
    print("Turning on fan")
    fan.forward() # Sets 27 High, 17 Low, and 22 High

def stop_motor():
    print("Stopping fan")
    fan.stop() # Sets all motor pins Low

def cleanup():
    # gpiozero handles cleanup automatically when the script exits,
    # but you can manually close devices if needed.
    success_led.close()
    fail_led.close()
    buzzer.close()
    fan.close()
