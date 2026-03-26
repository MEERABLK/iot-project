import paho.mqtt.subscribe as subscribe
import ssl
import timeit

for x in range(50):
    
    msg = subscribe.simple("vanier", hostname="192.168.0.111",
    port=1883,client_id="")
    #publish.
    print(msg)