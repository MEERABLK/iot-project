# database.py
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()  # loads variables from .env

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

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
