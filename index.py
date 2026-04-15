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
    print("Toggling on")
    socketio.emit(f'toggle{id}_updated', {'toggle_on': True})

def toggle_off(id):
    print("Toggling off")
    socketio.emit(f'toggle{id}_updated', {'toggle_on': False})

controller = Controller(toggle_on, toggle_off)

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

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = data.get_all_products()  # must return list of dicts
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['POST'])
def add_product():
    try:
        req = request.get_json()

        name = req.get('name')
        category = req.get('category')
        price = req.get('price')
        upc = req.get('upc')
        epc = req.get('epc')
        producer = req.get('producer')
        quantity = req.get('quantity')
        image = req.get('image')

        if not all([name, category, price, upc, epc, producer, quantity]):
            return jsonify({"error": "Missing fields"}), 400

        data.add_product(name, category, price, upc, epc, producer, quantity, image)

        return jsonify({"message": "Product added"}), 201

    except Exception as e:
        print("ERROR:", e) 
        return jsonify({"error": str(e)}), 500

       

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        req = request.get_json()

        name = req.get('name')
        category = req.get('category')
        price = req.get('price')
        upc = req.get('upc')
        epc = req.get('epc')
        producer = req.get('producer')
        quantity = req.get('quantity')
        image = req.get('image')

        data.update_product(id, name, category, price, upc, epc, producer, quantity, image)

        return jsonify({"message": "Product updated"})

    except Exception as e:
        print("🔥 UPDATE ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        data.delete_product(id)
        return jsonify({"message": "Product deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/client')
def client_default():
    return redirect(url_for('login'))

@app.route('/client/login')
def login():
    return render_template('client_login.html')

@app.route('/client/register')
def register():
    return render_template('client_register.html')

if __name__ == '__main__':
    import threading

    
    # Start controller in background thread
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=controller.start, daemon=True).start()
    
    socketio.run(app, debug=True)
