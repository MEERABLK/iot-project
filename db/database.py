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
        cursor = mydb.cursor()
        
        # We sort by ID descending to put the highest (newest) ID at the top
        query = """
            SELECT temperature_threshold 
            FROM thresholds 
            WHERE fridge_name = %s 
            ORDER BY id DESC 
            LIMIT 1
        """
        
        cursor.execute(query, (fridge_name,))
        result = cursor.fetchone()
        
        cursor.close()
        mydb.close()
        
        # If a result exists, return the float; otherwise, return the default 8.0
        return float(result[0]) if result else 8.0

    except Exception as e:
        print(f"🚨 Error fetching latest threshold for {fridge_name}: {e}")
        return 8.0
    
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
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        # ===============================
        # 1. CHECK STOCK FIRST
        # ===============================
        for pid, item in cart.items():

            cursor.execute("""
                SELECT quantity
                FROM inventory
                WHERE product_id = %s
            """, (pid,))

            stock = cursor.fetchone()

            if not stock:
                print(f"❌ Product {pid} not found in inventory")
                db.rollback()
                return None

            available = stock['quantity']

            if item['qty'] > available:
                print(f"❌ Not enough stock for product {pid}")
                db.rollback()
                return None

        # ===============================
        # 2. CALCULATE TOTAL
        # ===============================
        raw_total = sum(
            item['price'] * item['qty']
            for item in cart.values()
        )

        final_total = raw_total * (1 - discount_percent)

        points_to_add = int(final_total)

        # ===============================
        # 3. CREATE RECEIPT
        # ===============================
        cursor.execute("""
            INSERT INTO receipts
            (customer_id, total, points_earned)
            VALUES (%s, %s, %s)
        """, (
            customer_id,
            final_total,
            points_to_add
        ))

        receipt_id = cursor.lastrowid

        # ===============================
        # 4. UPDATE CUSTOMER POINTS
        # ===============================
        cursor.execute("""
            UPDATE customers
            SET points = points + %s
            WHERE customer_id = %s
        """, (
            points_to_add,
            customer_id
        ))

        # ===============================
        # 5. SAVE ITEMS + REDUCE STOCK + REMOVE RFID TAGS
        # ===============================
        for pid, item in cart.items():

            qty = item['qty']
            price = item['price']

            # receipt item
            cursor.execute("""
                INSERT INTO receipt_items
                (receipt_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (
                receipt_id,
                pid,
                qty,
                price
            ))

            # reduce inventory
            cursor.execute("""
                UPDATE inventory
                SET quantity = quantity - %s
                WHERE product_id = %s
            """, (
                qty,
                pid
            ))

            # get RFID tags to remove
            cursor.execute("""
                SELECT epc_code
                FROM product_rfid
                WHERE product_id = %s
                LIMIT %s
            """, (
                pid,
                qty
            ))

            tags = cursor.fetchall()

            # delete purchased RFID tags
            for tag in tags:
                cursor.execute("""
                    DELETE FROM product_rfid
                    WHERE epc_code = %s
                """, (
                    tag['epc_code'],
                ))

        db.commit()
        cursor.close()
        db.close()

        return receipt_id

    except Exception as e:
        print("Checkout Error:", e)
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
    
def get_receipt_history(customer_id):
    try:
        mydb = get_connection()
        cursor = mydb.cursor(dictionary=True)
        
        cursor.execute("SELECT receipt_id as id, total, points_earned, created_at as date, payment_method FROM receipts WHERE customer_id = %s", (customer_id,))
        info = cursor.fetchall()

        receipt_ids = [i['id'] for i in info]

        if not receipt_ids:
            return []
        
        ids_string = ','.join(['%s'] * len(receipt_ids))

        cursor.execute(f"SELECT r.receipt_id, p.name, r.quantity as qty, r.price, r.subtotal FROM receipt_items r INNER JOIN products p ON r.product_id = p.product_id WHERE r.receipt_id IN ({ids_string})", tuple(receipt_ids))
        all_lines = cursor.fetchall()

        cursor.close()
        mydb.close()

        receipt_map = {i['id']: i for i in info}

        for i_id in receipt_map:
            receipt_map[i_id]['lines'] = []

        for line in all_lines:
            r_id = line['receipt_id']
            if r_id in receipt_map:
                receipt_map[r_id]['lines'].append(line)

        receipt_list = list(receipt_map.values())

        for receipt in receipt_list:
            receipt['formatted_lines'] = []
            for line in receipt['lines']:
                f_line = f"{line['name'][:24]:<25} {line['qty']:>5} {line['price']:>10.2f} {line['subtotal']:>12.2f}"
                receipt['formatted_lines'].append(f_line)

        return receipt_list

    except mysql.connector.Error as err:
        print(f"🚨 Database Error fetching receipt history: {err}")
        return []

def get_products():
    try:
        mydb = get_connection()
        cursor = mydb.cursor(dictionary=True)
        
        query = "SELECT * FROM products"
        
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        mydb.close()

        return results

    except mysql.connector.Error as err:
        print(f"🚨 Database Error fetching products: {err}")
        return []
    
def get_items_by_date(start_date, end_date):
    try:
        mydb = get_connection()
        cursor = mydb.cursor(dictionary=True)
        
        query = "SELECT * FROM receipt_items WHERE 1 = 1"
        params = []

        if is_valid_date(start_date):
            query += " AND receipt_id IN (SELECT receipt_id FROM receipts WHERE created_at >= %s)"
            params.append(start_date)

        if is_valid_date(end_date):
            query += " AND receipt_id IN (SELECT receipt_id FROM receipts WHERE created_at <= %s)"
            params.append(end_date)
        
        cursor.execute(query, params)
        results = cursor.fetchall()

        cursor.close()
        mydb.close()

        return results

    except mysql.connector.Error as err:
        print(f"🚨 Database Error fetching items: {err}")
        return []
    
def get_customer_activity(start_date, end_date):
    try:
        mydb = get_connection()
        cursor = mydb.cursor(dictionary=True)
        
        # 1. Base query using a JOIN so we can see the receipt AND the customer account info
        query = """
            SELECT 
                COUNT(DISTINCT r.customer_id) AS active_customers,
                
                -- If their account was created during this window, they are New
                COUNT(DISTINCT CASE WHEN c.created_at >= %s THEN r.customer_id END) AS new_customers,
                
                -- If their account was created before this window, they are Returning
                COUNT(DISTINCT CASE WHEN c.created_at < %s THEN r.customer_id END) AS returning_customers

            FROM receipts r
            INNER JOIN customers c ON r.customer_id = c.customer_id
            WHERE 1=1
        """

        params = [start_date, start_date] # For the CASE statements

        # 2. Dynamically apply the date filter to the RECEIPTS (when the purchase happened)
        if is_valid_date(start_date):
            query += " AND r.created_at >= %s"
            params.append(start_date)

        if is_valid_date(end_date):
            query += " AND r.created_at <= %s"
            params.append(end_date)

        # 3. Execute exactly once
        cursor.execute(query, tuple(params))
        report = cursor.fetchone()

        # Now you have report['active_customers'], report['new_customers'], etc.

        cursor.close()
        mydb.close()

        return report

    except mysql.connector.Error as err:
        print(f"🚨 Database Error fetching items: {err}")
        return []

def add_product(name, category, price, upc_code, producer, quantity, image):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO products (name, category, price, producer, image)
            VALUES (%s,%s,%s,%s,%s)
        """, (name, category, price, producer, image))

        product_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO product_upc (product_id, upc_code)
            VALUES (%s,%s)
        """, (product_id, upc_code))

        cursor.execute("""
            INSERT INTO inventory (product_id, quantity)
            VALUES (%s,%s)
        """, (product_id, quantity))

        conn.commit()

    except Exception as e:
        print("add_product error:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def add_rfid_tag(product_id, epc):
    """
    Links a physical RFID tag (EPC) to a specific product using its product_id.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. (Optional) Check if this EPC already exists to prevent duplicate errors
        cursor.execute("SELECT * FROM product_rfid WHERE epc_code = %s", (epc,))
        if cursor.fetchone():
            print(f"⚠️ Tag {epc} is already registered to a product.")
            cursor.close()
            conn.close()
            return False

        # 2. Insert the new mapping
        sql = "INSERT INTO product_rfid (product_id, epc_code) VALUES (%s, %s)"
        cursor.execute(sql, (product_id, epc))

        conn.commit()
        print(f"✅ Successfully linked tag {epc} to product ID {product_id}")
        
        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        print(f"🚨 Database Error in add_rfid_tag: {err}")
        return False

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

