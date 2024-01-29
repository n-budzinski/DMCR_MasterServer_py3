import ipaddress
from collections import defaultdict
from struct import pack, unpack, unpack_from
from zlib import compress, decompress
from requests import RequestException
import requests
from typing import Callable
from sqlalchemy import create_engine
from typing import Any
import configparser

class Client:

    def __init__(self, 
                 address: str, 
                 port: int | str,
                 player_id: int | str = 0,
                 session_key: str = "") -> None:
        self.address = address
        self.port = port
        self.player_id = player_id
        self.session_key = session_key


class Server():

    def __init__(self, 
                address: str = "0.0.0.0", 
                udp_port: int = 34000, 
                tcp_port: int = 34001
                ) -> None:
        self.address, self.udp_port, self.tcp_port = address, udp_port, tcp_port


class Packet:

    def __init__(self, seq: int, language: int, version: int, data: list) -> None:
        self.seq, self.language, self.version, self.data =\
            seq, language, version, data


class Request(Packet):

    def __init__(self, request: bytes) -> None:
        metadata, data = Request._unpack(request)
        super().__init__(*metadata, data)

    @staticmethod
    def _unpack(packet: bytes) -> tuple[tuple[int, int, int], list]:
        try:
            payload = decompress(packet[12:])
            data = []
            lsize = unpack('H', payload[0:2])[0]
            function_length = unpack_from("B"*lsize, payload[2:])[0]
            cursor = 5 + function_length
            data.append(payload[3:3 + function_length].decode())
            param_n = unpack("H", payload[3 + function_length:5 + function_length])[0]
            for _ in range(0, param_n):
                parameter_length = unpack("I", payload[cursor:cursor+4], )[0]
                cursor += 4
                data.append(payload[cursor:cursor+parameter_length].rstrip(b'\x00'))
                cursor += parameter_length
            metadata = unpack("HBB", packet[:4])
            if len(metadata) == 3 and all(isinstance(i, int) for i in metadata):
                return metadata, data
            raise
        except:
            raise RequestException


class Response(Packet):

    def __init__(self, seq: int, language: int, version: int, data: list, integrity: str) -> None:
        super().__init__(seq, language, version, data)
        self.as_packet = Response._add_header(seq, language, version, Response._pack(data, integrity))

    @staticmethod
    def _add_header(sequence: int, language: int, version: int, data: bytearray) -> bytearray:
        _data = compress(data)
        print(data)
        return bytearray(pack('HBBII', sequence, language, version, len(_data) + 12, len(data)) + _data)

    @staticmethod
    def _pack(data: list, integrity: str) -> bytearray:
        packet = bytearray()
        packet.extend(pack("H", len(data)))
        for idx, function in enumerate(data):
            # data[idx].append(integrity)
            packet.extend(pack("B", len(data[idx][0])))
            packet.extend(data[idx][0].encode())
            packet.extend(pack("H", len(data[idx])))
            for parameter in function[1:]:
                packet.extend(pack("I", len(str(parameter))))
                packet.extend(str(parameter).encode())
            packet.extend(pack("I", len(str(integrity)) + 1))
            packet.extend(str(integrity).encode() + b'\x00')
        return packet

class Api_Response:
    def __init__(self, response: dict, *args, **kwargs) -> None:
        self.result = response['result']
        self.content = response['content']

    def __bool__(self) -> bool:
        return self.result == "success"

class Game:

    route_map = {}

    def route(self, dcml: str):
        def inner(func):
            self.route_map[dcml] = func
            return func
        return inner

    def __init__(self,
                 packet_handler: Callable,
                 config_file: str = "games/alexander/config.ini",
                 dcml_directory: str = "games/alexander/dcml/"
                 ) -> None:
        self.packet_handler = packet_handler
        self.dcml_directory = dcml_directory
        self.config = configparser.ConfigParser(inline_comment_prefixes=("//"))
        self.config.read(config_file)
        self.irc_address = self.config["IRC"]["HOSTNAME"]
        self.irc_ch1 = self.config["IRC"]["CH1"]
        self.irc_ch2 = self.config["IRC"]["CH2"]
        self.dbtbl_interval = self.config["SETTINGS"]["DBTBL_INTERVAL"]
        self.engine = create_engine(f'mysql+pymysql://'
                                    f'{self.config["DATABASE"]["USERNAME"]}:{self.config["DATABASE"]["PASSWORD"]}'
                                    f'@{self.config["DATABASE"]["HOSTNAME"]}/{self.config["DATABASE"]["SCHEME"]}?charset=utf8mb4')


    def get_response(self, query: str, client: Client, **kwargs: Any) -> Api_Response:
        return Api_Response(requests.get(f"http://{self.config['API']['HOSTNAME']}:{self.config['API']['PORT']}/{self.config['DATABASE']['SCHEME']}/{query}", 
                                     params= kwargs | {
                                         "session_key": client.session_key,
                                         "player_id": client.player_id
                                     }).json())

    def render_tempate(self, filename: str, **kwargs) -> str:
        file = open(self.dcml_directory + filename, 'rb').read().decode()
        for key, value in kwargs.items():
            file = file.replace(f"<<{key}>>", str(value)).replace('\r', '').replace('\n', '')
        return file

