from multiprocessing import shared_memory
import time
import random

device_ids = ['SENSOR01', 'SENSOR02', 'SENSOR03']
shm_dict = {}

for device in device_ids:
    dust = str(random.randint(100, 400)).zfill(3)
    temp = str(random.randint(25, 50)).zfill(2)
    lat = "085241"  
    lon = "0769366"

    data = bytearray(f"{device}-{dust}-{temp}-{lat}-{lon}".encode())

    # Create shared memory and keep reference
    shm = shared_memory.SharedMemory(create=True, size=len(data), name=f"{device}_data")
    shm.buf[:len(data)] = data

    # Save reference so it doesn’t get destroyed by garbage collection
    shm_dict[device] = shm

    print(f"Data written to shared memory for {device}")

# Keep shared memory alive
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print("Shutting down")

    # Clean up
    for device, shm in shm_dict.items():
        shm.close()
        shm.unlink()

