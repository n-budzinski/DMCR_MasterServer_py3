import struct

packet = b'\x01\x00\x05\x61\x6c\x69\x76\x65\x03\x00\x08\x00\x00\x00\x01\x00\x00\x00\x0b\x00\x00\x00\x03\x00\x00\x00\x30\x32\x00\x03\x00\x00\x00\x31\x31\x00'



def unpack(packetData):
    data = []
    lsize = struct.unpack('H', packetData[0:2])[0]
    print(lsize)
    functionLength = struct.unpack_from("B"*lsize, packetData[2:])[0]
    cursor = 5 + functionLength
    data.append([packetData[3:3 + functionLength].decode()])
    param_n = struct.unpack("H", packetData[3 + functionLength:5 + functionLength])[0]
    for _ in range(0, param_n):
        parameter_length = struct.unpack(
            "I", packetData[cursor:cursor+4], )[0]
        cursor += 4
        value = packetData[cursor:cursor+parameter_length].rstrip(b'\x00')
        data.append(value)
        cursor += parameter_length
    packetData = packetData[cursor:]
    return data

print(unpack(packet))