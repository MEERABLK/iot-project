# app.py
from db.database import add_customer
from hardware.gpio_controller import success, failure, cleanup
import time

result = add_customer("Melissa", "Smith", "melissa.smith@gmail.com")

if result:
    print("Customer added successfully!")
    success()
else:
    print("Insert failed.")
    failure()

time.sleep(2)
cleanup()