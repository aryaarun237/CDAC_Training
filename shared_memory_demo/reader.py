from multiprocessing import shared_memory
import time

existing_shm = shared_memory.SharedMemory(name='dustdata')

data = bytes(existing_shm.buf[:19]).decode()

print("Data read from shared memory:",data)

existing_shm.close()