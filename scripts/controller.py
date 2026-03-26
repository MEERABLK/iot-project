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
        self.data = data
        self.email_address = EMAIL_ADDRESS 
        self.email_password = EMAIL_PASSWORD

        self.last_email_time = time.time()

        self.fridge1_alert_sent = False

        self.threshold = 8


    def start(self):
        # Start MQTT listener
        start_mqtt()

        # Start background logic (alerts, GPIO, etc.)
        threading.Thread(target=self._background_tasks, daemon=True).start()

    # def _background_tasks(self):
    #     while True:
    #         # Example: control GPIO based on temperature
    #         if self.data.fridge1Temperature is not None:
    #             if self.data.fridge1Temperature > 8:
    #                 # send alert
    #                 send_email.send_email(
    #                     subject="Fridge Alert 🚨",
    #                     body=f"Temp too high: {self.data.fridge1Temperature}. Would you like to turn on the fan?",
    #                     sender=EMAIL_ADDRESS,
    #                     recipients=[""],
    #                     password=EMAIL_PASSWORD
    #                 )

    #         time.sleep(5)
    def _background_tasks(self):
        threshold = 19

        while True:
            f1 = self.data.fridge1Temperature
            f2 = self.data.fridge2Temperature

            alert_triggered = False
            message = ""

            # Check both fridges
            if f1 is not None and f1 > threshold:
                alert_triggered = True
                message += f"Fridge 1: {f1}°C\n"

            if f2 is not None and f2 > threshold:
                alert_triggered = True
                message += f"Fridge 2: {f2}°C\n"

            # ===== SEND EMAIL ONCE =====
            if alert_triggered:
                if not self.fridge1_alert_sent:  # reuse one flag
                    send_email.send_email(
                        subject="Fridge Alert 🚨",
                        body=f"The following temperatures are too high:\n\n{message}\nReply YES to turn on the fan.",
                        sender=self.email_address,
                        recipients=["lowkeymischievous@gmail.com"],
                        password=self.email_password
                    )
                    self.fridge1_alert_sent = True
                    self.last_email_time = time.time()

                # ===== CHECK FOR REPLY =====
                elif send_email.check_reply_to_test_subject(self.email_address, self.email_password, self.last_email_time):
                    print("🔥 Turning ON fan")
                    gpio_controller.spinMotor()
                    time.sleep(5)
                    gpio_controller.stopMotor()

                    self.fridge1_alert_sent = False  # reset after action

            else:
                # Reset when everything is back to normal
                self.fridge1_alert_sent = False

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
            print(user_input)
            if user_input == "YES":
                print("Turning on fan...")
    
    
    def monitor_temperatures(self, recipient):
        fridge1_alert_sent = False
        fridge2_alert_sent = False

        while True:
            f1 = self.data.fridge1Temperature
            f2 = self.data.fridge2Temperature

            print("----- TEMPERATURE CHECK -----")

            # ===== FRIDGE 1 =====
            if f1 is not None:
                print(f"Fridge 1: {f1}°C")

                if f1 > self.threshold:
                    print("⚠️ Fridge 1 temperature too high!")

                    # Send email once
                    if not fridge1_alert_sent:
                        send_email.send_email(
                            subject="Fridge 1 Alert 🚨",
                            body=f"Fridge 1 temperature is {f1}°C.\nReply YES to turn on the fan.",
                            sender=self.email_address,
                            recipients=[recipient],
                            password=self.email_password
                        )
                        fridge1_alert_sent = True

                    # ✅ Check for YES reply
                    if send_email.check_reply_to_test_subject(self.email_address, self.email_password):
                        print("🔥 Turning ON fan for Fridge 1")
                        gpio_controller.spinMotor()
                        time.sleep(5)
                        gpio_controller.stopMotor()

                        fridge1_alert_sent = False  # reset after action

                else:
                    fridge1_alert_sent = False

            else:
                print("Fridge 1: No data")

            # ===== FRIDGE 2 =====
            if f2 is not None:
                print(f"Fridge 2: {f2}°C")

                if f2 > self.threshold:
                    print("⚠️ Fridge 2 temperature too high!")

                    # Send email once
                    if not fridge2_alert_sent:
                        send_email.send_email(
                            subject="Fridge 2 Alert 🚨",
                            body=f"Fridge 2 temperature is {f2}°C.\nReply YES to turn on the fan.",
                            sender=self.email_address,
                            recipients=["lowkeymischievous@gmail.com"],
                            password=self.email_password
                        )
                        fridge2_alert_sent = True

                    # ✅ Check for YES reply
                    if send_email.check_reply_to_test_subject(self.email_address, self.email_password):
                        print("🔥 Turning ON fan for Fridge 2")
                        gpio_controller.spinMotor()
                        time.sleep(5)
                        gpio_controller.stopMotor()

                        fridge2_alert_sent = False  # reset after action

                else:
                    fridge2_alert_sent = False

            else:
                print("Fridge 2: No data")

            print("-----------------------------\n")

            time.sleep(5)