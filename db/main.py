from typing import Any, Dict
from fastapi import FastAPI, Depends
from database import get_engine
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

app = FastAPI()
conn = {
    "alexander": get_engine("alexander")
}

async def is_authorized(scheme: str,
                        player_id: int | None = None, 
                        session_key: str | None = None) -> bool:
    if player_id and session_key:
        engine = conn.get(scheme)
        if engine:
            with engine.connect() as connection:
                result = connection.execute(text(
                    "SELECT * FROM sessions "
                    "WHERE "
                    f"player_id = {player_id} AND "
                    f"session_key = '{session_key}'"
                )).fetchone()
                if result:
                    return True
    return False

async def common_parameters(scheme: str, session_key: str = "", authorized: bool = False, player_id: int | None = None):
    return {"scheme": scheme, "authorized": await is_authorized(scheme, player_id, session_key), "player_id": player_id}


@app.get("/{scheme}/get_choices")
async def get_choices(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
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


@app.get("/{scheme}/login")
async def relogin(  username: str,
                    password: str,
                    gmid: str = "",
                    relogin: str = "",
                    common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                if relogin == "true":
                    profile = connection.execute(text(
                    f"CALL relogin(\'{username}\',\'{password}\')")).fetchone()
                    if profile:
                        return {"result": dict(profile._mapping)}
                elif username and password and gmid:
                    profile = connection.execute(text(
                    f"CALL login(\'{username}\',\'{password}\', \'{gmid}\')")).fetchone()
                    if profile:
                        return {"result": dict(profile._mapping)}
                else:
                     return {"result": "MISSING_FIELDS_ERROR"}
    except DBAPIError as ex:
        if ex.orig:
            return {"result": ex.orig.args[1]}
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/clan_admin")
async def clan_admin(   new_jointer: int,
                        leaver: int,
                        clanID: int,
                        again: str,
                        common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            connection.execute(text(
                f'CALL clan_admin({common["player_id"]}, {new_jointer}, {leaver}, {clanID}, "{again}")'
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
async def create_clan(  title: str, 
                        signature: str,
                        info: str,
                        common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            connection.execute(text(
                f'CALL create_clan({common["player_id"]}, "{title}", "{signature}", "{info}")'
            ))
            connection.commit()
        return {"result": True}
    except:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_clan_summary")
async def get_clan_summary( clanID: int,
                            common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not ["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                summary = connection.execute(text(
                    f"CALL get_clan_summary({clanID}, {common['player_id']})"
                )).fetchone()
                if summary:
                    return {"result": dict(summary._mapping)}
        return {"result": False}
    except Exception:
        return {"result": "INTERNAL_ERROR"}
    

@app.get("/{scheme}/get_clan_members")
async def get_clan_members(clanID: int,
                           common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
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
                        members.append(dict(member._mapping))
                    return {"result": members}
        return {"result": False}
    except Exception:
        return {"result": "INTERNAL_ERROR"}
    

@app.get("/{scheme}/get_clans")
async def get_clans(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
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
                        clans.append(dict(clan._mapping))
                    return {"result": clans}
        return {"result": False}
    except Exception:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_lobbies")
async def get_lobbies(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
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
                        lobbies.append(dict(lobby._mapping))
                    return {"result": lobbies}
        return {"result": False}
    except Exception:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/send_thread_message")
async def thread_message(   message: str,
                            theme: str | None = None,
                            common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            if theme:
                connection.execute(text(
                    'INSERT INTO thread_messages '
                    '(author_id, thread_id, content) '
                    f'VALUES ({common["player_id"]}, {theme}, '
                    f'"{message}")'
                ))
            else:
                connection.execute(text(
                    'INSERT INTO threads '
                    '(author_id, content) '
                    f'VALUES ({common["player_id"]}, "{message}")'
                ))
            connection.commit()
        return {"result": True}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_thread")
async def get_thread(   theme: int,
                        common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                    f"CALL get_thread({theme})"
                )).fetchone()
                if result:
                    return {"result": dict(result._mapping)}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_thread_messages")
async def get_thread_messages(  theme: int,
                                common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
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
                         messages.append(dict(message._mapping))
                    return {"result": messages}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/search_forum")
async def search_forum( search_nick: str = "",
                        search_text: str = "",
                        common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
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
                         messages.append(dict(message._mapping))
                    return {"result": messages}
                return {"result": False}
    except Exception:
        return {"result": "INTERNAL_ERROR"}

@app.get("/{scheme}/get_threads")
async def get_threads(  mode: int = 1,
                        next_message: int = 0,
                        common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
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
                         threads.append(dict(thread._mapping))
                    return {"result": threads}
                return {"result": False}
    except Exception:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_lobby")
async def get_lobby(id_room: int,
                    common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
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
                    return {"result": dict(result._mapping)}
                return {"result": False}
    except Exception as ex:
        print(ex)
    return {"result": "INTERNAL_ERROR"}

@app.get("/{scheme}/mail")
async def mail( messageID: int,
                sent: str | None = None,
                readable: str | None = None,
                delete: str | None = None,
                common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            if delete == "true":
                sender = connection.execute(text(
                    f"SELECT id_from, id_to "
                    f"FROM mail_messages "
                    f"WHERE mail_messages.id = {messageID}"
                )).fetchone()
                if sender:
                    sender = sender._mapping
                    connection.execute(text(
                        f"UPDATE mail_messages "
                        f"SET {'removed_by_sender' if sender['id_from'] == int(common['player_id']) else 'removed_by_recipient'} = 1 "
                        f"{', removed_by_recipient = 1' if sender['id_from'] == sender['id_to'] else ''} "
                        f"WHERE id = {messageID}"
                    ))
                    connection.commit()
            summary = connection.execute(text(
                f"CALL mail_stats({common['player_id']}) "
            )).fetchone()
            if summary:
                summary = summary._mapping
                if sent == 'true':
                    mode = "1"
                elif readable == '2':
                    mode = "2"
                elif readable == '3':
                    mode = "3"
                else:
                    mode = "4"
                result = connection.execute(text(
                        f"CALL get_mail({mode}, {common['player_id']})"
                    )).fetchall()
                mail = []
                for entry in result:
                        mail.append(dict(entry._mapping))
                return {"result": mail}
    except DBAPIError as ex:
        if ex.orig:
            return {"result": ex.orig.args[1]}
    return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/send_mail")
async def send_mail(send_to: str,
                    subject: str,
                    message: str,
                    send: str | None,
                    common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
            summary = connection.execute(text(
                f"CALL mail_stats({common['player_id']}) "
            )).fetchone()
            if summary:
                summary = summary._mapping
                if send == 'true':
                    id = connection.execute(text(
                        f"CALL get_player_id_by_nick(\"{send_to}\")"
                    )).fetchone()
                    if id:
                        id = id._mapping.id
                        if id == common["player_id"]:
                                return {"result": "INVALID_RECIPIENT"}
                        if subject and message:
                            connection.execute(text(
                                "INSERT INTO mail_messages "
                                "(id_from, id_to, subject, content) "
                                "VALUES "
                                f"({common['player_id']}, {id._mapping}, \"{subject}\", \"{message}\")"
                            ))
                            connection.commit()
                    else:
                        return {"result": "MAIL_RECIPIENT_NOT_FOUND"}
                return {"result": summary}
            raise
    except Exception:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/view_mail")
async def view_mail(    messageID: int = 1,
                        common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                summary = connection.execute(text(
                    f"CALL mail_stats({common['player_id']}) "
                )).fetchone()
                if summary:
                    summary = summary._mapping
                    message = connection.execute(text(
                        f"SELECT "
                        f"subject "
                        f"content, "
                        f"id_from, "
                        f"sent_at, "
                        f"subject, "
                        f"player_id, "
                        f"status, "
                        f"CONCAT(COALESCE(clans.signature,''), players.nick) AS name "
                        f"FROM mail_messages "
                        f"INNER JOIN players ON players.player_id = id_to "
                        f"LEFT JOIN clans ON clan_id = clans.id "
                        f"WHERE mail_messages.id = {messageID} "
                    )).fetchone()
                    if message:
                        message = message._mapping
                        if message['status'] == 1:
                            connection.execute(text(
                                f"UPDATE mail_messages "
                                f"SET status = 2 "
                                f"WHERE id = {messageID}"
                            ))
                            connection.commit()
                        return {"result": {
                             "summary": dict(summary),
                             "message": dict(message)
                        }}
        raise
    except Exception:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_news")
async def get_news(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                "SELECT posted_at, content FROM news ORDER BY id DESC"
                )).fetchall()
                news = []
                for article in result:
                        news.append(dict(article._mapping))
                return {"result": news}
    except Exception as ex:
        return {"result": "INTERNAL_ERROR"}
    

@app.get("/{scheme}/get_punishments")
async def get_punishments(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                "CALL get_punishments()"
                )).fetchall()
                punishments = []
                for punishment in result:
                        punishments.append(dict(punishment._mapping))
                return {"result": punishments}
    except Exception as ex:
        return {"result": "INTERNAL_ERROR"}
    

@app.get("/{scheme}/get_scored_games")
async def get_scored_games(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                "CALL get_punishments()"
                )).fetchall()
                scored_games = []
                for game in result:
                        scored_games.append(dict(game._mapping))
                return {"result": scored_games}
    except Exception as ex:
        return {"result": "INTERNAL_ERROR"}
    

@app.get("/{scheme}/get_user_details")
async def get_user_details(ID: str,
                           common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                profile = connection.execute(text(
                    f"CALL get_user_details({ID})"
                )).fetchone()
                if profile:
                    profile = profile._mapping
                    can_be_excluded = connection.execute(text(
                        f"CALL can_be_excluded({ID}, {common['player_id']})"
                    )).fetchone()

                    return {"result": [
                        {
                        "profile": dict(profile),
                        "can_be_excluded": True if can_be_excluded else False
                        }
                    ]}
                return {"result": "ERR_USER_NOT_FOUND"}
    except Exception as ex:
        return {"result": "INTERNAL_ERROR " + str(ex)}


@app.get("/{scheme}/get_user_list")
async def get_user_list(    page: int = 0,
                            resort: int | None = None,
                            order: str = "1",
                            common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        order_by = "players." + order if order in ("nick", "name", "id", "country", "score") else "players.score"
        order = 'DESC' if resort == '1' else 'ASC'
        with engine.connect() as connection:
                result = connection.execute(text(
                    f"SELECT get_display_nick(player_id), players.name, players.player_id, countries.name, players.score, ranks.name, row_number()\
                    OVER ( order by {order_by} {order} ) AS 'pos'\
                    FROM players\
                    INNER JOIN ranks ON players.clan_rank = ranks.id\
                    LEFT JOIN countries ON players.country = countries.id\
                    ORDER BY {order_by} {order} LIMIT 14 OFFSET {13 * page};")).fetchall()
                users = []
                for user in result:
                        users.append(dict(user._mapping))
                return {"result": users}
    except Exception as ex:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{scheme}/get_poll")
async def get_poll(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    if not common["authorized"]:
       return {"result": "UNAUTHORIZED"}
    engine = conn.get(common["scheme"])
    if not engine:
          return {"result": "SCHEME_ERROR"}
    try:
        with engine.connect() as connection:
                result = connection.execute(text(
                f"SELECT id, subject, published_at FROM votes;"
                )).fetchone()
                if result:
                    return {"result": dict(result._mapping)}
        return {"result": "POLL_NOT_FOUND"}
    except Exception:
        return {"result": "INTERNAL_ERROR"}


@app.get("/{path:path}")
@app.get("/")
async def invalid(_: str | None = None):
    return {"result" : "INVALID_REQUEST"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)