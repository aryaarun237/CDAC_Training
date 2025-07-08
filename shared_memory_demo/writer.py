from multiprocessing import shared_memory
import time

shm = shared_memory.SharedMemory(create=True,size=50,name='dustdata')
data = b'IotDevice_01-350-42'
shm.buf[:len(data)] = data

print("Data written to shared memory")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("closing shared memory")
    shm.close()
    shm.unlink()