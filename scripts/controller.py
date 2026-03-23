# controller.py

from scripts.sensor_data import data, start as start_mqtt
from scripts import gpio_controller
from scripts import send_email
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv("credentials.env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")




class Controller:
    def __init__(self):
        self.data = data  # shared sensor data
        self.email_sent = False 
        self.email_address = EMAIL_ADDRESS 
        self.email_password = EMAIL_PASSWORD
    def start(self):
        # Start MQTT listener
        start_mqtt()

        # Start background logic (alerts, GPIO, etc.)
        threading.Thread(target=self._background_tasks, daemon=True).start()

    def _background_tasks(self):
        while True:
            # Example: control GPIO based on temperature
            if self.data.fridge1Temperature is not None:
                if self.data.fridge1Temperature > 8:
                    # send alert
                    send_email.send_email(
                        subject="Fridge Alert 🚨",
                        body=f"Temp too high: {self.data.fridge1Temperature}. Would you like to turn on the fan?",
                        sender=EMAIL_ADDRESS,
                        recipients=["you@gmail.com"],
                        password=EMAIL_PASSWORD
                    )

            time.sleep(5)

    # 👇 functions GUI can call
    def get_fridge1_temp(self):
        return self.data.fridge1Temperature

    def get_fridge1_humidity(self):
        return self.data.fridge1Humidity

    def get_fridge2_temp(self):
        return self.data.fridge2Temperature

    def get_fridge2_humidity(self):
        return self.data.fridge2Humidity
    
    
    def check_fridge1_temperature(self, threshold=8):
        temp = self.data.fridge1Temperature
        if temp is not None and temp > threshold:
            if not self.email_sent:  # ✅ only send once
                subject = "Fridge Alert 🚨"
                body = f"The current temperature is {temp}°C. Would you like to turn on the fan?"
                send_email.send_email(
                    subject=subject,
                    body=body,
                    sender=self.email_address,
                    recipients=["lowkeymischievous@gmail.com"],
                    password=self.email_password
                )
                self.email_sent = True  # mark as sent

            # Wait for user input
            user_input = input("Reply YES to turn on fan: ").strip().upper()
            if user_input == "YES":
                print("Turning on fan...")
            else:
                print("No action taken.")
        else:
            self.email_sent = False