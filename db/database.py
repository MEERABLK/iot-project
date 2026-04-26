# database.py
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()  # loads variables from .env

print("DEBUG: Database file loaded successfully!")

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

# checkout function
def create_receipt(customer_id, cart, discount_percent=0.0):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database="smartstoreiotproject_db"
        )
        cursor = db.cursor()

        # Calculate totals
        raw_total = sum(item['price'] * item['qty'] for item in cart.values())
        final_total = raw_total * (1 - discount_percent)
        
        # Define the variable clearly here
        points_to_add = int(final_total) 

        # 1. Insert receipt
        cursor.execute(
            "INSERT INTO receipts (customer_id, total, points_earned) VALUES (%s, %s, %s)",
            (customer_id, final_total, points_to_add)
        )
        receipt_id = cursor.lastrowid

        # 2. Update customer's total points 
        # Use 'points_to_add' here so it matches the variable above!
        cursor.execute(
            "UPDATE customers SET points = points + %s WHERE customer_id = %s",
            (points_to_add, customer_id)
        )

        # 3. Insert items
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
        print("Checkout Error:", e) # This is where 'name points is not defined' was coming from
        return None

def get_user_points(customer_id):
    try:
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database="smartstoreiotproject_db"
        )
        cursor = mydb.cursor(dictionary=True)

        # Fetch only the points for this specific user
        query = "SELECT points FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        
        result = cursor.fetchone()

        cursor.close()
        mydb.close()

        # Return the points as an integer, default to 0 if user not found
        return result['points'] if result else 0

    except mysql.connector.Error as err:
        print(f"🚨 Database Error fetching points: {err}")
        return 0
          
def get_receipt_items(receipt_id):
    # Fetches all items associated with a specific receipt ID from the database.
    try:
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database="smartstoreiotproject_db"
        )
        cursor = mydb.cursor(dictionary=True)
        
        query = "SELECT item_id, receipt_id, product_id, quantity, price, subtotal FROM receipt_items WHERE receipt_id = %s"
        
        cursor.execute(query, (receipt_id,))
        results = cursor.fetchall()

        cursor.close()
        mydb.close()

        return results

    except mysql.connector.Error as err:
        print(f"🚨 Database Error fetching receipt items: {err}")
        return []   

def add_product(name, category, price, upc_code, epc, producer, quantity, image):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Insert into products (NO UPC/EPC HERE)
        cursor.execute("""
            INSERT INTO products (name, category, price, producer, image)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, category, price, producer, image))

        product_id = cursor.lastrowid  # 👈 IMPORTANT

        # 2. Insert UPC (barcode + quantity)
        cursor.execute("""
            INSERT INTO product_upc (product_id, upc_code, quantity)
            VALUES (%s, %s, %s)
        """, (product_id, upc_code, quantity))

        # 3. Insert RFID (EPC = one item)
        if epc:
            cursor.execute("""
                INSERT INTO product_rfid (product_id, epc_code)
                VALUES (%s, %s)
            """, (product_id, epc))

        conn.commit()

    except Exception as e:
        print("❌ Add product error:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

## Phase 2 products epc
def get_product_by_epc(epc):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.* 
        FROM products p
        JOIN product_rfid r ON p.product_id = r.product_id
        WHERE r.epc_code = %s
    """, (epc,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def get_product_by_id(product_id):
    """
    Fetches a single product and its associated UPC code by the product_id.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # We join with product_upc because assign_tags needs the 'upc' 
        # to link the new RFID tag.
        query = """
            SELECT p.*, u.upc_code as upc
            FROM products p
            LEFT JOIN product_upc u ON p.product_id = u.product_id
            WHERE p.product_id = %s
        """
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"🚨 Database Error in get_product_by_id: {e}")
        return None

## Phase 2 products upc
def get_product_by_upc(upc_code):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, u.quantity
        FROM products p
        JOIN product_upc u ON p.product_id = u.product_id
        WHERE u.upc_code = %s
    """, (upc_code,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

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


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 🔥 DELETE ALL DEPENDENCIES FIRST

        cursor.execute("DELETE FROM receipt_items WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM product_rfid WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM product_upc WHERE product_id = %s", (product_id,))

        # THEN delete product
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))

        conn.commit()

    except Exception as e:
        print("❌ Delete error:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def update_product(id, name, category, price, upc_code, epc, producer, quantity, image):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # update main product
        cursor.execute("""
            UPDATE products
            SET name=%s, category=%s, price=%s, producer=%s, image=%s
            WHERE product_id=%s
        """, (name, category, price, producer, image, id))

        # update UPC
        cursor.execute("""
            UPDATE product_upc
            SET upc_code=%s, quantity=%s
            WHERE product_id=%s
        """, (upc_code, quantity, id))

        # update EPC (only if needed)
        if epc:
            cursor.execute("""
                UPDATE product_rfid
                SET epc_code=%s
                WHERE product_id=%s
                LIMIT 1
            """, (epc, id))

        conn.commit()

    except Exception as e:
        print(" Update error:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def add_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers (username, email, password)
        VALUES (%s, %s, %s)
    """, (name, email, password))

    conn.commit()
    cursor.close()
    conn.close()

def verify_user(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM customers 
        WHERE email = %s AND password = %s
    """, (email, password))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user