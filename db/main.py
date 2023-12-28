from fastapi import FastAPI
from database import get_engine
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

app = FastAPI()
conn = {
    "alexander": get_engine("alexander")
}


@app.get("/{scheme}/clan_admin")
async def clan_admin(scheme: str, 
                       player_id: int, 
                       new_jointer: int,
                       leaver: int,
                       clanID: int,
                       again: str):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            connection.execute(text(
                f'CALL clan_admin({player_id}, {new_jointer}, {leaver}, {clanID}, "{again}")'
            ))
            connection.commit()
        return {"result": True}
    except DBAPIError as err:
        if err.orig:
            error_message = err.orig.args[1]
            if error_message == 'DLG_CLAN_REMOVE':
                return {"result": error_message}
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/create_clan")
async def create_clan(scheme: str,
                        player_id: int,
                        title: str, 
                        signature: str,
                        info: str):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            connection.execute(text(
                f'CALL create_clan({player_id}, "{title}", "{signature}", "{info}")'
            ))
            connection.commit()
        return {"result": True}
    except:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_clan_summary")
async def get_clan_summary(scheme: str,
                        clanID: int,
                        player_id: int):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                summary = connection.execute(text(
                    f"CALL get_clan_summary({clanID}, {player_id})"
                )).fetchone()
                if summary:
                    return {"result": summary._mapping}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}
    

@app.get("/{scheme}/get_clan_members")
async def get_clan_members(scheme: str,
                        clanID: int):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f"CALL get_clan_members({clanID})"
                )).fetchall()
                if result:
                    members = []
                    for member in result:
                        members.append(member._mapping)
                    return {"result": members}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}
    

@app.get("/{scheme}/get_clans")
async def get_clans(scheme: str):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f"CALL get_clans()"
                )).fetchall()
                if result:
                    clans = []
                    for clan in result:
                        clans.append(clan._mapping)
                    return {"result": clans}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_lobbies")
async def get_lobbies(scheme: str):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f"CALL get_lobbies()"
                )).fetchall()
                if result:
                    lobbies = []
                    for lobby in result:
                        lobbies.append(lobby._mapping)
                    return {"result": lobbies}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/send_thread_message")
async def thread_message(scheme: str,
                      message: str,
                      player_id: int,
                      theme: str | None = None):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            if theme:
                connection.execute(text(
                    'INSERT INTO thread_messages '
                    '(author_id, thread_id, content) '
                    f'VALUES ({player_id}, {theme}, '
                    f'"{message}")'
                ))
            else:
                connection.execute(text(
                    'INSERT INTO threads '
                    '(author_id, content) '
                    f'VALUES ({player_id}, "{message}")'
                ))
            connection.commit()
        return {"result": True}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_thread")
async def get_thread(scheme: str,
                        theme: int):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f"CALL get_thread({theme})"
                )).fetchone()
                if result:
                    return {"result": result._mapping}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_thread_messages")
async def get_thread_messages(scheme: str,
                        theme: int):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f"CALL get_thread_messages({theme})"
                )).fetchall()
                if result:
                    messages = []
                    for message in result:
                         messages.append(message._mapping)
                    return {"result": messages}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/search_forum")
async def search_forum(scheme: str,
                        search_nick: str = "",
                        search_text: str = ""):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f'CALL forum_search("{search_nick}", "{search_text}")'
                )).fetchall()
                if result:
                    messages = []
                    for message in result:
                         messages.append(message._mapping)
                    return {"result": messages}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_threads")
async def get_threads(scheme: str,
                        mode: int = 1,
                        next_message: int = 0):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f'CALL get_thread_list({mode}, {next_message})'
                )).fetchall()
                if result:
                    threads = []
                    for thread in result:
                         threads.append(thread._mapping)
                    return {"result": threads}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_lobby")
async def get_lobby(scheme: str,
                        id_room: int):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                "SELECT players, max_players, ip, password, "
                "(SELECT nick "
                "FROM players "
                "WHERE players.player_id = lobbies.host_id) "
                "AS nick, host_id "
                "FROM lobbies "
                f"WHERE id = {id_room} LIMIT 1")).fetchone()
                if result:
                    return {"result": result._mapping}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_choices")
async def get_choices(scheme: str):
    engine = conn.get(scheme)
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                output = {}
                sexes = connection.execute(text(
                "SELECT name FROM sexes")).fetchall()
                if sexes:
                    output["sexes"] = []
                    for sex in sexes:
                         output["sexes"].append(sex._mapping["name"])
                countries = connection.execute(text(
                "SELECT name FROM countries")).fetchall()
                if countries:
                    output["countries"] = []
                    for country in countries:
                         output["countries"].append(country._mapping["name"])
                return {"result": output}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{path:path}")
@app.get("/")
async def invalid(_: str | None = None):
    return {"result" : "INVALID REQUEST"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)