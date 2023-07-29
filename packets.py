from zlib import compress, decompress
import struct

def unpack(packet):
    packetData = decompress(packet[12:])
    data = []
    lsize = struct.unpack('H', packetData[0:2])[0]
    functionLength = struct.unpack_from("B"*lsize, packetData[2:])[0]
    cursor = 5 + functionLength
    data.append(packetData[3:3 + functionLength].decode())
    param_n = struct.unpack("H", packetData[3 + functionLength:5 + functionLength])[0]
    for _ in range(0, param_n):
        parameter_length = struct.unpack(
            "I", packetData[cursor:cursor+4], )[0]
        cursor += 4
        value = packetData[cursor:cursor+parameter_length].rstrip(b'\x00')
        data.append(value)
        cursor += parameter_length
    packetData = packetData[cursor:]
    return *struct.unpack("HBB", packet[:4]), data

def pack(data, integrity):
    packet = bytearray()
    packet.extend(struct.pack("H", len(data)))
    for idx,function in enumerate(data):
        data[idx].append(integrity)
        packet.extend(struct.pack("B", len(data[idx][0])))
        packet.extend(data[idx][0].encode())
        packet.extend(struct.pack("H", len(data[idx])-1))
        for parameter in function[1:]:
            packet.extend(struct.pack("I", len(parameter) + 1))
            packet.extend(parameter.encode() + b'\x00')
    return packet


def addHeader(packet, sequence, language, version):
    data = compress(packet)
    return bytearray(struct.pack("HBBII", sequence, language, version, len(data) + 12, len(packet)) + data)