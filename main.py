import threading
from classes import Player
import asyncio
import socket
import math
import pkt
import req
import classes
import json

with open("./settings.json") as file:
    SETTINGS = json.load(file)

connOrd = 0
gamemanager = classes.GameManager()
Lock = threading.Lock()

def handle_udp(udp_sock: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
    while True:
        recvdata, recvaddr = udp_sock.recvfrom(64)
        keepalivethread = threading.Thread(
            target=pkt.handle_client,
            args=(recvdata, recvaddr, udp_sock, gamemanager))
        keepalivethread.start()


async def handle_tcp(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global connOrd
    connOrd += 1
    player = Player(
        ip_address=writer.get_extra_info(name='peername'),
        session_id=connOrd,
        )
    while True:
        try:
            data = await asyncio.wait_for(reader.read(1440), timeout=60)
        # except asyncio.TimeoutError:
        #     print("Timed out")
        #     break
        # except ConnectionResetError:
        #     print("Connection reset")
        #     break
        except Exception as e:
            Lock.acquire()
            print(e)
            Lock.release()
            break
        else:
            if data:
                player.packet_ordinal += 1
                response = req.process_request(data, player, gamemanager)
                if not response:
                    continue
                response = pkt.add_header(response, data)
                fragment_offset = 0
                for fragment_i in range(0, math.ceil(len(response)/1440)):
                    fragment = response[fragment_offset:fragment_offset + 1440]
                    fragment_offset = (fragment_i + 1) * 1440
                    writer.write(fragment)
            else:
                writer.write(bytearray())
        finally:
            await writer.drain()

    gamemanager.player_disconnect(player)
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
    try:
        start()
    except KeyboardInterrupt:
        pass
