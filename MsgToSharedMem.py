import paho.mqtt.client as mqtt
import multiprocessing.shared_memory as shm
import json

# MQTT Broker Configuration
BROKER = "localhost"  # Replace with actual broker IP
PORT = 1883  # Default MQTT port
DEVICE_TOPICS = [f"iot/device_{i+1}" for i in range(2)]  # Topics for IoT devices

# Shared Memory Setup
SHM_SIZE = 1024  # Define shared memory size (adjust as needed)
shared_mem = shm.SharedMemory(create=True, size=SHM_SIZE, name="mqtt_shared")

# MQTT Message Callback
def on_message(client, userdata, message):
    try:
        payload_str = message.payload.decode("utf-8")  # Decode JSON message
        payload_json = json.loads(payload_str)  # Parse JSON

        if "payload_hex" not in payload_json:
            print(f"❌ Error: No 'payload_hex' found in message from {message.topic}!")
            return

        # Construct message in "topic;payload_hex" format
        formatted_message = f"{message.topic};{payload_json['payload_hex']}"
        encoded_message = formatted_message.encode("utf-8")

        # Ensure data fits within shared memory
        if len(encoded_message) > SHM_SIZE:
            print(f"⚠️ Warning: Message too large for shared memory, truncating...")
            encoded_message = encoded_message[:SHM_SIZE]

        # Write to shared memory
        shared_mem.buf[:len(encoded_message)] = encoded_message
        shared_mem.buf[len(encoded_message):] = b'\x00' * (SHM_SIZE - len(encoded_message))  # Clear remaining memory
        print(f"✅ Written to shared memory: {formatted_message}")

    except json.JSONDecodeError:
        print(f"❌ Error: Failed to decode JSON payload from {message.topic}!")
    except Exception as e:
        print(f"❌ Error writing to shared memory: {e}")

# MQTT Client Setup
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 600)

# Subscribe to all IoT device topics
for topic in DEVICE_TOPICS:
    client.subscribe(topic)

print("📡 Waiting for MQTT messages and writing to shared memory...")
client.loop_forever()
