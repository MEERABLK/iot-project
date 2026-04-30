import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# BROKER = os.getenv("BROKER_IP")
#BROKER = "172.20.10.4"
#BROKER = "10.0.0.136"
BROKER = "localhost"
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
    # Subscribe only to the specific fridge topics
    client.subscribe("fridge1/temperature")
    client.subscribe("fridge1/humidity")
    client.subscribe("fridge2/temperature")
    client.subscribe("fridge2/humidity")

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

import requests

def fetch_msp01_data():
    """Fetches the latest environment data from the Pareto Context API."""
    url = "http://172.20.10.4:3001/context/device/c30000455da7/3"
    try:
        # We use a short timeout so a network hiccup doesn't freeze the app
        response = requests.get(url, timeout=1.5)
        if response.status_code == 200:
            raw_data = response.json()
            # Navigate to the 'dynamb' object for our specific device
            dynamb = raw_data['devices']['c30000455da7/3']['dynamb']
            
            return {
                "temp": round(dynamb.get("temperature", 0), 1),
                "hum": round(dynamb.get("relativeHumidity", 0), 1),
                "battery": dynamb.get("batteryPercentage", 0),
                "lux": dynamb.get("luminousFlux", 0)
            }
    except Exception as e:
        print(f"🚨 Sensor Fetch Error: {e}")
    return None

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start():
    client.connect(BROKER, PORT, 60)
    client.loop_start()