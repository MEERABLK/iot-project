# index.py
import os
from dotenv import load_dotenv

load_dotenv("credentials.env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

from scripts.controller import Controller
import time

controller = Controller()
#controller = Controller(email_address=EMAIL_ADDRESS, email_password=EMAIL_PASSWORD)

controller.start()
controller.data.fridge1Temperature = 10
controller.monitor_temperatures()
while True:
    print("Fridge1 Temp:", controller.get_fridge1_temp())
    print("Fridge1 Hum:", controller.get_fridge1_humidity())
    print("Fridge2 Temp:", controller.get_fridge2_temp())
    print("Fridge2 Hum:", controller.get_fridge2_humidity())
    print("------")

    time.sleep(2)