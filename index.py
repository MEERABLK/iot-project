# index.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from scripts.controller import Controller
import scripts.gpio_controller as gpio
import db.database as data
import time

controller = Controller()
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
    return render_template(
        'fridges.html',
        fridge1_temp=controller.get_fridge1_temp(),
        fridge1_humidity=controller.get_fridge1_humidity(),
        fridge2_temp=controller.get_fridge2_temp(),
        fridge2_humidity=controller.get_fridge2_humidity(),
        fridge1_threshold=controller.thresholds["fridge1"],  # fridge 1 threshold
        fridge2_threshold=controller.thresholds["fridge2"],  # fridge 2 threshold
    )
@app.route('/send_email', methods=['POST'])
def handle_send_email():
    email = request.form.get('email', '').strip()

    if email:
        controller.monitor_temperatures(email)
        flash("Email sent!", "mail success")
    else:
        flash("Invalid email", "mail error")       

    return redirect(url_for('fridges'))



@app.route('/set_threshold/<int:fridge_id>', methods=['POST'])
def handle_set_threshold(fridge_id):
    fridge_name = f"fridge{fridge_id}"
    threshold = request.form.get('threshold', 'Bad value')

    try:
        value = float(threshold)
        data.set_threshold(fridge_name, value)  # update DB
        controller.set_threshold(fridge_name, value)  # update controller memory

        flash("Threshold updated", f"temp{fridge_id} success")
    except (TypeError, ValueError):
        flash("Invalid value", f"temp{fridge_id} error") 

    return redirect(url_for('fridges'))

@app.route('/api/update-fan', methods=['POST'])
def handle_fan():
    data = request.get_json()

    if 'fridge1' in data :
        fridge1 = data.get('fridge1')

        if fridge1 is True :
            gpio.spinMotor()
        else :
            gpio.stopMotor()

    return jsonify({"status": "success"})

@app.route('/api/temps')
def get_temps():
    return jsonify({
        "fridge1_temp": controller.get_fridge1_temp(),
        "fridge1_humidity": controller.get_fridge1_humidity(),
        "fridge2_temp": controller.get_fridge2_temp(),
        "fridge2_humidity": controller.get_fridge2_humidity()
    })

if __name__ == '__main__':
    import threading

    
    # Start controller in background thread
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=controller.start, daemon=True).start()
    
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
