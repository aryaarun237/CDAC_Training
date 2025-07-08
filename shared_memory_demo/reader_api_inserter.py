print("Reader API Inserter starting...")

from multiprocessing import shared_memory
import requests, datetime, time, logging, json, ast
from pathlib import Path

# Setup error log
logging.basicConfig(filename="error_log.txt", level=logging.ERROR)

device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
log_file = Path("readings_log.json")

if not log_file.exists():
    log_file.write_text("[]")

def safe_eval(value):
    try:
        # Only allow simple math expressions by restricting builtins
        return eval(value, {"__builtins__": {}})
    except:
        try:
            return float(value)
        except:
            print(f"⚠️ Invalid value encountered: '{value}' — setting as None")
            return None


while True:
    for device in device_ids:
        try:
            shm = shared_memory.SharedMemory(name=f"{device}_data")
            raw_data = bytes(shm.buf[:]).decode().strip('\x00')
            shm.close()

            fields = dict(item.split(":") for item in raw_data.split("-")[1:])

            pm10_value = safe_eval(fields["PM10"])
            pm25_raw = fields["PM2.5"]
            pm25_value = safe_eval(pm25_raw)

            payload = {
                "sensor_id": raw_data.split("-")[0],
                "timestamp": datetime.datetime.now().isoformat(),
                "latitude": float(fields["LAT"]) / 10000,
                "longitude": float(fields["LON"]) / 10000,
                "pm10": pm10_value,
                "pm25": pm25_value,
                "pm25_raw": pm25_raw,
                "so2": safe_eval(fields["SO2"]),
                "no2": safe_eval(fields["NO2"]),
                "no": safe_eval(fields["NO"]),
                "co": safe_eval(fields["CO"]),
                "temperature": float(fields["TEMP"]),
                "humidity": float(fields["HUM"])
            }

            # Debug log: see what is being sent
            print(f"\nPayload for {device}:")
            for k, v in payload.items():
                print(f"  {k}: {v}")

            response = requests.post("http://127.0.0.1:8000/api/readings/", json=payload)
            print(f"{device} → {response.status_code}")

            with open(log_file, "r+") as file:
                data = json.load(file)
                data.append(payload)
                file.seek(0)
                json.dump(data, file, indent=4)

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
