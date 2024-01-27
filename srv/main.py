from threading import Thread
from asyncio import StreamReader, StreamWriter, wait_for, TimeoutError, run, start_server
from socket import socket, AF_INET, SOCK_DGRAM
from traceback import print_exc
from asyncio import StreamWriter
from common import Server, LOCALE, Client, Request, Response
from struct import pack
from games.alexander import get_game

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
    client = Client(*writer.get_extra_info('peername'))
    while True:
        try:
            packet = await wait_for(reader.read(TCP_MAX_PACKET_SIZE), timeout=TCP_TIMEOUT)
            if not packet:
                break
            await process_packet(packet, writer, client)
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

async def process_packet(packet, writer: StreamWriter, client: Client) -> None:
    request = Request(packet)
    print(f"SEQ: {request.seq} LANG: {LOCALE.get(request.language, 1)}\nREQUEST: {request.data}")
    response = Response(request.seq, request.language, request.version, VERSIONS[16].handle(request, client))
    print(f"RESPONSE: {response}\n")
    send_packet(writer, response.as_packet)
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