data = bytearray.fromhex('434F414C010234003644324130313132')

# Device Name
device_name = data[0:4].decode()
print("Device Name:", device_name)

# Device ID
device_id = data[4]
print("Device ID:", device_id)

# Dust Level (bytes 5-6)
dust_level = int(data[5:7].hex(), 16)
print("Dust Level:", dust_level)

# Temperature (bytes 7-8)
temperature = int(data[7:9].hex(), 16)
print("Temperature:", temperature)

# Latitude (bytes 9-13)
latitude = int(data[9:13].hex(), 16) / 10000
print("Latitude:", latitude)

# Longitude (bytes 13:17)
longitude = int(data[13:17].hex(), 16) / 10000
print("Longitude:", longitude)



# # print(data)
# # print(data.decode())

# # print(data[0:5].decode())

# # with open("sensor_data.txt", "w") as f:
# #     f.write("IOT01 0420 035 26.3 70.8\nIOT02 0340 040 27.1 75.0")
    
# # with open("sensor_data.txt", "r") as f:
# #     for line in f:
# #         print(line.strip())


# # hex_data = "496f744465766963655f3031"
# # bytes_data = bytes.fromhex(hex_data)
# # print(bytes_data.decode())


# packet =  b"IOT01 0400 035 26.3 70.8"

# print(packet)

# device_id = packet[0:5].decode()
# print("Device ID:",device_id)

# dust_level = packet[6:10].decode()
# print("Dust level:", dust_level)

# if int(dust_level)>350:
#     print("high dust level detected")
    
# data = bytearray(packet)
# data[6:10] = b"0450"
# print("Modified packet:",data.decode())