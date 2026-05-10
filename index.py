# index.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_socketio import SocketIO
import json

from scripts.controller import Controller
import scripts.gpio_controller as gpio
import db.database as data
import time
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

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

# load_dotenv(".env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fridges')
def fridges():
    # Fetch the latest sensor data from the controller
    sensor_data = controller.get_ambient_data()
    
    return render_template(
        'fridges.html',
        fridge1_temp=controller.get_fridge1_temp(),
        fridge1_humidity=controller.get_fridge1_humidity(),
        fridge2_temp=controller.get_fridge2_temp(),
        fridge2_humidity=controller.get_fridge2_humidity(),
        fridge1_threshold=controller.thresholds["fridge1"],
        fridge2_threshold=controller.thresholds["fridge2"],
        
        # Add these lines to pass the MSP01 data to the HTML
        ambient_temp=sensor_data.get("temp", "N/A"),
        ambient_hum=sensor_data.get("hum", "N/A"),
        sensor_status=sensor_data.get("status", "Offline")
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
    sensor_data = get_msp01_context()

    f1_thresh = data.get_threshold("fridge1")
    f2_thresh = data.get_threshold("fridge2")
    
    #Debug
    print(f"Syncing UI: F1 Thresh: {f1_thresh}, F2 Thresh: {f2_thresh}")
    
    return jsonify({
        "fridge1_temp": controller.get_fridge1_temp(),
        "fridge1_humidity": controller.get_fridge1_humidity(),
        "fridge1_threshold": f1_thresh,  # 👈 ADD THIS LINE
        
        "fridge2_temp": controller.get_fridge2_temp(),
        "fridge2_humidity": controller.get_fridge2_humidity(),
        "fridge2_threshold": f2_thresh,  # 👈 ADD THIS LINE
        
        "ambient_temp": sensor_data["temp"] if sensor_data else "N/A",
        "ambient_hum": sensor_data["hum"] if sensor_data else "N/A",
        "battery": sensor_data["battery"] if sensor_data else 0,
        "status": "Online" if sensor_data else "Offline"
    })

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/inventory-report')
def admin_inv_report():
    products = data.get_products()
    return render_template('admin_inv_report.html', products=products)

@app.route('/admin/sales-report')
def admin_sales_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    items = data.get_items_by_date(start_date, end_date)
    return render_template('admin_sales_report.html', items = items, start_date = start_date, end_date = end_date)

@app.route('/admin/customer-report')
def admin_customer_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    activity = data.get_customer_activity(start_date, end_date)
    return render_template('admin_customer_report.html', activity = activity, start_date = start_date, end_date = end_date)

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
        producer = req.get('producer')
        quantity = req.get('quantity')
        image = req.get('image')

        if not all([name, category, price, upc, producer, quantity]):
            return jsonify({"error": "Missing fields"}), 400

        success = data.add_product(name, category, price, upc, producer, quantity, image)

        if not success:
            return jsonify({"error": "Product name or UPC already exists"}), 400

        return jsonify({"message": "Product added"}), 201

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

       

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        req = request.get_json()

        success = data.update_product(
            id,
            req.get('name'),
            req.get('category'),
            req.get('price'),
            req.get('upc'),
            req.get('producer'),
            req.get('image')
        )

        if not success:
            return jsonify({"error": "Product update failed"}), 400

        return jsonify({"message": "Product updated"})

    except Exception as e:
        print("UPDATE ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/products/<int:id>/rfids', methods=['POST'])
def add_manual_rfid(id):
    try:
        req = request.get_json()
        epc = req.get("epc", "").strip()

        if not epc:
            return jsonify({"error": "Missing EPC"}), 400

        success = data.add_rfid_tag(id, epc)

        if not success:
            return jsonify({"error": "Could not add RFID. It may already exist."}), 400

        return jsonify({"message": "RFID added"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/products/<int:id>/rfids/<old_epc>', methods=['PUT'])
def update_rfid(id, old_epc):
    try:
        req = request.get_json()
        new_epc = req.get("epc", "").strip()

        if not new_epc:
            return jsonify({"error": "Missing new EPC"}), 400

        success = data.update_rfid_tag(id, old_epc, new_epc)

        if not success:
            return jsonify({"error": "Could not update RFID"}), 400

        return jsonify({"message": "RFID updated"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/products/<int:id>/rfids/<epc>', methods=['DELETE'])
def delete_rfid(id, epc):
    try:
        success = data.delete_rfid_tag(id, epc)

        if not success:
            return jsonify({"error": "Could not delete RFID"}), 400

        return jsonify({"message": "RFID deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/admin/stop-scan-tags', methods=['POST'])
def stop_scan_tags():
    controller.stop_admin_tag_assignment()
    return jsonify({"message": "Scan mode stopped"})

@app.route('/products/<int:id>/scan-next-tag', methods=['POST'])
def scan_next_tag(id):
    controller.start_admin_tag_assignment(id)
    return jsonify({"message": "Scan the RFID tag now"})



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

@app.route('/client/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 1. Capture form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 2. Call your new database function
        # (Assuming 'data' is your import for db.database)
        user = data.verify_user(email, password)
        
        if user:
            # 3. Success! Store user info in the session
            # We use 'customer_id' and 'email' based on your DB schema
            session['user_id'] = user.get('customer_id')
            session['user_email'] = user.get('email')
            session['user_name'] = user.get('name')
            
            print(f"Login successful for: {email}")
            flash(f"Welcome back, {user.get('name')}!", "success")
            return redirect(url_for('checkout')) 
        else:
            # 4. Failure! Stay on login page and show error
            print(f"Login failed for: {email}")
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for('login'))
        
    return render_template('client_login.html')
# def login():
#     return render_template('client_login.html')

@app.route('/client/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # Capture form data from the register page
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Here you would call your database function to save the user
        data.add_user(username, email, password)
        
        print(f"Registering new user: {email}")
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))
        
        if success:
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        else:
            flash("Error: Could not create account.", "danger")
            
    return render_template('client_register.html')

@app.route('/guest-checkout')
def guest_checkout():
    # Clear any old session data to ensure a fresh start
    session.clear()
    
    # Flag the session as a guest
    session['user_id'] = None
    session['is_guest'] = True
    session['user_name'] = "Guest User"
    
    # Redirect to your main shopping/checkout page
    return redirect(url_for('checkout'))

# def register():
#     return render_template('client_register.html')

# if __name__ == '__main__':
#     import threading

@app.route('/client/logout')
def logout():
    session.clear() # Removes user_id, user_email, etc.
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/api/cart')
def get_current_cart():
    # Retrieve the cart dictionary from the controller
    cart_data = controller.get_cart()
    
    # Transform it into a list that is easier for JavaScript to loop through
    formatted_cart = []
    for product_id, info in cart_data.items():
        formatted_cart.append({
            "id": product_id,
            "name": info['name'],
            "price": info['price'],
            "qty": info['qty'],
            "subtotal": info['price'] * info['qty']
        })
    
    return jsonify(formatted_cart)

import json # Ensure this is imported at the top

import json

@app.route('/client/history')
def client_receipt_history():
    customer_id = session.get('user_id', 1)
    
    receipts = data.get_receipt_history(customer_id)
    
    for receipt in receipts:
        receipt['items_json'] = json.dumps(receipt['lines'], default=str)
        
    return render_template('client_receipt_history.html', receipts=receipts)

@app.route('/api/complete-purchase', methods=['POST'])
def complete_purchase():
    try:
        data_req = request.get_json()
        customer_id = session.get('user_id', 1) 
        customer_email = data_req.get('email')

        current_points = data.get_user_points(customer_id)
        # 1000 points = 1% discount
        discount_percent = (current_points // 1000) * 0.01
        
        # Cap the discount at 50%
        if discount_percent > 0.50:
            discount_percent = 0.50

        # 1. Process Checkout (Decrements inventory in DB)
        receipt_id = controller.process_final_checkout(customer_id, discount_percent)
        
        if not receipt_id:
            return jsonify({"status": "error", "message": "Transaction failed"}), 400

        # 2. Check Inventory Thresholds
        threshold = 1
        low_stock_items = data.get_low_stock_items(threshold)
        
        # 3. 🔥 NEW: Trigger Admin Email Alert
        if low_stock_items:
            controller.notify_admin_low_stock(low_stock_items)

        # 4. Send Customer Receipt
        if customer_email:
            controller.send_receipt(customer_email)

        return jsonify({"status": "success", "receipt_id": receipt_id})

    except Exception as e:
        print(f"Checkout Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/user-info')
def get_user_info():
    # Get the logged-in user's ID from the session
    customer_id = session.get('user_id')
    
    if not customer_id:
        return jsonify({"points": 0, "logged_in": False})
    
    # Call the new database function
    points = data.get_user_points(customer_id)
    
    return jsonify({
        "points": points,
        "logged_in": True
    })

#     # Start controller in background thread
#     if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#         threading.Thread(target=controller.start, daemon=True).start()
    
#     socketio.run(app, debug=True)
@app.route('/api/barcode', methods=['POST'])
def scan_barcode():
    data_req = request.get_json()
    upc = data_req.get('upc')

    if not upc:
        return jsonify({"error": "No UPC provided"}), 400

    result = controller.add_by_barcode(upc)

    if "error" in result:
        return jsonify(result), 404

    return jsonify({"status": "added", "product": result})

@app.route('/products/<int:id>/assign-tags', methods=['POST'])
def assign_tags(id):
    # 'id' here is the product_id from the URL
    tags = controller.get_unknown_tags()
    
    if not tags:
        return jsonify({"error": "No tags detected by scanner"}), 400

    new_epc = tags[0] # Take the most recent unknown tag

    # Call the new function using product_id
    success = data.add_rfid_tag(id, new_epc)
    
    if success:
        controller.clear_unknown_tags()
        return jsonify({
            "status": "success",
            "message": f"Tag {new_epc} linked successfully!"
        })
    
    return jsonify({"error": "Could not link tag to database"}), 500

import requests

def get_msp01_context():
    url = "http://172.20.10.4:3001/context/device/c30000455da7/3"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            # Navigate the nested JSON structure
            device_data = data['devices']['c30000455da7/3']['dynamb']
            
            return {
                "temp": round(device_data.get('temperature'), 2),
                "hum": round(device_data.get('relativeHumidity'), 2),
                "lux": device_data.get('luminousFlux'),
                "battery": device_data.get('batteryPercentage')
            }
    except Exception as e:
        print(f"🚨 Context API Error: {e}")
    return None

if __name__ == '__main__':
    import threading

    # 1. Start the controller background threads
    # We remove the WERKZEUG_RUN_MAIN check and use use_reloader=False 
    # to ensure your hardware/RFID logic starts exactly once.
    threading.Thread(target=controller.start, daemon=True).start()
    
    # 2. Run the App
    # host='0.0.0.0' allows you to access the site via the Pi's IP address
    # use_reloader=False prevents the 405 errors caused by process duplication
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
