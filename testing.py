import time
from scripts.controller import Controller

# 1. Initialize with dummy functions to prevent errors
ctrl = Controller(toggle_on=lambda x: None, toggle_off=lambda x: None)

# 2. Fire up the background threads
ctrl.start()

print("🛰️  Scanning... (CTRL+C to stop)")

try:
    while True:
        # 3. Pull the array directly from the controller
        tags = ctrl.get_latest_tags()
        
        if tags:
            print(f"Current Array: {tags}")
        
        time.sleep(0.5) # Fast polling for testing
except KeyboardInterrupt:
    print("\nTest finished.")