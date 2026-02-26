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

    if not first or not last or not email:
        messagebox.showwarning("Input Error", "Please fill in First Name, Last Name, and Email.")
        return
    if not validators.email(email):
        messagebox.showwarning("Input Error", "Please enter email format example abcd@gmail.com")
        return
    if add_customer(first, last, email):
        messagebox.showinfo("Success", f"Customer {first} added!")
        success() 
    else:
        messagebox.showerror("Error", "Database insertion failed.")
        failure() 

root = tk.Tk()
root.title("Vanier IoT - Phase 1")
root.geometry("300x400")

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

btn_submit = tk.Button(root, text="Add Customer", command=handle_submit, bg="blue", fg="white")
btn_submit.pack(pady=20)

root.mainloop()