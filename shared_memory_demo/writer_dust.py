from multiprocessing import shared_memory
import time
import random

device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
shm_dict = {}

for device in device_ids:
    pm10 = random.randint(100, 400)
    pm25 = random.randint(50, 200)

    # PM2.5 can be a valid simple expression
    if random.choice([True, False]):
        pm25_value = f"{pm10}+{pm25}"
    else:
        pm25_value = str(pm25)

    so2 = random.randint(0, 500)
    no2 = random.randint(0, 500)
    no = random.randint(0, 500)
    co = random.randint(0, 25)
    temp = round(random.uniform(20, 50), 1)
    hum = random.randint(20, 80)
    lat = "085241"
    lon = "0769366"

    data = f"{device}-PM10:{pm10}-PM2.5:{pm25_value}-SO2:{so2}-NO2:{no2}-NO:{no}-CO:{co}-TEMP:{temp}-HUM:{hum}-LAT:{lat}-LON:{lon}"
    byte_data = bytearray(data.encode())

    shm = shared_memory.SharedMemory(create=True, size=256, name=f"{device}_data")  # Increased size
    shm.buf[:len(byte_data)] = byte_data
    shm_dict[device] = shm

    print(f"Data written to shared memory for {device}")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print("Shutting down")
    for device, shm in shm_dict.items():
        shm.close()
        shm.unlink()
















# before new packet format
# from multiprocessing import shared_memory
# import time
# import random

# device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
# shm_dict = {}

# for device in device_ids:
#     dust = str(random.randint(100, 400)).zfill(3)
#     temp = str(random.randint(25, 50)).zfill(2)
#     lat = "085241"  
#     lon = "0769366"

#     data = bytearray(f"{device}-{dust}-{temp}-{lat}-{lon}".encode())

#     # Create shared memory and keep reference
#     shm = shared_memory.SharedMemory(create=True, size=len(data), name=f"{device}_data")
#     shm.buf[:len(data)] = data

#     # Save reference so it doesn’t get destroyed by garbage collection
#     shm_dict[device] = shm

#     print(f"Data written to shared memory for {device}")

# # Keep shared memory alive
# try:
#     while True:
#         time.sleep(5)
# except KeyboardInterrupt:
#     print("Shutting down")

#     # Clean up
#     for device, shm in shm_dict.items():
#         shm.close()
#         shm.unlink()

