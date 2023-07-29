import threading
import asyncio
import socket
import math
import packets
import traceback
import games.alexander.process as alex
import games.alexander.process as alexdemo
# import games.c2nw.process as c2nw
import games.heroes_of_annihilated_empires.process as hoae
from config import ALEX_DB, ALEX_DEMO_DB, HOAE_DB, SERVER

def sendPacket(writer, response):
    fragment_offset = 0
    for fragment_i in range(0, math.ceil(len(response)/1440)):
        fragment = response[fragment_offset:fragment_offset + 1440]
        fragment_offset = (fragment_i + 1) * 1440
        writer.write(fragment)

def udpPunch(recvdata, recvaddr, keepalivesock):
    from struct import pack
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
        recvdata = bytearray(recvdata)
        recvdata[-5:] = [0x25, 0xCD, 0x40, 0x6E, 0x3E]
        keepalivesock.sendto(recvdata, (hostaddr, 34000))

def handleUDP(udpSock: socket.socket):
    while True:
        recvdata, recvaddr = udpSock.recvfrom(64)
        keepalivethread = threading.Thread(
            target=udpPunch,
            args=(recvdata, recvaddr, udpSock))
        keepalivethread.start()

async def handleTCP(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        try:
            rawData = await asyncio.wait_for(reader.read(1440), timeout=120)
        except asyncio.TimeoutError:
            break
        except ConnectionResetError:
            break
        except Exception:
            break
        else:
            if rawData:
                try:
                    sequence, language, version, data = packets.unpack(rawData)
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
                        response = game.processRequest(data, db, writer.get_extra_info(name='peername')[0])
                    if response:
                        response = packets.pack(response, data[-2].decode())
                        response = packets.addHeader(response, sequence, language, version)
                        sendPacket(writer, response)
                    else:
                        sendPacket(writer, bytearray())
                except Exception as f:
                    print(f)
                    traceback.print_exc()
                    break
                finally:
                    await writer.drain()
    writer.close()

async def run():
    server = await asyncio.start_server(handleTCP, SERVER.address, SERVER.tcp_port)
    async with server:
        await server.serve_forever()

def main():
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsocket.bind((SERVER.address, SERVER.udp_port))
    udpsocket.setblocking(True)
    udpPunchThread = threading.Thread(target=handleUDP, args=(udpsocket,))
    udpPunchThread.daemon = True
    udpPunchThread.start()
    asyncio.run(run())

if __name__ == "__main__":
    main()
