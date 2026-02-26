import tkinter as tk
from tkinter import messagebox
from db.database import add_customer
import validators
from tkinter import ttk
import re

try:
    from hardware.gpio_controller import success, failure
except (ImportError, ModuleNotFoundError):
    def success(): print("Hardware: Blue LED ON")
    def failure(): print("Hardware: Red LED & Buzzer ON")

#regex functions
def valid_name(name):
    #isalpha will check if it is all aphabetic letters and a string
    #len counts element in string
    return name.isalpha() and len(name) >= 2


def valid_phone(phone):
    # accepts 5141234567 or 514-123-4567
    pattern = r"^\d{10}$"
    phone = phone.replace("-", "").replace(" ", "")
    return re.match(pattern, phone)


def valid_postal(postal):
    # canadian postal code format H1A1A1 or H1A 1A1
    pattern = r"^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$"
    return re.match(pattern, postal)


def valid_address(address):
    return len(address) >= 5


def valid_city(city):
    #checking cities with spaces and only letters Saint John becomes SaintJohn
    return city.replace(" ", "").isalpha()


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
    if not valid_name(first):
        messagebox.showerror("Error", "Invalid first name")
        failure()
        return


    if not valid_name(last):
        messagebox.showerror("Error", "Invalid last name")
        failure()
        return


    if not validators.email(email):
        messagebox.showerror("Error", "Invalid email")
        failure()
        return


    if not valid_phone(phone):
        messagebox.showerror("Error", "Phone must be 10 digits")
        failure()
        return


    if not valid_address(address):
        messagebox.showerror("Error", "Invalid address")
        failure()
        return


    if not valid_city(city):
        messagebox.showerror("Error", "Invalid city")
        failure()
        return


    if province == "Select Province":
        messagebox.showerror("Error", "Select a province")
        failure()
        return


    if not valid_postal(postal_code):
        messagebox.showerror("Error", "Invalid Canadian postal code")
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


provinces = ["Alberta", "British Columbia", "Manitoba", "New Brunswick",
    "Newfoundland and Labrador", "Nova Scotia", "Ontario",
    "Prince Edward Island", "Quebec", "Saskatchewan"];

tk.Label(root, text="Province:").pack()

entry_province = ttk.Combobox(root, values = provinces, state = "readonly")
entry_province.pack(pady=5)
entry_province.set("Select Province")

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