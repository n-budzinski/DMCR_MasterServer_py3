from threading import Thread
from asyncio import StreamReader, StreamWriter, wait_for, TimeoutError, run, start_server
from socket import socket, AF_INET, SOCK_DGRAM
from traceback import print_exc
from struct import pack, unpack, unpack_from
from zlib import compress, decompress
from common import Server, LOCALE
from games.alexander import get_game
from typing import Any

def unpack_packet(packet: bytes) -> tuple[Any, list[bytes]]:
    payload = decompress(packet[12:])
    data = []
    lsize = unpack('H', payload[0:2])[0]
    function_length = unpack_from("B"*lsize, payload[2:])[0]
    cursor = 5 + function_length
    data.append(payload[3:3 + function_length].decode())
    param_n = unpack("H", payload[3 + function_length:5 + function_length])[0]
    for _ in range(0, param_n):
        parameter_length = unpack(
            "I", payload[cursor:cursor+4], )[0]
        cursor += 4
        value = payload[cursor:cursor+parameter_length].rstrip(b'\x00')
        data.append(value)
        cursor += parameter_length
    return unpack("HBB", packet[:4]), data


def pack_packet(data, integrity: str) -> bytearray:
    packet = bytearray()
    packet.extend(pack("H", len(data)))
    for idx, function in enumerate(data):
        data[idx].append(integrity)
        packet.extend(pack("B", len(data[idx][0])))
        packet.extend(data[idx][0].encode())
        packet.extend(pack("H", len(data[idx])-1))
        for parameter in function[1:]:
            packet.extend(pack("I", len(str(parameter)) + 1))
            packet.extend(str(parameter).encode() + b'\x00')
    return packet


def add_header(packet, sequence, language, version) -> bytearray:
    data = compress(packet)
    return bytearray(pack('HBBII', sequence, language, version, len(data) + 12, len(packet)) + data)


def send_packet(writer: StreamWriter, response: bytearray) -> None:
    for n in range(0, len(response)//TCP_MAX_PACKET_SIZE+1):
        writer.write(response[TCP_MAX_PACKET_SIZE*n:][:TCP_MAX_PACKET_SIZE])


def udp_punch(data_received: bytes, received_address: tuple, keepalivesock: socket) -> None:
    action_id = data_received[4]
    if action_id == 22:
        publicaddr = bytearray()
        publicaddr.extend(data_received[:4])
        publicaddr.extend(pack('H', 17))
        for octet in received_address[0].split(sep="."):
            publicaddr.extend(pack("B", int(octet)))
        publicaddr.extend(pack("H", received_address[1]))
        keepalivesock.sendto(publicaddr, received_address)

    elif action_id == 24:
        host_address = data_received[6:10]
        host_address = ".".join([str(byte) for byte in host_address])
        data_received = bytearray(data_received)
        data_received[-5:] = [0x25, 0xCD, 0x40, 0x6E, 0x3E]
        keepalivesock.sendto(data_received, (host_address, 34000))


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
        except ConnectionError as f:
            print(f)
            print_exc()
            break
        else:
            continue
    writer.close()
    await writer.wait_closed()


async def process_packet(packet, writer) -> None:
    (sequence, language, version), data = unpack_packet(packet)
    print(f"SEQ: {sequence} LANG: {LOCALE.get(language, 1)}\nREQUEST: {data}")
    response = VERSIONS[16].handle(data)
    print(f"RESPONSE: {response}\n")
    send_packet(writer, add_header(pack_packet(response, data[-2].decode()), sequence, language, version))
    await writer.drain()


async def run_tcp() -> None:
    server = await start_server(handle_tcp, SERVER.address, SERVER.tcp_port)
    async with server:
        await server.serve_forever()


def main() -> None:
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind((SERVER.address, SERVER.udp_port))
    udp_socket.setblocking(True)
    udp_punch_thread = Thread(target=handle_udp, args=(udp_socket,))
    udp_punch_thread.daemon = True
    udp_punch_thread.start()
    run(run_tcp())


if __name__ == "__main__":
    TCP_MAX_PACKET_SIZE = 1440
    TCP_TIMEOUT = 120
    UDP_MAX_PACKET_SIZE = 64

    VERSIONS = {16: get_game()}
    
    SERVER = Server()
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down...")