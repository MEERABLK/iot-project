# controller.py
from unittest import result

from phase1_index import success
from scripts.sensor_data import data, start as start_mqtt
from scripts import gpio_controller
from scripts import send_email
# import index
import threading
import time
from dotenv import load_dotenv
import os
from db import database
from scripts.rfid_reader import get_rfid_tags
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

print("LOADED EMAIL:", EMAIL_ADDRESS)



class Controller:
    def __init__(self, toggle_on, toggle_off):
        # 📧 Email & Alert Configuration
        self.email_address = EMAIL_ADDRESS 
        self.email_password = EMAIL_PASSWORD
        self.last_email_time = time.time()
        self.fridge1_alert_sent = False
        self.checkout_locked = False
        # self.checkout_mode = False
        self.admin_scan_mode = False
        #  Sensor & Threshold Data
        self.admin_assign_product_id = None
        self.state = "SHOPPING"
        self.data = data
        self.thresholds = {
            "fridge1": 8,
            "fridge2": 8
        }

        self.msp01_data = {
            "temp": 0, 
            "hum": 0, 
            "battery": 0, 
            "status": "Offline"
        }

        # ⚙️ Hardware Controls
        self.toggle_on = toggle_on
        self.toggle_off = toggle_off
        self.lock = threading.Lock()

        # 🛰️ RFID & Cart Logic
        self.rfid_tags = []         # Current tags physically on the scanner
        # Scanned EPCs
        self.scanned_epcs = set()
        self.unknown_tags = [] # unknown tags to be used for adding epcs to the database
        self.cart_check_list = set() # 👈 ADDED: Tracks "active" tags to prevent double-scanning
        self.cart = {}              # Stores product info and quantities
        self.carts = {}             # For historical or multiple cart tracking
        self.last_receipt = None  # 👈 Initialized as None

    def start(self):
        # Start MQTT listener
        start_mqtt()

        # Start background logic (alerts, GPIO, etc.)
        threading.Thread(target=self._background_tasks, daemon=True).start()
        # Start RFID Logic 👈 NEW THREAD
        threading.Thread(target=self._rfid_background_task, daemon=True).start()
        # start barcode listener
        threading.Thread(target=self.barcode_listener, daemon=True).start()
    
    #===RFID==
    def _rfid_background_task(self):
        """Syncs the controller state and the cart with the physical scanner."""
        for current_tags in get_rfid_tags():
            
            if self.checkout_locked:
                time.sleep(0.5)
                continue

            with self.lock:
                self.rfid_tags = current_tags

            for tag_epc in current_tags:
                with self.lock:
                    admin_mode = self.admin_assign_product_id is not None

                if tag_epc in self.scanned_epcs and not admin_mode:
                    continue

                result = self._handle_tag(tag_epc)

                if result and "error" not in result:
                    self.scanned_epcs.add(tag_epc)

            # 2. REMOVAL: Handle tags no longer on the scanner
            for tag_epc in list(self.cart_check_list):
                if tag_epc not in current_tags:
                    self._handle_removal(tag_epc) 
                    self.cart_check_list.remove(tag_epc)
                    print(f"🗑️ Tag {tag_epc} removed from scanner & cart")

    #===core logic===
  
    def _handle_tag(self, tag_epc):
        try:
            with self.lock:
                assign_product_id = self.admin_assign_product_id
                admin_scan_mode = self.admin_scan_mode

        # 🔥 ADMIN MULTI-SCAN MODE
            if admin_scan_mode and assign_product_id is not None:
                success = database.add_rfid_tag(assign_product_id, tag_epc)

                if success:
                    print(f"Admin assigned RFID {tag_epc} to product {assign_product_id}")
                    return {"status": "admin_assigned", "epc": tag_epc}

                print(f"Admin failed to assign RFID {tag_epc}")
                return {"error": "admin_assign_failed", "epc": tag_epc}

        # 🔥 NORMAL SHOPPING MODE
            product = database.get_product_by_epc(tag_epc)

            if not product:
                print(f"⚠️ Unregistered tag detected: {tag_epc}")
                with self.lock:
                    if tag_epc not in self.unknown_tags:
                        self.unknown_tags.append(tag_epc)
                return {"error": "unknown_tag", "epc": tag_epc}

            pid = product.get('product_id')
            name = product.get('name')
            price = float(product.get('price', 0))

            with self.lock:
                if pid in self.cart:
                    self.cart[pid]['qty'] += 1
                else:
                    self.cart[pid] = {
                        "name": name,
                        "price": price,
                        "qty": 1
                    }

            print(f"Added {name} to cart")
            return product

        except Exception as e:
            print("Handle tag error:", e)
            return None
        
    def get_unknown_tags(self):
        """Returns the list of detected but unregistered tags."""
        return self.unknown_tags

    def clear_unknown_tags(self):
        """Clears the list after you've handled/registered them."""
        with self.lock:
            self.unknown_tags = []


    def start_admin_tag_assignment(self, product_id):
        with self.lock:
            self.admin_assign_product_id = product_id
            self.admin_scan_mode = True
            self.scanned_epcs.clear()
            self.unknown_tags.clear()

        print(f"ADMIN SCAN MODE ON for product {product_id}")

    def stop_admin_tag_assignment(self):
        with self.lock:
            self.admin_assign_product_id = None
            self.admin_scan_mode = False
            self.scanned_epcs.clear()

        print("ADMIN SCAN MODE OFF")
        
    def get_receipt(self, customer_id):
        """
        Finalizes transaction and stores the receipt details internally.
        """
        current_cart = self.get_cart()
        if not current_cart:
            print("🛒 Cannot create receipt: Cart is empty.")
            return None

        # 1. Save to DB
        receipt_id = database.create_receipt(customer_id, current_cart)

        if receipt_id:
            # 2. Fetch the finalized items from the DB
            receipt_items = database.get_receipt_items(receipt_id)
            
            # 3. Store the receipt internally so send_receipt() can access it
            self.last_receipt = {
                "receipt_id": receipt_id,
                "items": receipt_items,
                "customer_id": customer_id,
                "timestamp": time.time()
            }

            # 4. Clear local cart state
            with self.lock:
                self.cart = {}
                self.cart_check_list.clear()
                self.scanned_epcs.clear()
            print(f"📄 Receipt #{receipt_id} stored in controller memory.")
            return self.last_receipt
        
        return None

    def send_receipt(self, customer_email):
        """
        Sends the most recently stored receipt to the customer's email.
        """
        # 1. Check if a receipt exists in memory
        if not hasattr(self, 'last_receipt') or self.last_receipt is None:
            print("🚨 Error: No recent receipt found to send. Run get_receipt() first.")
            return

        receipt_data = self.last_receipt
        receipt_id = receipt_data['receipt_id']

        # 2. Build the email body
        body = f"Thank you for shopping at SmartStore IoT!\n"
        body += f"Receipt ID: #{receipt_id}\n"
        body += "-" * 35 + "\n"
        
        total_sum = 0
        for item in receipt_data['items']:
            name = item.get('name', f"Product {item['product_id']}")
            qty = item['quantity']
            price = item['price']
            subtotal = item['subtotal']
            total_sum += subtotal
            body += f"{name:<15} x{qty} @ ${price:.2f} = ${subtotal:.2f}\n"

        body += "-" * 35 + "\n"
        body += f"GRAND TOTAL: ${total_sum:.2f}\n"
        body += f"Points Earned: {int(total_sum)}\n\n"
        body += "We hope to see you again soon!"

        # 3. Send via existing send_email script
        try:
            print("Sending to:", customer_email)
            print("Sender:", self.email_address)
            print("Password exists:", self.email_password is not None)

            send_email.send_email(
                subject=f"Your SmartStore Receipt #{receipt_id}",
                body=body,
                sender=self.email_address,
                recipients=[customer_email],
                password=self.email_password
            )

            print("EMAIL SENT SUCCESS")

        except Exception as e:
            print("EMAIL FAILED:", str(e))

    # === Barcode Logic ===
    def add_by_barcode(self, upc):
       
        if self.checkout_locked:
            print("⛔ Barcode ignored (checkout locked)")
            return None
        """
        Manually adds an item to the cart using its barcode/UPC.
        """
        try:
            # 1. Fetch product using the UPC function in database.py
            product = database.get_product_by_upc(upc)

            if not product:
                print(f"⚠️ Unknown Barcode: {upc}")
                return {"error": "unknown_barcode", "upc": upc}

            pid = product.get('product_id')
            name = product.get('name', 'Unknown Product')
            price = float(product.get('price', 0.0))

            # 2. Update internal cart (Same logic as RFID)
            with self.lock:
                if pid in self.cart:
                    self.cart[pid]['qty'] += 1
                else:
                    self.cart[pid] = {
                        "name": name,
                        "price": price,
                        "qty": 1,
                        "category": product.get('category', 'General'),
                        "producer": product.get('producer', 'Unknown'),
                        "source": "barcode",  # 👈 New flag
                    }

            print(f"🏷️ Barcode Scanned: {name} (${price})")
            return product

        except Exception as e:
            print(f"🚨 Barcode Error: {str(e)}")
            return {"error": "system_error", "message": str(e)}
    
    def barcode_listener(controller_instance):
        while True:
            upc = input("Scan Barcode: ").strip()
            if upc:
                controller_instance.add_by_barcode(upc)

        

    def _handle_removal(self, tag_epc):
        """Decreases quantity or removes product from cart when EPC is lost."""
        try:
            # 1. Fetch product to find its product_id
            product = database.get_product_by_epc(tag_epc)
            if not product:
                return # Can't remove what we don't recognize

            pid = product.get('product_id')
            
            with self.lock:
                if pid in self.cart:
                    # 2. Logic: If multiple items of same ID exist, decrease qty
                    if self.cart[pid]['qty'] > 1:
                        self.cart[pid]['qty'] -= 1
                        print(f"➖ Decreased quantity for: {self.cart[pid]['name']}")
                    else:
                        # 3. Otherwise, remove the product entry entirely
                        removed_name = self.cart[pid]['name']
                        del self.cart[pid]
                        print(f"🗑️ Removed from cart: {removed_name}")
        
        except Exception as e:
            print(f"🚨 Error during removal of tag {tag_epc}: {e}")

    def _save_tag_to_db(self, tag_epc):
    # Helper to send data to your DB script.
    # Example: database_script.insert_tag(tag_epc, time.time())
        print(f"💾 Tag {tag_epc} saved to database.")

    # 👇 This is what Frontend / GUI should call
    def get_latest_tags(self):
        with self.lock:
            return list(self.rfid_tags) # Return a copy to be safe 
    
    def get_cart(self):
        # Returns the current cart dictionary containing all scanned products,their names, prices, and quantities.
        
        with self.lock:
            # We return a copy (dict()) so the frontend doesn't accidentally 
            # modify the live data used by the background threads.
            return dict(self.cart)
        

    
    
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
                        recipients=["jonathan.markovic@outlook.com"],
                        password=self.email_password
                    )
                    self.fridge1_alert_sent = True
                    self.last_email_time = time.time()

                # ===== CHECK FOR REPLY =====
                elif send_email.check_reply_to_test_subject(self.email_address, self.email_password, self.last_email_time):
                    print("🔥 Turning ON fan")
                    gpio_controller.spinMotor()
                    self.toggle_on(1)
                    self.toggle_on(2)
                    time.sleep(5)
                    gpio_controller.stopMotor()
                    self.toggle_off(1)
                    self.toggle_off(2)
                    

                    self.fridge1_alert_sent = False  # reset after action

            else:
                # Reset when everything is back to normal
                self.fridge1_alert_sent = False

            time.sleep(5)

    def get_ambient_data(self):
        with self.lock:
            print("bluetooth sensor")
            print(self.msp01_data)
            return self.msp01_data
        
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
                    recipients=["jonathan.markovic@outlook.com"],
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
                        self.toggle_on(1)
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
                            recipients=["jonathan.markovic@outlook.com"],
                            password=self.email_password
                        )
                        fridge2_alert_sent = True

                    # ✅ Check for YES reply
                    if send_email.check_reply_to_test_subject(self.email_address, self.email_password):
                        print("🔥 Turning ON fan for Fridge 2")
                        self.toggle_on(2)

                        fridge2_alert_sent = False  # reset after action

                else:
                    fridge2_alert_sent = False

            else:
                print("Fridge 2: No data")

            print("-----------------------------\n")

            time.sleep(5)
            # Get threshold for a specific fridge
    def get_threshold(self, fridge_name):
        return self.thresholds.get(fridge_name, 8)
    
    def set_threshold(self, fridge_name, value):
        """
        Updates the temperature threshold for a specific fridge in memory.
        :param fridge_name: 'fridge1' or 'fridge2'
        :param value: The new float value for the threshold
        """
        with self.lock:
            if fridge_name in self.thresholds:
                self.thresholds[fridge_name] = value
                print(f"✅ Memory Updated: {fridge_name} threshold set to {value}°C")
                
                # Reset alert flags so the system can alert again if the new 
                # threshold is immediately violated
                if fridge_name == "fridge1":
                    self.fridge1_alert_sent = False
            else:
                print(f"⚠️ Warning: {fridge_name} not found in thresholds dictionary.")

    def lock_checkout(self):
        print("🔒 CHECKOUT LOCKED - NO SCANS ALLOWED")
        self.checkout_locked = True

    def unlock_checkout(self):
        print("🔓 CHECKOUT UNLOCKED")
        self.checkout_locked = False

    def process_final_checkout(self, customer_id, discount_percent=0):

        self.lock_checkout()

        try:
            current_cart = self.get_cart()

            if not current_cart:
                return None

            receipt_id = database.create_receipt(
                customer_id,
                current_cart,
                discount_percent
            )

            if not receipt_id:
                return None

            receipt_items = database.get_receipt_items(receipt_id)

            self.last_receipt = {
                "receipt_id": receipt_id,
                "items": receipt_items,
                "customer_id": customer_id,
                "timestamp": time.time()
            }

            with self.lock:
                self.cart.clear()
                self.cart_check_list.clear()
                self.scanned_epcs.clear()

            return receipt_id

        finally:
            self.unlock_checkout()