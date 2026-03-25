import time
import paho.mqtt.client as mqtt
from sensor_data import data
import os
from dotenv import load_dotenv

# BROKER = os.getenv("BROKER_IP")
#BROKER = "192.168.0.146"
BROKER = "10.0.0.136"
#BROKER = "172.20.10.4"
# BROKER = "127.0.0.1"
PORT = 1883

# Global variables
temperature = None
humidity = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")

def on_message(client, userdata, msg):
   # global temperature, humidity

    payload = msg.payload.decode()

  #if msg.topic == "esp32/temperature":
       # temperature = float(payload)
    #elif msg.topic == "esp32/humidity":
    humidity = float(payload)

   # print(f"{msg.topic} -> {payload}")
  
    if msg.topic == "esp32/temperature":
     data.fridge1Temperature = float(payload)  # assign to fridge1 temp for testing
    elif msg.topic == "esp32/humidity":
     data.fridge1Humidity = float(payload)
    elif msg.topic == "vanier":
     print(payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

# Run in background
client.loop_start()

# ✅ Now you can use values anywhere
import time

while True:
    print("Temp:", temperature, "| Hum:", humidity)
    time.sleep(2)