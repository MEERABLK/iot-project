import tkinter as tk
from tkinter import messagebox
from db.database import add_customer
import validators

try:
    from hardware.gpio_controller import success, failure
except (ImportError, ModuleNotFoundError):
    def success(): print("Hardware: Blue LED ON")
    def failure(): print("Hardware: Red LED & Buzzer ON")

def handle_submit():
    first = entry_first.get().strip()
    last = entry_last.get().strip()
    email = entry_email.get().strip()
    phone = entry_phone.get().strip()
    address = entry_address.get().strip()
    city = entry_city.get().strip()
    province = entry_province.get().strip()
    postal_code = entry_postalcode.get().strip()


    if not first or not last or not email or not phone or not address or not city or not province or not postal_code :
        messagebox.showwarning("Input Error", "Please fill in the blanks")
        failure() 
        return
    if not validators.email(email):
        messagebox.showwarning("Input Error", "Please enter email format example abcd@gmail.com")
        failure() 
        return
    if add_customer(first, last, email,phone,address,province,city, postal_code):
        messagebox.showinfo("Success", f"Customer {first} added!")
        success() 
    else:
        messagebox.showerror("Error", "Database insertion failed.")
        failure() 

root = tk.Tk()
root.title("Vanier IoT - Phase 1")
root.geometry("800x800")

tk.Label(root, text="Customer Registration", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(root, text="First Name:").pack()
entry_first = tk.Entry(root)
entry_first.pack(pady=5)

tk.Label(root, text="Last Name:").pack()
entry_last = tk.Entry(root)
entry_last.pack(pady=5)

tk.Label(root, text="Email:").pack()
entry_email = tk.Entry(root)
entry_email.pack(pady=5)

tk.Label(root, text="Province:").pack()
entry_province = tk.Entry(root)
entry_province.pack(pady=5)

tk.Label(root, text="City:").pack()
entry_city = tk.Entry(root)
entry_city.pack(pady=5)

tk.Label(root, text="Address:").pack()
entry_address = tk.Entry(root)
entry_address.pack(pady=5)

tk.Label(root, text="Phone:").pack()
entry_phone = tk.Entry(root)
entry_phone.pack(pady=5)

tk.Label(root, text="Postal Code:").pack()
entry_postalcode = tk.Entry(root)
entry_postalcode.pack(pady=5)


btn_submit = tk.Button(root, text="Add Customer", command=handle_submit, bg="blue", fg="white")
btn_submit.pack(pady=20)

root.mainloop()