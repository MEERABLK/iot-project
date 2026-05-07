# import time
# import json
# from scripts.controller import Controller

# # 1. Initialize Controller
# ctrl = Controller(toggle_on=lambda x: print(f"Fan {x} ON"), toggle_off=lambda x: print(f"Fan {x} OFF"))

# # 2. Start threads (MQTT, RFID, Barcode Listener)
# ctrl.start()

# print("🛰️  System Active. Scan RFID, type a Barcode, or type 'CHECKOUT' to finish.")

# last_cart = None

# try:
#     while True:
#         # 3. Get the current state of the cart
#         current_cart = ctrl.get_cart()

#         # 4. Only print if the cart content has changed
#         if current_cart != last_cart:
#             print("\n--- 🛒 UPDATED CART ---")
#             if not current_cart:
#                 print("Cart is empty.")
#             else:
#                 for pid, info in current_cart.items():
#                     source_icon = "📡" if info.get('source') == 'rfid' else "🏷️"
#                     print(f"{source_icon} {info['name']} | Qty: {info['qty']} | Price: ${info['price']} | Source: {info['source']}")
                
#                 # Calculate total locally for the test display
#                 total = sum(item['price'] * item['qty'] for item in current_cart.values())
#                 print(f"💰 TOTAL: ${total:.2f}")
            
#             last_cart = current_cart.copy()

#         # 5. Optional: Manual Trigger for Checkout test via terminal
#         # In a real scenario, this would be a button in your GUI.
#         # This is just for your internal testing logic.
        
#         time.sleep(0.2) 

# except KeyboardInterrupt:
#     print("\nTest finished.")
body = f"""
Attention Admin,
        
The following items have fallen below the inventory threshold after the last purchase:        
        
        
Please restock these items soon.
        
Best regards,
Smart Store System
        """
print(body)