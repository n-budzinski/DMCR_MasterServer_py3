import ipaddress
import uuid
from os import urandom
from collections import defaultdict

def getFile(filename: str) -> str:
    return open(f'res/{filename}', 'rb').read().decode()

def reverse_address(address):
    address = address.split(".")
    address = [octet for octet in address[::-1]]
    address = ".".join(address)
    return str(int(ipaddress.IPv4Address(address)))

def genID():
    return str(uuid.UUID(bytes = urandom(16)))

def clip_string(string:str, limit: int) -> str:
    return string if len(string) <= limit else string[:limit]

def clip(value, lower, upper) -> int | float:
    return lower if value < lower else upper if value > upper else value

def extract_variables(destination: defaultdict, variable_string: str) -> None:
    for option in variable_string.split(sep="^"):
        t = (option.strip("'").split(sep="="))
        if len(t) == 2:
            destination[t[0]] = t[1]  # type: ignore