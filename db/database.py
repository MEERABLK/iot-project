# database.py
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


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