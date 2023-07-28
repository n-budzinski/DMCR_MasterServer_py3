import threading
from games.classes import Player, GameManager
import asyncio
import socket
import math
import packets
import traceback
import games.alexander.process as alex
import games.alexander.process as alexdemo
# import games.c2nw.process as c2nw
import games.heroes_of_annihilated_empires.process as hoae
import sqlalchemy
from games.alexander.config import DB as ADBCONF
from games.heroes_of_annihilated_empires.config import DB as HOAECONF

alexdb = sqlalchemy.create_engine(f'mysql+pymysql://{ADBCONF["user"]}:{ADBCONF["password"]}@{ADBCONF["host"]}/{ADBCONF["database"]}?charset=utf8mb4')
hoaedb = sqlalchemy.create_engine(f'mysql+pymysql://{ADBCONF["user"]}:{ADBCONF["password"]}@{ADBCONF["host"]}/{ADBCONF["database"]}?charset=utf8mb4')



gamemanager = GameManager()

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
        with alexdb.connect() as connection:
            lobby = connection.execute(sqlalchemy.text(f"SELECT ip FROM lobbies WHERE ip = '{recvaddr[0]}' LIMIT 1")).fetchone()
            if lobby:
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
    player = Player(writer.get_extra_info(name='peername'))
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
                    header, data = packets.unpack(rawData)
                    player.language = header.clientLanguage
                    response = None
                    if header.clientVersion == 14:
                        # response = c2nw.processRequest(request[0], request[1], request[2], request[4], player, gamemanager)
                        pass
                    elif header.clientVersion == 13:
                        pass
                        # response = alexdemo.processRequest(request[0], request[1], request[2], request[4], player, gamemanager)
                    elif header.clientVersion == 16:
                        response = alex.processRequest(data, alexdb, player, writer.get_extra_info(name='peername')[0])
                    elif header.clientVersion == 30:
                        response = hoae.processRequest(data, alexdb, player, writer.get_extra_info(name='peername')[0])

                    if response:
                        response = packets.pack(response, data[-2].decode())
                        response = packets.addHeader(response, header.sequenceNumber, header.clientLanguage, header.clientVersion)
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
    server = await asyncio.start_server(handleTCP, "0.0.0.0", 34001)
    async with server:
        await server.serve_forever()

def main():
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsocket.bind(("0.0.0.0", 34000))
    udpsocket.setblocking(True)
    udpPunchThread = threading.Thread(target=handleUDP, args=(udpsocket,))
    udpPunchThread.daemon = True
    udpPunchThread.start()
    asyncio.run(run())

if __name__ == "__main__":
    main()
