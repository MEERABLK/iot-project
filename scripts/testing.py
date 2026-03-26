import time
from sensor_data import data, start

start()

while True:
    print("Fridge1 Temp:", data.fridge1Temperature)
    print("Fridge1 Hum:", data.fridge1Humidity)
    print("Fridge2 Temp:", data.fridge2Temperature)
    print("Fridge2 Hum:", data.fridge2Humidity)
    print("------")
    time.sleep(2)