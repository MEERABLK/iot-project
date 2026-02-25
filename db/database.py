# database.py
import mysql.connector

def add_customer(first, last, email):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="root123",
            database="smartstoreiotproject_db"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO customers (first_name, last_name, email) VALUES (%s, %s, %s)"
        values = (first, last, email)

        mycursor.execute(sql, values)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return True

    except mysql.connector.Error as err:
        print("Database Error:", err)
        return False