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


def stunServe(recvdata, recvaddr, keepalivesock):
    from struct import pack
    # datalen = len(recvdata)
    action_id = recvdata[4]

    if action_id == 22:
        publicaddr = bytearray()
        publicaddr.extend(recvdata[:4])
        publicaddr.extend(pack('H', 17))
        octets = recvaddr[0].split(sep=".")

        for octet in octets:
            octetint = int(octet)
            octetint = pack("B", octetint)
            publicaddr.extend(octetint)
        clientport = pack("H", recvaddr[1])
        publicaddr.extend(clientport)
        keepalivesock.sendto(publicaddr, recvaddr)

    elif action_id == 24:
        hostaddr = recvdata[6:10]
        hostaddr = [str(byte) for byte in hostaddr]
        hostaddr = ".".join(hostaddr)

        for lobby in gamemanager.lobbies:
            if hostaddr == gamemanager.lobbies[lobby].host.ipAddress[0]:
                recvdata = bytearray(recvdata)
                recvdata[-5:] = [0x25, 0xCD, 0x40, 0x6E, 0x3E]
                keepalivesock.sendto(recvdata, (hostaddr, 34000))

    else:
        pass


def handleUDP(udp_sock: socket.socket):
    while True:
        recvdata, recvaddr = udp_sock.recvfrom(64)
        keepalivethread = threading.Thread(
            target=stunServe,
            args=(recvdata, recvaddr, udp_sock, gamemanager))
        keepalivethread.start()


async def handleTCP(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
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
                    response = process.processRequest(
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
    server = await asyncio.start_server(handleTCP, SETTINGS["HOST"], SETTINGS["TCP_PORT"])
    async with server:
        await server.serve_forever()


def start():
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsocket.bind((SETTINGS["HOST"], SETTINGS["UDP_PORT"]))
    udpsocket.setblocking(True)
    stunThread = threading.Thread(target=handleUDP, args=(udpsocket,))
    stunThread.daemon = True
    stunThread.start()
    asyncio.run(run_server())


if __name__ == "__main__":
    start()
