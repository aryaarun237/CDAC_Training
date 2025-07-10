import paho.mqtt.client as mqtt
import struct
import datetime
import pytz
import json
import random
import time
import threading

# MQTT Broker Configuration
BROKER = "localhost"  # Replace with actual broker IP
PORT = 1883  # Default MQTT port
DEVICE_TOPICS = [f"iot/device_{i+1}" for i in range(5)]  # Topics for 5 IoT devices

# Define IST timezone
ist = pytz.timezone("Asia/Kolkata")

# Function to simulate packet creation for IoT devices
def create_packet(device_id):
    """Create a 190-byte packet for LoRaWAN device."""
    header = b'\xCD\xAC'  # 2 Bytes
    packet_length = struct.pack('>H', 190)  # 2 Bytes
    timestamp = struct.pack('>Q', int(time.time()))[-6:]  # 6 Bytes
    frame_counter = random.randint(0, 65535)  # Random frame counter for each device

    # Sensor Data Simulation (7 Sensors)
    sensor_data = b''  
    for i in range(7):
        sensor_id = struct.pack('>Q', i + 1)  # 8 Bytes
        sensor_type = struct.pack('>B', 1)  # 1 Byte
        tag_quality = struct.pack('>B', random.choice([0, 1]))  # 1 Byte
        pm_status = struct.pack('>B', 1)  # 1 Byte
        pm10_value = struct.pack('>f', random.uniform(40, 60))  # 4 Bytes (Randomized PM10)
        pm2_5_value = struct.pack('>f', random.uniform(20, 30))  # 4 Bytes (Randomized PM2.5)
        sensor_data += sensor_id + sensor_type + tag_quality + pm_status + pm10_value + pm2_5_value

    # Temperature & Humidity + Tag Quality
    temperature = struct.pack('>f', 27.5)  # 4 Bytes
    temp_quality = struct.pack('>B', 1)  # 1 Byte
    humidity = struct.pack('>f', 65.3)  # 4 Bytes
    humidity_quality = struct.pack('>B', 1)  # 1 Byte

    # Additional Sensors (6 x 4B) & Tag Quality (6 x 1B)
    other_sensors = b''  
    for i in range(6):
        sensor_value = struct.pack('>f', float(10 + i))  # 4 Bytes
        sensor_tag_quality = struct.pack('>B', 1)  # 1 Byte
        other_sensors += sensor_value + sensor_tag_quality

    # Digital Inputs (4 x 1 Byte)
    digital_inputs = struct.pack('>BBBB', 1, 0, 1, 0)  # 4 Bytes

    # Construct the full packet (Without CRC yet)
    packet = (
        header + packet_length + timestamp +
        sensor_data + temperature + temp_quality + humidity + humidity_quality +
        other_sensors + digital_inputs
    )

    # Adjust length to ensure exactly 188 bytes before CRC
    if len(packet) != 188:
        #print(f"❌ Error: Packet length is {len(packet)}, adjusting to 188 bytes...")
        missing_bytes = 188 - len(packet)
        packet += b'\x00' * missing_bytes  # Pad with zeroes to make the packet exactly 188 bytes

    # Calculate CRC Checksum (2 Bytes)
    crc = struct.pack('<H', random.randint(0, 65535))  # Simulated CRC for now

    # Final Packet (Including CRC)
    final_packet = packet + crc  # 190 Bytes (188 + 2 CRC)

    return final_packet, frame_counter

# Function to simulate sending data from IoT devices one by one
def send_data_one_by_one():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    while True:
        for device_id, topic in enumerate(DEVICE_TOPICS, 1):
            packet, frame_counter = create_packet(device_id)
            if packet:
                payload_hex = packet.hex().upper()  # Convert binary packet to HEX string
                message = {
                    "DevEUI": f"01020304050607{device_id:02x}",
                    "FPort": 1,
                    "FCntUp": frame_counter,
                    "ADR": True,
                    "DR": 3,
                    "RSSI": -70 + random.randint(-5, 5),  # Simulated RSSI (-70 ±5 dBm)
                    "SNR": random.uniform(5, 10),  # Simulated SNR (5-10 dB)
                    "payload_hex": payload_hex
                }
                client.publish(topic, json.dumps(message))
                print(f"📡 Device {device_id} Sent Data to {topic} ({len(packet)} bytes)")
                time.sleep(5)  # Wait for 5 seconds before sending next message
            else:
                print(f"⚠️ Device {device_id} failed to create a valid packet!")

# MQTT Message Callback
def on_message(client, userdata, message):
    try:
        payload_str = message.payload.decode("utf-8")  # Decode JSON message
        payload_json = json.loads(payload_str)  # Parse JSON

        if "payload_hex" not in payload_json:
            print(f"❌ Error: No 'payload_hex' found in message from {message.topic}!")
            return

        # Extract & Convert payload_hex to bytes
        payload_bytes = bytes.fromhex(payload_json["payload_hex"])

        print(f"📩 Received Payload from {message.topic} (Hex): {payload_json['payload_hex']}")
        # You can define parse_packet or remove this line if not needed
        # parse_packet(payload_bytes)

    except json.JSONDecodeError:
        print(f"❌ Error: Failed to decode JSON payload from {message.topic}!")

# MQTT Client Setup
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 600)

# Subscribe to all IoT device topics
for topic in DEVICE_TOPICS:
    client.subscribe(topic)

# Create and run the thread that sends data to all devices one by one
thread = threading.Thread(target=send_data_one_by_one)
thread.daemon = True  # Ensures the thread will be terminated when the script exits
thread.start()

print("📡 Waiting for MQTT messages from all IoT devices...")
client.loop_forever()
