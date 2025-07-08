# from multiprocessing import shared_memory
# import requests
# import datetime

# # Connect to existing shared memory
# existing_shm = shared_memory.SharedMemory(name="sensor_raw_data")

# # Read data
# raw_data = bytes(existing_shm.buf[:]).decode().strip('\x00')

# # Parse values (assuming fixed positions)
# sensor_id = raw_data[0:8]
# dust_level = int(raw_data[9:12])
# temperature = int(raw_data[13:15])
# latitude = float(raw_data[16:22]) / 10000
# longitude = float(raw_data[23:30]) / 10000
# timestamp = datetime.datetime.now().isoformat()

# # Prepare JSON payload
# payload = {
#     "sensor_id": sensor_id,
#     "timestamp": timestamp,
#     "latitude": latitude,
#     "longitude": longitude,
#     "dust_level": dust_level,
#     "temperature": temperature
# }

# # Send POST request to your Django API
# response = requests.post("http://127.0.0.1:8000/api/readings/", json=payload)

# print("Data sent to API:", response.status_code, response.json())

# # Clean up
# existing_shm.close()
from multiprocessing import shared_memory
import requests, datetime, time, logging

# Setup logger
logging.basicConfig(filename="error_log.txt", level=logging.ERROR)

device_ids = ['SENSOR01', 'SENSOR02']

while True:
    for device in device_ids:
        try:
            shm = shared_memory.SharedMemory(name=f"{device}_data")
            raw_data = bytes(shm.buf[:]).decode().strip('\x00')

            sensor_id = raw_data[0:8]
            dust_level = int(raw_data[9:12])
            temperature = int(raw_data[13:15])
            latitude = float(raw_data[16:22]) / 10000
            longitude = float(raw_data[23:30]) / 10000
            timestamp = datetime.datetime.now().isoformat()

            payload = {
                "sensor_id": sensor_id,
                "timestamp": timestamp,
                "latitude": latitude,
                "longitude": longitude,
                "dust_level": dust_level,
                "temperature": temperature
            }

            response = requests.post("http://127.0.0.1:8000/api/readings/", json=payload)
            print(f"{sensor_id} → {response.status_code}")

            shm.close()

        except Exception as e:
            logging.error(f"{datetime.datetime.now()} - {device} - {str(e)}")
            continue

    time.sleep(3)
