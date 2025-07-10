from multiprocessing import shared_memory
import requests, struct, datetime, time, logging, json
from pathlib import Path

logging.basicConfig(filename="error_log.txt", level=logging.ERROR)

device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
log_file = Path("readings_log.json")
if not log_file.exists():
    log_file.write_text("[]")

def parse_packet(packet_hex):
    packet_bytes = bytes.fromhex(packet_hex)

    pm10 = struct.unpack('>f', packet_bytes[12+8+1+1+0 : 12+8+1+1+4])[0]
    pm25 = struct.unpack('>f', packet_bytes[12+8+1+1+4 : 12+8+1+1+8])[0]
    temp = struct.unpack('>f', packet_bytes[12 + 7*15 : 12 + 7*15 + 4])[0]
    hum = struct.unpack('>f', packet_bytes[12 + 7*15 + 5 : 12 + 7*15 + 9])[0]

    return pm10, pm25, temp, hum

while True:
    for device in device_ids:
        try:
            shm = shared_memory.SharedMemory(name=f"{device}_data")
            raw_data = bytes(shm.buf[:]).decode().strip('\x00')
            shm.close()

            device_id, packet_hex = raw_data.split(";")
            pm10, pm25, temp, hum = parse_packet(packet_hex)

            payload = {
                "sensor_id": device_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "latitude": 8.5241,
                "longitude": 76.9366,
                "pm10": pm10,
                "pm25": pm25,
                "raw_payload": packet_hex[:20],
                "so2": 0,
                "no2": 0,
                "no": 0,
                "co": 0,
                "temperature": temp,
                "humidity": hum
            }

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









# # print("Reader API Inserter starting...")

# from multiprocessing import shared_memory
# import requests, datetime, time, logging, json, ast
# from pathlib import Path

# # Setup error log
# logging.basicConfig(filename="error_log.txt", level=logging.ERROR)

# device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
# log_file = Path("readings_log.json")

# if not log_file.exists():
#     log_file.write_text("[]")

# def safe_eval(value):
#     try:
#         # Only allow simple math expressions by restricting builtins
#         return eval(value, {"__builtins__": {}})
#     except:
#         try:
#             return float(value)
#         except:
#             print(f"⚠️ Invalid value encountered: '{value}' — setting as None")
#             return None


# while True:
#     for device in device_ids:
#         try:
#             shm = shared_memory.SharedMemory(name=f"{device}_data")
#             raw_data = bytes(shm.buf[:]).decode().strip('\x00')
#             shm.close()

#             fields = dict(item.split(":") for item in raw_data.split("-")[1:])

#             pm10_value = safe_eval(fields["PM10"])
#             pm25_raw = fields["PM2.5"]
#             pm25_value = safe_eval(pm25_raw)

#             payload = {
#                 "sensor_id": raw_data.split("-")[0],
#                 "timestamp": datetime.datetime.now().isoformat(),
#                 "latitude": float(fields["LAT"]) / 10000,
#                 "longitude": float(fields["LON"]) / 10000,
#                 "pm10": pm10_value,
#                 "pm25": pm25_value,
#                 "pm25_raw": pm25_raw,
#                 "so2": safe_eval(fields["SO2"]),
#                 "no2": safe_eval(fields["NO2"]),
#                 "no": safe_eval(fields["NO"]),
#                 "co": safe_eval(fields["CO"]),
#                 "temperature": float(fields["TEMP"]),
#                 "humidity": float(fields["HUM"])
#             }

#             # Debug log: see what is being sent
#             print(f"\nPayload for {device}:")
#             for k, v in payload.items():
#                 print(f"  {k}: {v}")

#             response = requests.post("http://127.0.0.1:8000/api/readings/", json=payload)
#             print(f"{device} → {response.status_code}")

#             with open(log_file, "r+") as file:
#                 data = json.load(file)
#                 data.append(payload)
#                 file.seek(0)
#                 json.dump(data, file, indent=4)

#         except Exception as e:
#             logging.error(f"{datetime.datetime.now()} - {device} - {str(e)}")
#             continue

#     time.sleep(3)




































