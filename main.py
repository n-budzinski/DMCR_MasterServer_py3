import threading
from classes import Player
import asyncio
import socket
import math
import packets
import process
import classes
import json
from common import genID
import traceback


with open("./settings.json") as file:
    SETTINGS = json.load(file)

gamemanager = classes.GameManager()
Lock = threading.Lock()


def handle_udp(udp_sock: socket.socket):
    while True:
        recvdata, recvaddr = udp_sock.recvfrom(64)
        keepalivethread = threading.Thread(
            target=packets.handle_client,
            args=(recvdata, recvaddr, udp_sock, gamemanager))
        keepalivethread.start()


async def handle_tcp(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    player = Player(
        writer.get_extra_info(name='peername'),
        genID()
    )
    while True:
        try:
            data = await asyncio.wait_for(reader.read(1440), timeout=120)
        except asyncio.TimeoutError:
            break
        except ConnectionResetError:
            break
        except Exception as e:
            break
        else:
            if data:
                try:
                    player.packetOrdinal += 1
                    response = process.process_request(
                        data, player, gamemanager)
                    if not response:
                        continue
                    response = packets.add_header(response, data)
                    fragment_offset = 0
                    for fragment_i in range(0, math.ceil(len(response)/1440)):
                        fragment = response[fragment_offset:fragment_offset + 1440]
                        fragment_offset = (fragment_i + 1) * 1440
                        writer.write(fragment)
                except Exception as serverException:
                    traceback.print_exc()
                    break
            else:
                writer.write(bytearray())
                await writer.drain()

    gamemanager.disconnect(player)
    writer.close()


async def run_server():
    server = await asyncio.start_server(handle_tcp, SETTINGS["HOST"], SETTINGS["TCP_PORT"])
    async with server:
        await server.serve_forever()


def start():
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsocket.bind((SETTINGS["HOST"], SETTINGS["UDP_PORT"]))
    udpsocket.setblocking(True)
    lobby_thread = threading.Thread(target=handle_udp, args=(udpsocket,))
    lobby_thread.daemon = True
    lobby_thread.start()
    asyncio.run(run_server())


if __name__ == "__main__":
    start()
