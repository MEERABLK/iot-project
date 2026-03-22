# index.py
import os
from dotenv import load_dotenv

load_dotenv()

from scripts.controller import Controller
import time

controller = Controller()
controller.start()

while True:
    print("Fridge1 Temp:", controller.get_fridge1_temp())
    print("Fridge1 Hum:", controller.get_fridge1_humidity())
    print("Fridge2 Temp:", controller.get_fridge2_temp())
    print("Fridge2 Hum:", controller.get_fridge2_humidity())
    print("------")

    time.sleep(2)