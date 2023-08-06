import os
from sqlalchemy import create_engine
from collections import defaultdict

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
ALEX_IRC = Irc(address = "192.168.0.200", ch1 = "#GSP!conquest_m!5", ch2 = "#GSP!conquest!3")
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


mysql_error_messages = defaultdict(lambda: "ERR_INTERNAL",{
    "ERR_INTERNAL" : 45000,
    "ERR_NICK_EXISTS" : 45001,
    "ERR_NICK_EMPTY" : "The Nickname is an obligatory field to be filled in.",
    "ERR_NICK_LENGTH" : 45003,
    "ERR_NICK_FORMAT" : "Incorrect nickname! Nickname must begin with a letter and must not contain other characters than letters, digits and underscores in its body. Press Edit button to check nickname. Press Cancel to exit",
    "ERR_PASS_EMPTY" : "The Password is an obligatory field to be filled in. Attention! The Password will be required in case you need to change account information in future.",
    "ERR_PASS_LENGTH" : "The Password should be between 8 and 24 characters.",
    "ERR_PASS_FORMAT" : "Incorrect password format!",
    "ERR_PASS_MISMATCH" : "Passwords do not match. Please ensure both password fields are identical.",
    "ERR_GMID_EMPTY" : "The GMID is an obligatory field to be filled in.",
    "ERR_GMID_INVALID" : "An invalid Game Box Identifier was entered! Please enter more carefully. The number of attempts is limited. Press Edit button to check Game Box Identifier. Press Cancel to exit",
    "ERR_GMID_USED" : 45010,
    "ERR_MAIL_USED" : 45011,
    "ERR_MAIL_FORMAT" : 45012,
    "ERR_BIRTH_FORMAT" : "Incorrect birthday date! Birthday must be in DD/MM/YYYY or DD.MM.YYYY format. Where DD - day (1-31), MM - month (1-12), YYYY - year. Press Edit button to check birthday date. Press Cancel to exit.",
    "ERR_ACC_NOTFOUND" : "Invalid login data were specified! Press Edit button to update your login data. Press Cancel to exit.",
    "REG_NEW_USER_EDIT_OK": "Your personal profile data has been successfully updated!\\Press OK button to save password, in other case press Cancel.\\This option saves your password and Game Box #ID. Don't use it, if you play from computer accessible for other people.",
    "REG_NEW_USER_CREATE_OK" : "Your personal profile data has been successfully created!\\Press OK button to save password, in other case press Cancel.\\This option saves your password and Game Box #ID. Don't use it, if you play from computer accessible for other people."
})
