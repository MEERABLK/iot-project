from flask import Flask, render_template, request, redirect, url_for, flash
from db.database import add_customer

try:
    from hardware.gpio_controller import success, failure
except (ImportError, ModuleNotFoundError):
    def success(): print("Hardware: Blue LED ON")
    def failure(): print("Hardware: Red LED & Buzzer ON")

app = Flask(__name__)
app.secret_key = "iot_vanier_1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_customer', methods=['POST'])
def handle_submit():
    first = request.form.get('first_name', '').strip()
    last = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    city = request.form.get('city', '').strip()
    province = request.form.get('province', '').strip()
    postal_code = request.form.get('postal_code', '').strip()

    if not first or not last or not email:
        flash("Please fill in all fields.", "warning")
        return redirect(url_for('index'))

    if add_customer(first, last, email, phone, address, city, province, postal_code):
        flash(f"Customer {first} added!", "success")
        success() 
    else:
        flash("Database insert failed.", "danger")
        failure() 

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
