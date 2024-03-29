from os import environ
from sqlalchemy import create_engine
from collections import defaultdict


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


class Database:
    # DEFAULTS
    host = environ.get("DCMLEMU_DB_URL", "localhost")
    username = environ.get("DCMLEMU_DB_USERNAME", "admin")
    password = environ.get("DCMLEMU_DB_PASSWORD", "password")
    scheme = environ.get("DCMLEMU_DB_SCHEME", "alexander")


class Game:

    route_map = {}

    def route(self, dcml: str):
        def inner(func):
            self.route_map[dcml] = func
            return func
        return inner

    def __init__(self,
                 host: str,
                 scheme: str,
                 username: str,
                 password: str,
                 irc: Irc,
                 dbtbl_interval: int) -> None:
        self.scheme = scheme
        self.username = username
        self.password = password
        self.irc = irc
        self.dbtbl_interval = dbtbl_interval
        self.engine = create_engine(f'mysql+pymysql://'
                                    f'{environ.get(username, Database.username)}:{environ.get(password, Database.password)}'
                                    f'@{environ.get(host, Database.host)}/{environ.get(scheme, "alexander")}?charset=utf8mb4')

alexander = Game(
    host = "DCMLEMU_ALEX_URL",
    scheme = "DCMLEMU_ALEX_SCHEME",
    username = "DCMLEMU_ALEX_USERNAME",
    password = "DCMLEMU_ALEX_PASSWORD",
    irc = Irc(address = "127.0.0.1", 
              ch1 = "#GSP!conquest_m!5", 
              ch2 = "#GSP!conquest!3"),
    dbtbl_interval = 15)

alexander_demo = Game(
    host = "DCMLEMU_ALEX_DEMO_URL",
    scheme = "DCMLEMU_ALEX_DEMO_SCHEME",
    username = "DCMLEMU_ALEX_DEMO_USERNAME",
    password = "DCMLEMU_ALEX_DEMO_PASSWORD",
    irc = Irc(address = "127.0.0.1", 
              ch1 = "#GSP!conquest_m!5", 
              ch2 = "#GSP!conquest!3"),
    dbtbl_interval = 15)

heroes_of_annihilated_empires = Game(
    host = "DCMLEMU_HOAE_URL",
    scheme = "DCMLEMU_HOAE_SCHEME",
    username = "DCMLEMU_HOAE_USERNAME",
    password = "DCMLEMU_HOAE_PASSWORD",
    irc = Irc(address = "127.0.0.1", 
              ch1 = "#GSP!conquest_m!5", 
              ch2 = "#GSP!conquest!3"),
    dbtbl_interval = 15)

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
    "ERR_EMAIL_FORMAT" : 45012,
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