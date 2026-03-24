# index.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

# from scripts.controller import Controller
import time

app = Flask(__name__)
app.secret_key = "iot_vanier_1"

load_dotenv("credentials.env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fridges')
def fridges():
    return render_template('fridges.html')

@app.route('/send_email', methods=['POST'])
def handle_send_email():
    email = request.form.get('email', '').strip()



    return redirect(url_for('fridges'))

if __name__ == '__main__':
    app.run(debug=True)

# controller = Controller()
# #controller = Controller(email_address=EMAIL_ADDRESS, email_password=EMAIL_PASSWORD)

# controller.start()
# controller.data.fridge1Temperature = 10
# controller.monitor_temperatures()
# while True:
#     print("Fridge1 Temp:", controller.get_fridge1_temp())
#     print("Fridge1 Hum:", controller.get_fridge1_humidity())
#     print("Fridge2 Temp:", controller.get_fridge2_temp())
#     print("Fridge2 Hum:", controller.get_fridge2_humidity())
#     print("------")

#     time.sleep(2)
