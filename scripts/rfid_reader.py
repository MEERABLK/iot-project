# # Use this if rfid reader is not appearing in the USB devices under /dev/ttyUSB*
# # sudo modprobe usbserial vendor=0x0483 product=0x5750

import serial
import time

def get_rfid_tags(timeout=2.0):
    try:
        ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
    except serial.SerialException:
        print("Error: Could not open /dev/ttyUSB0")
        return 123456789012
    
    # Init commands
    ser.write(bytes.fromhex("0008220100000023")) # Stop
    time.sleep(0.1)
    ser.write(bytes.fromhex("0007FF0000000000")) # No beep
    ser.write(bytes.fromhex("0008220000000022")) # Start continuous
    
    buffer = bytearray()
    active_tags = {} # Format: {epc: last_seen_timestamp}

    try:
        while True:
            data = ser.read(ser.in_waiting or 1)
            current_time = time.time()

            if data:
                buffer.extend(data)
                while True:
                    idx = buffer.find(b'\xFC')
                    if idx == -1 or len(buffer) < idx + 5: break

                    epc_len = buffer[idx+4]
                    frame_len = 5 + epc_len + 2
                    if len(buffer) < idx + frame_len: break

                    frame = buffer[idx:idx+frame_len]
                    epc = frame[5:5+epc_len].hex().upper()
                    
                    # Update or Add the tag with current timestamp
                    active_tags[epc] = current_time
                    del buffer[:idx+frame_len]

            # --- REMOVAL LOGIC ---
            # Create a list of tags that haven't been seen within the timeout
            removed_tags = [epc for epc, last_seen in active_tags.items() 
                            if current_time - last_seen > timeout]
            
            for epc in removed_tags:
                del active_tags[epc]

            # Yield the current list of tags physically present
            yield list(active_tags.keys())
            
    finally:
        ser.close()

if __name__ == "__main__":
    print("📡 Monitoring active tags... (Remove tag to see it disappear)")
    for tags in get_rfid_tags():
        print(f"Active Tags: {tags}", end="\r")
        time.sleep(0.1)