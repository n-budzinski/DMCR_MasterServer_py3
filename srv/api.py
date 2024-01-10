import dotmap
import requests
from typing import Callable
from sqlalchemy import create_engine
from typing import Any
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--api_address", type=str, help="the database host", required=True)
parser.add_argument("--api_port", type=int, help="the database host", required=False, default=8000)
parser.add_argument("--irc_address", type=str, help="the database host", required=True)
parser.add_argument("--db_address", type=str, help="the database host", required=True)
parser.add_argument("--db_username", type=str, help="the database host", required=True)
parser.add_argument("--db_password", type=str, help="the database host", required=True)
argv = parser.parse_args()

class Response(dotmap.DotMap):
    def __init__(self, request: dict, *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)
        self.result = request.get("result", "error")
        self.content = dotmap.DotMap(request.get("content") if isinstance(request.get("content"), dict) else None)
        # self.content = dotmap.DotMap(request["content"]) if isinstance(request.get("content"), dict) else request.get("content", {})

    def __bool__(self) -> bool:
        return self.result != "error"

# print(
#     Response(requests.get("http://localhost:8000/alexander/get_polls", 
#                  params={
#                      "session_key" : "414715a0-af20-11ee-aa7c-704d7b84b2a8",
#                      "player_id": 2
#                  }).json()).content
# )

class Game:
    route_map = {}

    def route(self, dcml: str):
        def inner(func):
            self.route_map[dcml] = func
            return func
        return inner

    def handle(self, data):
        return self.packet_handler(data)

    def __init__(self,
                 packet_handler: Callable,
                 db_address: str = argv.db_address,
                 db_username: str = argv.db_username,
                 db_password: str = argv.db_password,
                 api_address: str = argv.api_address,
                 api_port: int = 8000,
                 irc_address: str = argv.irc_address,
                 irc_ch1: str = "#test",
                 irc_ch2: str = "#test",
                 scheme: str = "alexander",
                 dbtbl_interval: int = 15) -> None:
        self.packet_handler = packet_handler
        self.db_address = db_address
        self.db_username = db_username
        self.db_password = db_password
        self.api_address = api_address
        self.api_port = api_port
        self.irc_address = irc_address
        self.irc_ch1 = irc_ch1
        self.irc_ch2 = irc_ch2
        self.scheme = scheme
        self.dbtbl_interval = dbtbl_interval
        self.engine = create_engine(f'mysql+pymysql://'
                                    f'{self.db_username}:{self.db_password}'
                                    f'@{self.db_address}/{self.scheme}?charset=utf8mb4')


    def get(self, query: str, **kwargs: Any):
        return dotmap.DotMap(
            requests.get(f"http://{self.api_address}:{self.api_port}/{self.scheme}/{query}", params=kwargs).json(), 
            _dynamic=False
            )
    
    def get_response(self, query: str, session_key: str | None, player_id: str | int | None, **kwargs: Any) -> Response:
        return Response(requests.get(f"http://{self.api_address}:{self.api_port}/{self.scheme}/{query}", 
                                     params={
                                         "session_key": session_key,
                                         "player_id": player_id
                                     } | kwargs).json())

