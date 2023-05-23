from zlib import compress, decompress
import struct

GGWDSERVER_LANG = 0
GGWDSERVER_VERS = 16

# TODO Research the behavior when multiple commands are present


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
        struct.unpack("B", packet[4:5])[0])
    packetData = decompress(packet[12:])
    functions = []
    fun_count = struct.unpack("B", packetData[0:1])[0]

    for function_n in range(0, fun_count):
        functionLength = struct.unpack_from("B", packetData[2:3], False)[0]
        cursor = 5 + functionLength
        functions.append([packetData[3:3 + functionLength].decode(), []])
        param_n = struct.unpack(
            "B", packetData[3 + functionLength:4 + functionLength])[0]
        for _ in range(0, param_n):
            parameter_length = struct.unpack(
                "<H", packetData[cursor:cursor+2], )[0]
            cursor += 4
            value = packetData[cursor:cursor+parameter_length-1]
            functions[function_n][1].append(value)
            cursor += parameter_length
        packetData = packetData[cursor:]
    return header, functions


def pack(data, integrity):
    packet = bytearray()
    packet.extend(struct.pack("H", len(data)))
    for idx,function in enumerate(data):
        data[idx].append(integrity)
        packet.extend(struct.pack("B", len(data[idx][0])))
        packet.extend(data[idx][0].encode())
        packet.extend(struct.pack("H", len(data[idx])-1))
        for parameter in function[1:]:
            packet.extend(struct.pack("I", len(parameter)))
            packet.extend(parameter.encode())
    return packet


def addHeader(packet, sequence):
    packeddata = compress(packet)
    finalizedpacket = bytearray()
    finalizedpacket.extend(struct.pack("H", sequence))
    finalizedpacket.extend(struct.pack("B", GGWDSERVER_LANG))
    finalizedpacket.extend(struct.pack("B", GGWDSERVER_VERS))
    finalizedpacket.extend(struct.pack("I", len(packeddata) + 12))
    finalizedpacket.extend(struct.pack("I", len(packet)))
    finalizedpacket.extend(packeddata)
    return finalizedpacket