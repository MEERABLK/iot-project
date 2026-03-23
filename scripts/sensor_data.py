import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# BROKER = os.getenv("BROKER_IP")
BROKER = "172.20.10.4"
# BROKER = "10.0.0.136"
# BROKER = "127.0.0.1"
PORT = 1883

class SensorData:
    def __init__(self):
        self.fridge1Temperature = None
        self.fridge1Humidity = None
        self.fridge2Temperature = None
        self.fridge2Humidity = None

data = SensorData()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("#")  # subscribe to all topics

def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    if msg.topic == "fridge1/temperature":
        data.fridge1Temperature = float(payload)

    elif msg.topic == "fridge1/humidity":
        data.fridge1Humidity = float(payload)

    elif msg.topic == "fridge2/temperature":
        data.fridge2Temperature = float(payload)

    elif msg.topic == "fridge2/humidity":
        data.fridge2Humidity = float(payload)

    print(f"{msg.topic} -> {payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start():
    client.connect(BROKER, PORT, 60)
    client.loop_start()