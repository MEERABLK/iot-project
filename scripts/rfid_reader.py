#No Beep and ontinuous inventory

import serial
import time

ser = serial.Serial("/dev/ttyUSB0",115200,timeout=0.1)

# Stop inventory command (standard for many ST-based readers)
ser.write(bytes.fromhex("0008220100000023")) 
time.sleep(0.1)

# disable beep
ser.write(bytes.fromhex("0007FF0000000000"))

# start continuous inventory
ser.write(bytes.fromhex("0008220000000022"))

print("Inventory started")

buffer = bytearray()

while True:

    data = ser.read(ser.in_waiting or 1)
    # print(f"RAW data received: {data.hex()}")
    if data:
        buffer.extend(data)

        while True:

            # idx = buffer.find(b'\xCF')
            idx = buffer.find(b'\xFC')

            if idx == -1:
                break

            if len(buffer) < idx + 5:
                break

            epc_len = buffer[idx+4]

            frame_len = 2 + 2 + 1 + epc_len + 2

            if len(buffer) < idx + frame_len:
                break

            frame = buffer[idx:idx+frame_len]

            epc = frame[5:5+epc_len].hex().upper()

            rssi_raw = frame[5+epc_len]
            rssi = rssi_raw - 256 if rssi_raw > 127 else rssi_raw

            print("EPC:",epc,"RSSI:",rssi)

            del buffer[:idx+frame_len]