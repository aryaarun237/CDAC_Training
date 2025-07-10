from multiprocessing import shared_memory
import struct, time, random

device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
shm_dict = {}
SHM_SIZE = 1024

# Function to create simulated 190-byte packet (same structure)
def create_packet(device_id):
    header = b'\xCD\xAC'
    packet_length = struct.pack('>H', 190)
    timestamp = struct.pack('>Q', int(time.time()))[-6:]

    sensor_data = b''
    for i in range(7):
        sensor_id = struct.pack('>Q', i + 1)
        sensor_type = struct.pack('>B', 1)
        tag_quality = struct.pack('>B', random.choice([0, 1]))
        pm_status = struct.pack('>B', 1)
        pm10_value = struct.pack('>f', random.uniform(40, 60))
        pm2_5_value = struct.pack('>f', random.uniform(20, 30))
        sensor_data += sensor_id + sensor_type + tag_quality + pm_status + pm10_value + pm2_5_value

    temperature = struct.pack('>f', 27.5)
    temp_quality = struct.pack('>B', 1)
    humidity = struct.pack('>f', 65.3)
    humidity_quality = struct.pack('>B', 1)

    other_sensors = b''
    for i in range(6):
        other_sensors += struct.pack('>f', float(10 + i)) + struct.pack('>B', 1)

    digital_inputs = struct.pack('>BBBB', 1, 0, 1, 0)

    packet = header + packet_length + timestamp + sensor_data + temperature + temp_quality + humidity + humidity_quality + other_sensors + digital_inputs
    if len(packet) != 188:
        packet += b'\x00' * (188 - len(packet))

    crc = struct.pack('<H', random.randint(0, 65535))
    final_packet = packet + crc
    return final_packet.hex().upper()

# Create shared memory blocks
for device in device_ids:
    shm = shared_memory.SharedMemory(create=True, size=SHM_SIZE, name=f"{device}_data")
    shm_dict[device] = shm

try:
    while True:
        for device in device_ids:
            payload_hex = create_packet(device)
            message = f"{device};{payload_hex}"
            encoded_message = message.encode("utf-8")

            if len(encoded_message) > SHM_SIZE:
                encoded_message = encoded_message[:SHM_SIZE]

            shm = shm_dict[device]
            shm.buf[:len(encoded_message)] = encoded_message
            shm.buf[len(encoded_message):] = b'\x00' * (SHM_SIZE - len(encoded_message))

            print(f"📡 Data written to shared memory for {device}: {len(encoded_message)} bytes")
        time.sleep(3)

except KeyboardInterrupt:
    print("Shutting down writer")
    for shm in shm_dict.values():
        shm.close()
        shm.unlink()









# from multiprocessing import shared_memory
# import time
# import random

# device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
# shm_dict = {}


# for device in device_ids:
#     pm10 = random.randint(100, 400)
#     pm25 = random.randint(50, 200)

#     # PM2.5 can be a valid simple expression
#     if random.choice([True, False]):
#         pm25_value = f"{pm10}+{pm25}"
#     else:
#         pm25_value = str(pm25)

#     so2 = random.randint(0, 500)
#     no2 = random.randint(0, 500)
#     no = random.randint(0, 500)
#     co = random.randint(0, 25)
#     temp = round(random.uniform(20, 50), 1)
#     hum = random.randint(20, 80)
#     lat = "085241"
#     lon = "0769366"

#     data = f"{device}-PM10:{pm10}-PM2.5:{pm25_value}-SO2:{so2}-NO2:{no2}-NO:{no}-CO:{co}-TEMP:{temp}-HUM:{hum}-LAT:{lat}-LON:{lon}"
#     byte_data = bytearray(data.encode())

#     shm = shared_memory.SharedMemory(create=True, size=256, name=f"{device}_data")  # Increased size
#     shm.buf[:len(byte_data)] = byte_data
#     shm_dict[device] = shm

#     print(f"Data written to shared memory for {device}")

# try:
#     while True:
#         time.sleep(5)
# except KeyboardInterrupt:
#     print("Shutting down")
#     for device, shm in shm_dict.items():
#         shm.close()
#         shm.unlink()
