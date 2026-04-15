# database.py
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()  # loads variables from .env

# from db.database import get_connection

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


def get_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database="smartstoreiotproject_db"
    )


def get_threshold(fridge_name):
    try:
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database="smartstoreiotproject_db"
        )

        mycursor = mydb.cursor()

        sql = "SELECT temperature_threshold FROM thresholds WHERE fridge_name = %s"
        mycursor.execute(sql, (fridge_name,))

        result = mycursor.fetchone()

        mycursor.close()
        mydb.close()

        if result:
            return result[0]  # return threshold value
        else:
            return None

    except mysql.connector.Error as err:
        print("Database Error:", err)
        return None
    
def set_threshold(fridge_name, threshold_value):
    mydb = None
    print(fridge_name, threshold_value)
    try:
        value = float(threshold_value)

        mydb = mysql.connector.connect(
           # host=db_host, user=db_user, password=db_password, database="store_db"
             host=db_host, user=db_user, password=db_password, database="smartstoreiotproject_db"
        )
        mycursor = mydb.cursor()

        sql = """
            INSERT INTO thresholds (fridge_name, temperature_threshold) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE temperature_threshold = %s
        """
        mycursor.execute(sql, (fridge_name, value, value)) # passing the value twice, one for insert case, one for update case

        mydb.commit()
        return True

    except (mysql.connector.Error, ValueError) as err:
        print(f"Error saving threshold: {err}")
        return False
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()
        
def add_customer(first, last, email, phone, address, city, province, postal_code):
    try:
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database="smartstoreiotproject_db"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO customers (first_name, last_name, email, phone, address, city, province, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (first, last, email, phone, address, city, province, postal_code)

        mycursor.execute(sql, values)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return True

    except mysql.connector.Error as err:
        print("Database Error:", err)
        return False


## Phase 2 products epc
def get_product_by_epc(epc):
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database="smartstoreiotproject_db"
    )

    cursor = mydb.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE EPC = %s", (epc,))
    result = cursor.fetchone()

    cursor.close()
    mydb.close()

    return result

# checkout function
def create_receipt(customer_id, cart):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database="smartstoreiotproject_db"
        )
        cursor = db.cursor()

        total = sum(item['price'] * item['qty'] for item in cart.values())
        points = int(total)  # simple system

        # Insert receipt
        cursor.execute(
            "INSERT INTO receipts (customer_id, total, points_earned) VALUES (%s, %s, %s)",
            (customer_id, total, points)
        )
        receipt_id = cursor.lastrowid

        # Insert items
        for pid, item in cart.items():
            cursor.execute(
                "INSERT INTO receipt_items (receipt_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (receipt_id, pid, item['qty'], item['price'])
            )

        db.commit()
        cursor.close()
        db.close()

        return receipt_id

    except Exception as e:
        print("Checkout Error:", e)
        return None

#inventory update 
def reduce_stock(product_id, qty):
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database="smartstoreiotproject_db"
    )
    cursor = db.cursor()

    cursor.execute(
        "UPDATE inventory SET quantity = quantity - %s WHERE product_id = %s",
        (qty, product_id)
    )

    db.commit()
    cursor.close()
    db.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results    

def add_product(name, category, price, upc, epc, producer, quantity, image):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products (name, category, price, upc, epc, producer, quantity, image)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (name, category, price, upc, epc, producer, quantity, image))

    conn.commit()
    cursor.close()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE product_id = %s",
        (product_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

def update_product(id, name, category, price, upc, epc, producer, quantity, image):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products 
        SET name=%s, category=%s, price=%s, upc=%s, epc=%s, quantity=%s, producer=%s, image=%s
        WHERE product_id=%s
    """, (name, category, price, upc, epc, quantity, producer, image, id))

    

    conn.commit()
    cursor.close()
    conn.close()