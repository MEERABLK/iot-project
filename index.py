# index.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO

from scripts.controller import Controller
import scripts.gpio_controller as gpio
import db.database as data
import time

app = Flask(__name__)
app.secret_key = "iot_vanier_1"
socketio = SocketIO(app)

def toggle_on(id):
    socketio.emit(f'toggle{id}_updated', {'toggle_on': True})

def toggle_off(id):
    socketio.emit(f'toggle{id}_updated', {'toggle_on': False})

controller = Controller(toggle_on)

load_dotenv("credentials.env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fridges')
def fridges():
    # return render_template(
    #     'fridges.html'
    # )
    return render_template(
        'fridges.html',
        threshold=controller.threshold,
        fridge1_temp=controller.get_fridge1_temp(),
        fridge1_humidity=controller.get_fridge1_humidity(),
        fridge2_temp=controller.get_fridge2_temp(),
        fridge2_humidity=controller.get_fridge2_humidity()
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
    threshold = request.form.get('threshold', 'Bad value')

    try:
        data.set_threshold(f"fridge{fridge_id}", float(threshold))
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
    
    socketio.run(app, debug=True)
