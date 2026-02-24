import RPi.GPIO as GPIO
import time
import mysql.connector

#Database Connection
try:
    mydb = mysql.connector.connect(
          host="localhost",
          user="",#yourusername
          password="",#yourpassword
          database="smartstoreiotproject_db"
    )
    
    mycursor = mydb.cursor()

    print(mydb)

except mysql.connector.Error as err:
    print("Database Connection Failed:",err)
    exir()
    
    
#GPIO setup
GPIO.setmode(GPIO.BCM)

successLed = 17
failLed = 16
buzzer = 21

def success():
    GPIO.setup(successLed, GPIO.OUT)
    GPIO.output(successLed, 1)
    time.sleep(1)
    GPIO.output(successLed, 0)
    

def failure():
    GPIO.setup(failLed, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)

    GPIO.output(failLed, 1)
    GPIO.output(buzzer, True)
    print("Failure detected!")
    print("Buzzer On")
    time.sleep(1)
    GPIO.output(failLed, 0)
    GPIO.output(buzzer, False)
    print("Buzzer Off")

# Insert customer
def add_customer(first, last, email):
    try:
        sql = "INSERT INTO customers (first_name, last_name, email) VALUES (%s, %s, %s)"
        values = (first, last, email)

        mycursor.execute(sql, values)  
        mydb.commit()                  

        print("Customer added successfully!")
        success()

    except mysql.connector.Error as err:
        print("Error:", err)
        failure()

#test insert
add_customer("John", "Smith", "john.smith@gmail.com")

success()
time.sleep(2)
failure()
GPIO.cleanup()