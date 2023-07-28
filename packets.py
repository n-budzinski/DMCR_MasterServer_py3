from zlib import compress, decompress
import games.alexander.config as config
import struct

class Header:
    def __init__(self,
                 sequenceNumber: int,
                 clientLanguage: int,
                 clientVersion: int) -> None:
        self.sequenceNumber = sequenceNumber
        self.clientLanguage = clientLanguage
        self.clientVersion = clientVersion

def unpack(packet):
    header = Header(
        struct.unpack("H", packet[:2])[0],
        struct.unpack("B", packet[2:3])[0],
        struct.unpack("B", packet[3:4])[0])
    packetData = decompress(packet[12:])

    data = []
    lsize = struct.unpack('H', packetData[0:2])[0]
    print(lsize)
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
    return header, data

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
    packeddata = compress(packet)
    return bytearray(struct.pack("H", sequence)+
                                struct.pack("B", language)+
                                struct.pack("B", version)+
                                struct.pack("I", len(packeddata) + 12)+
                                struct.pack("I", len(packet))+
                                packeddata)