def reverse_address(address):
    address = address.split(".")
    address = [octet for octet in address[::-1]]
    address = ".".join(address)
    return str(int(ipaddress.IPv4Address(address)))

def clip_string(string:str, limit: int) -> str:
    return string if len(string) <= limit else string[:limit]

def clip(value, lower, upper) -> int | float:
    return lower if value < lower else upper if value > upper else value

def extract_variables(destination: defaultdict, variable_string: str) -> None:
    for option in variable_string.split(sep="^"):
        t = (option.strip("'").split(sep="="))
        if len(t) == 2:
            destination[t[0]] = t[1]  # type: ignore

mysql_error_messages = defaultdict(lambda: "ERR_INTERNAL",{
    "ERR_INTERNAL" : "Server error occurred while processing your request! Press Try Again button to attempt process request again. Press Cancel to exit",
    "ERR_NICK_EXISTS" : "User with that nickname already exists! Press Edit button to change nickname. Press Cancel button to exit",
    "ERR_NICK_EMPTY" : "The Nickname is an obligatory field to be filled in.",
    "ERR_NICK_LENGTH" : "Nickname too short. Press Cancel button to exit",
    "ERR_NICK_FORMAT" : "Incorrect nickname! Nickname must begin with a letter and must not contain other characters than letters, digits and underscores in its body. Press Edit button to check nickname. Press Cancel to exit",
    "ERR_PASS_EMPTY" : "The Password is an obligatory field to be filled in. Attention! The Password will be required in case you need to change account information in future.",
    "ERR_PASS_LENGTH" : "The Password should be between 8 and 24 characters.",
    "ERR_PASS_FORMAT" : "Incorrect password format!",
    "ERR_PASS_MISMATCH" : "Passwords do not match. Please ensure both password fields are identical.",
    "ERR_GMID_EMPTY" : "The GMID is an obligatory field to be filled in.",
    "ERR_GMID_INVALID" : "An invalid Game Box Identifier was entered! Please enter more carefully. The number of attempts is limited. Press Edit button to check Game Box Identifier. Press Cancel to exit",
    "ERR_GMID_USED" : "The provided Game Box Identifier has already been used. The number of attempts is limited. Press Edit button to check Game Box Identifier. Press Cancel to exit",
    "ERR_EMAIL_USED" : "The provided E-Mail address has already been used. Press Edit button to check E-Mail address. Press Cancel to exit",
    "ERR_BIRTH_FORMAT" : "Incorrect birthday date! Birthday must be in DD/MM/YYYY or DD.MM.YYYY format. Where DD - day (1-31), MM - month (1-12), YYYY - year. Press Edit button to check birthday date. Press Cancel to exit.",
    "ERR_ACC_NOTFOUND" : "Invalid login data were specified! Press Edit button to update your login data. Press Cancel to exit.",
    "REG_NEW_USER_EDIT_OK": "Your personal profile data has been successfully updated!\\Press OK button to save password, in other case press Cancel.\\This option saves your password and Game Box #ID. Don't use it, if you play from computer accessible for other people.",
    "REG_NEW_USER_CREATE_OK" : "Your personal profile data has been successfully created!\\Press OK button to save password, in other case press Cancel.\\This option saves your password and Game Box #ID. Don't use it, if you play from computer accessible for other people."
})

LOCALE = {
    1: "English",
    2: "German",
    3: "French",
    4: "Russian",
    5: "Japanese",
    6: "Spanish",
    7: "Italian",
    8: "Polish",
    9: "Ukrainian",
    10: "Czech",
    11: "Portuguese",
    12: "Chinese",
    13: "Estonian",
    14: "Lithuanian",
    15: "Dutch",
    16: "HOAE: Japanese",
    17: "HOAE: Chinese Simplified",
    18: "HOAE: Chinese Traditional"
}