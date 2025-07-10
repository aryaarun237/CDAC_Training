import multiprocessing.shared_memory as shm
import struct
import datetime
import pytz
import time

# Define IST timezone
ist = pytz.timezone("Asia/Kolkata")

# Function to parse packet
def parse_packet(device_name, data):
    """Parse the received 190-byte packet with proper Tag Quality handling"""
    try:
        if len(data) != 190:  # Expect exactly 190 bytes
            print(f"❌ Error: Incorrect packet size! Received {len(data)} bytes, expected 190.")
            return

        # Header (2 Bytes)
        header = data[:2]
        if header != b'\xCD\xAC':
            print("❌ Error: Invalid packet header!")
            return

        # Packet Length (2 Bytes)
        packet_length = struct.unpack('>H', data[2:4])[0]

        # Timestamp (6 Bytes) - Convert to IST
        timestamp_bytes = data[4:10]  
        timestamp = int.from_bytes(timestamp_bytes, byteorder="big")  
        utc_time = datetime.datetime.utcfromtimestamp(timestamp)  
        ist_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist)  

        # Parse Sensor Data (7 Sensors, 19 Bytes Each)
        sensors = []
        offset = 10
        for _ in range(7):
            sensor_id = struct.unpack('>Q', data[offset:offset+8])[0]
            sensor_type = data[offset+8]
            tag_quality = data[offset+9]
            pm_status = data[offset+10]

            if tag_quality == 0:
                pm10_value = "N/A"
                pm2_5_value = "N/A"
            else:
                pm10_value = struct.unpack('>f', data[offset+11:offset+15])[0]
                pm2_5_value = struct.unpack('>f', data[offset+15:offset+19])[0]

            sensors.append({
                "Sensor ID": sensor_id,
                "Type": sensor_type,
                "Tag Quality": tag_quality,
                "PM Status": pm_status,
                "PM10": pm10_value,
                "PM2.5": pm2_5_value
            })
            offset += 19  

        # Temperature & Humidity
        temp_quality = data[offset]
        temperature = "N/A" if temp_quality == 0 else struct.unpack('>f', data[offset+1:offset+5])[0]
        humidity_quality = data[offset+5]
        humidity = "N/A" if humidity_quality == 0 else struct.unpack('>f', data[offset+6:offset+10])[0]
        offset += 10

        # Additional Sensor Values (6 x 4B) & Tag Quality (6 x 1B)
        additional_sensors = []
        for _ in range(6):
            sensor_tag_quality = data[offset]
            sensor_value = "N/A" if sensor_tag_quality == 0 else struct.unpack('>f', data[offset+1:offset+5])[0]
            additional_sensors.append({"Value": sensor_value, "Tag Quality": sensor_tag_quality})
            offset += 5  

        # Digital Inputs (4 x 1B)
        digital_inputs = list(data[offset:offset+4])

        # Print Parsed Data
        print("\n✅ Received Valid Packet from:", device_name)
        print(f"  📅 Timestamp (IST): {ist_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  🌡 Temperature: {temperature}°C, 💧 Humidity: {humidity}%")
        print(f"  🔢 Sensors Data: {sensors}")
        print(f"  🔌 Digital Inputs: {digital_inputs}")
        print(f"  📊 Additional Sensors: {additional_sensors}\n")

    except Exception as e:
        print("❌ Packet Parsing Error:", e)

# Read data from shared memory and detect new updates
def read_from_shared_memory():
    try:
        shared_mem = shm.SharedMemory(name="mqtt_shared")
        last_data = None  # Store last read data to detect changes

        while True:
            raw_bytes = shared_mem.buf.tobytes().rstrip(b'\x00')  # Read and remove padding
            if not raw_bytes:
                time.sleep(0.5)
                continue

            # Detect change in shared memory data
            if raw_bytes != last_data:
                last_data = raw_bytes  # Update last seen data

                # Extract device name and message
                raw_string = raw_bytes.decode("utf-8", errors="ignore")
                if ";" not in raw_string:
                    print("❌ Error: Invalid format in shared memory!")
                    continue

                device_name, hex_message = raw_string.split(";", 1)

                # Convert hex string to bytes and parse the packet
                try:
                    message_bytes = bytes.fromhex(hex_message)
                    parse_packet(device_name, message_bytes)
                except ValueError:
                    print(f"❌ Error: Invalid hex data from {device_name}!")

            time.sleep(0.5)  # Polling interval to avoid CPU overload

    except Exception as e:
        print("❌ Shared Memory Error:", e)

if __name__ == "__main__":
    print("📡 Monitoring shared memory for new data...")
    read_from_shared_memory()
