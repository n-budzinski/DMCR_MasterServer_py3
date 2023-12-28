from sqlalchemy import create_engine
from sqlalchemy import exc
from os import environ

try:
    host = "localhost"
    username = "DMCR"
    password = "changeme"
    # host = environ["HOST"]
    # username = environ["USERNAME"]
    # password = environ["PASSWORD"]
except KeyError:
    print("Missing environmental variables!")
    quit()

def get_engine(schema: str):
    return create_engine(
        f'mysql+pymysql://'
        f'{username}:{password}'
        f'@{host}/{schema}'
        '?charset=utf8mb4')