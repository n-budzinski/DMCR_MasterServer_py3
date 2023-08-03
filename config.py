import os
from sqlalchemy import create_engine

TCP_MAX_PACKET_SIZE = 1440
TCP_TIMEOUT = 120
UDP_MAX_PACKET_SIZE = 64

class Server():
    def __init__(self, 
                address: str = "0.0.0.0", 
                udp_port: int = 34000, 
                tcp_port: int = 34001
                ) -> None:
        self.address, self.udp_port, self.tcp_port = address, udp_port, tcp_port

class Irc():
    def __init__(self, address: str, ch1: str, ch2: str) -> None:
        self.address, self.ch1, self.ch2 = address, ch1, ch2

DB_HOST = os.environ.get("DCMLEMU_DB_URL", "localhost")
DB_USERNAME = os.environ.get("DCMLEMU_DB_USERNAME", "admin")
DB_PASSWORD = os.environ.get("DCMLEMU_DB_PASSWORD", "password")

ALEX_HOST = os.environ.get("DCMLEMU_ALEX_URL", DB_HOST)
ALEX_SCHEME = os.environ.get("DCMLEMU_ALEX_SCHEME", "alexander")
ALEX_USERNAME = os.environ.get("DCMLEMU_ALEX_USERNAME", DB_USERNAME)
ALEX_PASSWORD = os.environ.get("DCMLEMU_ALEX_PASSWORD", DB_PASSWORD)
ALEX_IRC = Irc(address = "192.168.1.200", ch1 = "#GSP!conquest_m!5", ch2 = "#GSP!conquest!3")
ALEX_DBTBL_INTERVAL = 15

ALEX_DEMO_HOST = os.environ.get("DCMLEMU_ALEX_DEMO_URL", DB_HOST)
ALEX_DEMO_SCHEME = os.environ.get("DCMLEMU_ALEX_DEMO_SCHEME", "alexander_demo")
ALEX_DEMO_USERNAME = os.environ.get("DCMLEMU_ALEX_DEMO_USERNAME", DB_USERNAME)
ALEX_DEMO_PASSWORD =os.environ.get("DCMLEMU_ALEX_DEMO_PASSWORD", DB_PASSWORD)
ALEX_DEMO_IRC = Irc(address = "irc.freenode.org", ch1 = "#GSP!conquest_m!5", ch2 = "#GSP!conquest!3")
ALEX_DEMO_DBTBL_INTERVAL = 15

HOAE_HOST = os.environ.get("DCMLEMU_HOAE_URL", DB_HOST)
HOAE_SCHEME = os.environ.get("DCMLEMU_HOAE_SCHEME", "heroes_of_annihilated_empires")
HOAE_USERNAME = os.environ.get("DCMLEMU_HOAE_USERNAME", DB_USERNAME)
HOAE_PASSWORD =os.environ.get("DCMLEMU_HOAE_PASSWORD", DB_PASSWORD)
HOAE_IRC = Irc(address = "irc.freenode.org", ch1 = "#GSP!conquest_m!5", ch2 = "#GSP!conquest!3")
HOAE_DBTBL_INTERVAL = 15

ALEX_DB = create_engine(f'mysql+pymysql://{ALEX_USERNAME}:{ALEX_PASSWORD}@{ALEX_HOST}/{ALEX_SCHEME}?charset=utf8mb4')
ALEX_DEMO_DB = create_engine(f'mysql+pymysql://{ALEX_DEMO_USERNAME}:{ALEX_DEMO_PASSWORD}@{ALEX_DEMO_HOST}/{ALEX_DEMO_SCHEME}?charset=utf8mb4')
HOAE_DB = create_engine(f'mysql+pymysql://{HOAE_USERNAME}:{HOAE_PASSWORD}@{HOAE_HOST}/{HOAE_SCHEME}?charset=utf8mb4')
SERVER = Server()
