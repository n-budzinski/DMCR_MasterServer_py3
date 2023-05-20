import ipaddress
import uuid
from os import urandom

def get_file(filename: str) -> str:
    return open(f'res/{filename}', 'rb').read().decode()

def check_alpha(text: str):
    if text.isalnum():
        return True
    return False

def reverse_address(address):
    address = address[0].split(".")
    address = [octet for octet in address[::-1]]
    address = ".".join(address)
    return str(int(ipaddress.IPv4Address(address)))

def genID():
    return str(uuid.UUID(bytes = urandom(16)))
