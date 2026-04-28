# index.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
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

load_dotenv(".env")

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
        # epc = req.get('epc')
        producer = req.get('producer')
        quantity = req.get('quantity')
        image = req.get('image')

        if not all([name, category, price, upc, producer, quantity]):            return jsonify({"error": "Missing fields"}), 400

        data.add_product(name, category, price, upc, producer, quantity, image)

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

@app.route('/api/complete-purchase', methods=['POST'])
def complete_purchase():
    try:
        data_req = request.get_json()
        customer_id = session.get('user_id', 1) 
        customer_email = data_req.get('email')

        # 1. Get points and calculate discount percentage
        current_points = data.get_user_points(customer_id)
        # 1000 points = 0.01 (1%), 2000 = 0.02 (2%), etc.
        discount_percent = (current_points // 1000) * 0.01
        
        # Optional: Cap the discount at 50%
        if discount_percent > 0.50:
            discount_percent = 0.50

        # 2. Tell the controller to process with this discount
        # Note: You'll need to update your controller.py method to accept this!
        receipt_id = controller.process_final_checkout(customer_id, discount_percent)
        
        if not receipt_id:
            return jsonify({"status": "error", "message": "Transaction failed"}), 400

        # 3. Send email (the receipt logic we built earlier)
        if customer_email:
            controller.send_receipt(customer_email)

        return jsonify({
            "status": "success", 
            "message": f"Success! Applied {int(discount_percent*100)}% discount.",
            "receipt_id": receipt_id
        })

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
