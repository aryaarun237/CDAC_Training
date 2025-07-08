import numpy as np
from multiprocessing import shared_memory
import time

data = np.array([350,36,420,38], dtype=np.int32)

shm = shared_memory.SharedMemory(create=True, size=data.nbytes, name="sensor_shm")

shared_array = np.ndarray(data.shape,dtype=data.dtype,buffer=shm.buf)

shared_array[:] = data[:]

print("Data written to shared memory:", shared_array)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing and unlinking shared memory")
    shm.close()
    shm.unlink()