import threading
import asyncio
import socket
import traceback
import games.alexander.process as alex
import games.alexander.process as alexdemo
import games.heroes_of_annihilated_empires.process as hoae
from struct import pack, unpack, unpack_from
from zlib import compress, decompress
from config import ALEX_DB, ALEX_DEMO_DB, HOAE_DB, SERVER

def unpack_packet(packet):
    packetData = decompress(packet[12:])
    data = []
    lsize = unpack('H', packetData[0:2])[0]
    functionLength = unpack_from("B"*lsize, packetData[2:])[0]
    cursor = 5 + functionLength
    data.append(packetData[3:3 + functionLength].decode())
    param_n = unpack("H", packetData[3 + functionLength:5 + functionLength])[0]
    for _ in range(0, param_n):
        parameter_length = unpack(
            "I", packetData[cursor:cursor+4], )[0]
        cursor += 4
        value = packetData[cursor:cursor+parameter_length].rstrip(b'\x00')
        data.append(value)
        cursor += parameter_length
    packetData = packetData[cursor:]
    return *unpack("HBB", packet[:4]), data

def pack_packet(data, integrity):
    packet = bytearray()
    packet.extend(pack("H", len(data)))
    # print(data)
    for idx,function in enumerate(data):
        data[idx].append(integrity)
        packet.extend(pack("B", len(data[idx][0])))
        packet.extend(data[idx][0].encode())
        packet.extend(pack("H", len(data[idx])-1))
        for parameter in function[1:]:
            packet.extend(pack("I", len(str(parameter)) + 1))
            packet.extend(str(parameter).encode() + b'\x00')
    return packet

def addHeader(packet, sequence, language, version):
    data = compress(packet)
    return bytearray(pack("HBBII", sequence, language, version, len(data) + 12, len(packet)) + data)

def send_packet(writer: asyncio.StreamWriter, response: bytearray) -> None:
    for n in range(0, 1440//len(response)):
        writer.write(response[1439*n:][:1440])

def udp_punch(recvdata: bytes, recvaddr: tuple, keepalivesock: socket.socket) -> None:
    print(recvaddr)
    action_id = recvdata[4]
    if action_id == 22:
        publicaddr = bytearray()
        publicaddr.extend(recvdata[:4])
        publicaddr.extend(pack('H', 17))
        for octet in recvaddr[0].split(sep="."):
            publicaddr.extend(pack("B", int(octet)))
        publicaddr.extend(pack("H", recvaddr[1]))
        keepalivesock.sendto(publicaddr, recvaddr)

    elif action_id == 24:
        hostaddr = recvdata[6:10]
        hostaddr = ".".join([str(byte) for byte in hostaddr])
        recvdata = bytearray(recvdata)
        recvdata[-5:] = [0x25, 0xCD, 0x40, 0x6E, 0x3E]
        keepalivesock.sendto(recvdata, (hostaddr, 34000))

def handle_udp(udp_socket: socket.socket) -> None:
    while True:
        recvdata, recvaddr = udp_socket.recvfrom(64)
        keepalivethread = threading.Thread(
            target=udp_punch,
            args=(recvdata, recvaddr, udp_socket))
        keepalivethread.start()

async def handle_tcp(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        try:
            raw_data = await asyncio.wait_for(reader.read(1440), timeout=120)
        except asyncio.TimeoutError:
            break
        except ConnectionResetError:
            break
        except Exception:
            break
        else:
            if raw_data:
                try:
                    sequence, language, version, data = unpack_packet(raw_data)
                    response, game, db = None, None, None
                    if version == 13:
                        game, db = alexdemo, ALEX_DEMO_DB
                    # elif version == 14:
                    #     game, db = c2nw, C2NW_DB
                    elif version == 16:
                        game, db = alex, ALEX_DB
                    elif version == 30:
                        game, db = hoae, HOAE_DB
                    if game and db:
                        response = game.process_request(data, db, writer.get_extra_info(name='peername')[0])
                    if response:
                        response = pack_packet(response, data[-2].decode())
                        response = addHeader(response, sequence, language, version)
                        send_packet(writer, response)
                    # else:
                    #     send_packet(writer, bytearray())
                except Exception as f:
                    print(f)
                    traceback.print_exc()
                    break
                finally:
                    await writer.drain()
    writer.close()

async def run():
    server = await asyncio.start_server(handle_tcp, SERVER.address, SERVER.tcp_port)
    async with server:
        await server.serve_forever()

def main():
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsocket.bind((SERVER.address, SERVER.udp_port))
    udpsocket.setblocking(True)
    udpPunchThread = threading.Thread(target=handle_udp, args=(udpsocket,))
    udpPunchThread.daemon = True
    udpPunchThread.start()
    asyncio.run(run())

if __name__ == "__main__":
    main()
