import numpy as np
from multiprocessing import shared_memory

existing_shm = shared_memory.SharedMemory(name="sensor_shm")

array = np.ndarray((4,), dtype=np.int32, buffer=existing_shm.buf)

print("Data read from shared memory:",array)
existing_shm.close()