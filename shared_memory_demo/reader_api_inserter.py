from multiprocessing import shared_memory
import requests, datetime, time, logging

logging.basicConfig(filename="error_log.txt", level=logging.ERROR)
device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']

while True:
    for device in device_ids:
        try:
            shm = shared_memory.SharedMemory(name=f"{device}_data")
            raw_data = bytes(shm.buf[:]).decode().strip('\x00')
            shm.close()

            # Split by tag structure
            fields = dict(item.split(":") for item in raw_data.split("-")[1:])

            def safe_eval(value):
                try:
                    return eval(value)
                except:
                    return float(value)

            payload = {
                "sensor_id": raw_data.split("-")[0],
                "timestamp": datetime.datetime.now().isoformat(),
                "latitude": float(fields["LAT"]) / 10000,
                "longitude": float(fields["LON"]) / 10000,
                "pm10": safe_eval(fields["PM10"]),
                "pm25": safe_eval(fields["PM2.5"]),
                "so2": safe_eval(fields["SO2"]),
                "no2": safe_eval(fields["NO2"]),
                "no": safe_eval(fields["NO"]),
                "co": safe_eval(fields["CO"]),
                "temperature": float(fields["TEMP"]),
                "humidity": float(fields["HUM"])
            }

            response = requests.post("http://127.0.0.1:8000/api/readings/", json=payload)
            print(f"{device} → {response.status_code}")

        except Exception as e:
            logging.error(f"{datetime.datetime.now()} - {device} - {str(e)}")
            continue

    time.sleep(3)



# from multiprocessing import shared_memory
# import requests, datetime, time, logging

# # Setup logger
# logging.basicConfig(filename="error_log.txt", level=logging.ERROR)

# device_ids = ['SENSOR01', 'SENSOR02']

# while True:
#     for device in device_ids:
#         try:
#             shm = shared_memory.SharedMemory(name=f"{device}_data")
#             raw_data = bytes(shm.buf[:]).decode().strip('\x00')

#             sensor_id = raw_data[0:8]
#             dust_level = int(raw_data[9:12])
#             temperature = int(raw_data[13:15])
#             latitude = float(raw_data[16:22]) / 10000
#             longitude = float(raw_data[23:30]) / 10000
#             timestamp = datetime.datetime.now().isoformat()

#             payload = {
#                 "sensor_id": sensor_id,
#                 "timestamp": timestamp,
#                 "latitude": latitude,
#                 "longitude": longitude,
#                 "dust_level": dust_level,
#                 "temperature": temperature
#             }

#             response = requests.post("http://127.0.0.1:8000/api/readings/", json=payload)
#             print(f"{sensor_id} → {response.status_code}")

#             shm.close()

#         except Exception as e:
#             logging.error(f"{datetime.datetime.now()} - {device} - {str(e)}")
#             continue

#     time.sleep(3)