def get_product_by_tag_epc(epc):
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

    cursor.execute("""
        SELECT
            p.product_id,
            p.name,
            p.category,
            p.price,
            p.producer,
            p.image,
            i.quantity,
            u.upc_code AS upc,
            COUNT(r.epc_code) AS rfid_count
        FROM products p
        LEFT JOIN inventory i ON p.product_id = i.product_id
        LEFT JOIN product_upc u ON p.product_id = u.product_id
        LEFT JOIN product_rfid r ON p.product_id = r.product_id
        GROUP BY p.product_id, u.upc_code
    """)

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
        # 1. update main product
        cursor.execute("""
            UPDATE products
            SET name=%s, category=%s, price=%s, producer=%s, image=%s
            WHERE product_id=%s
        """, (name, category, price, producer, image, id))

        # 2. update UPC (ONLY UPC)
        cursor.execute("""
            INSERT INTO product_upc (product_id, upc_code)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE upc_code = VALUES(upc_code)
        """, (id, upc_code))

        # 3. update inventory
        cursor.execute("""
            UPDATE inventory
            SET quantity=%s
            WHERE product_id=%s
        """, (quantity, id))

        # 4. update RFID (better: replace instead of update 1 row)
        if epc:
            cursor.execute("""
                DELETE FROM product_rfid WHERE product_id=%s
            """, (id,))

            cursor.execute("""
                INSERT INTO product_rfid (product_id, epc_code)
                VALUES (%s, %s)
            """, (id, epc))

        conn.commit()

    except Exception as e:
        print("UPDATE ERROR:", e)
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

def is_valid_date(date_str):
    # 1. Check for None or empty string ""
    if not date_str:
        return False
        
    # 2. Try to parse it against the HTML5 standard format
    try:
        datetime.strptime(date_str.strip(), '%Y-%m-%d')
        return True
    except ValueError:
        # It was a string, but not a valid date format
        return False