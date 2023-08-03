from threading import Thread
from asyncio import StreamReader, StreamWriter, wait_for, TimeoutError, run, start_server
from socket import socket, AF_INET, SOCK_DGRAM
from traceback import print_exc
from struct import pack, unpack, unpack_from
from zlib import compress, decompress
from config import SERVER, TCP_MAX_PACKET_SIZE, TCP_TIMEOUT, UDP_MAX_PACKET_SIZE, GAME_VERSIONS

def unpack_packet(packet: bytes) -> tuple[int, int, int, list]:
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

def pack_packet(data, integrity: bytes):
    packet = bytearray()
    packet.extend(pack("H", len(data)))
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

def send_packet(writer: StreamWriter, response: bytearray) -> None:
    for n in range(0, len(response)//TCP_MAX_PACKET_SIZE+1):
        writer.write(response[TCP_MAX_PACKET_SIZE*n:][:TCP_MAX_PACKET_SIZE])

def udp_punch(recvdata: bytes, recvaddr: tuple, keepalivesock: socket) -> None:
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

def handle_udp(udp_socket: socket) -> None:
    while True:
        Thread(target=udp_punch, args=(*udp_socket.recvfrom(UDP_MAX_PACKET_SIZE), udp_socket)).start()

async def handle_tcp(reader: StreamReader, writer: StreamWriter) -> None:
    while True:
        try:
            packet = await wait_for(reader.read(TCP_MAX_PACKET_SIZE), timeout=TCP_TIMEOUT)
            if not packet:
                break
            await process_packet(packet, writer)
        except TimeoutError:
            break
        except ConnectionResetError:
            break
        except Exception as f:
            print(f)
            print_exc()
    writer.close()
    await writer.wait_closed()

async def process_packet(packet, writer):
    sequence, language, version, data = unpack_packet(packet)
    game, db = GAME_VERSIONS[version]
    response = game.process_request(data, db, writer.get_extra_info(name='peername')[0])
    if response:
        send_packet(writer, addHeader(pack_packet(response, data[-2].decode()), sequence, language, version))
    await writer.drain()

async def run_tcp():
    server = await start_server(handle_tcp, SERVER.address, SERVER.tcp_port)
    async with server:
        await server.serve_forever()

def main():
    udpsocket = socket(AF_INET, SOCK_DGRAM)
    udpsocket.bind((SERVER.address, SERVER.udp_port))
    udpsocket.setblocking(True)
    udpPunchThread = Thread(target=handle_udp, args=(udpsocket,))
    udpPunchThread.daemon = True
    udpPunchThread.start()
    run(run_tcp())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down...")