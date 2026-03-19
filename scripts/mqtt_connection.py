import paho.mqtt.client as mqtt

BROKER = "192.168.0.146"
PORT = 1883

# ✅ Global variables
temperature = None
humidity = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")

def on_message(client, userdata, msg):
    global temperature, humidity

    payload = msg.payload.decode()

    if msg.topic == "esp32/temperature":
        temperature = float(payload)
    elif msg.topic == "esp32/humidity":
        humidity = float(payload)

    print(f"{msg.topic} -> {payload}")

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