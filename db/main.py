from curses.ascii import isalnum
from typing import Any, Dict, Optional
from typing_extensions import Annotated, Doc
from dotmap import DotMap
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from database import get_engine
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

app = FastAPI()
conn = {
    "alexander": get_engine("alexander")
}

class DotMap(DotMap):
     def __getattr__(self, k):
        #   output = super().__getattr__(k)
        #   return output if output else ""
          output = super().__getattr__(k)
          return super().__getattr__(k) or ""

# class Auth_Exception(HTTPException):
#     def __init__(self) -> None:
#          super().__init__(200)

def route_exception_handler(request: Request, exc: Exception):
     return JSONResponse(status_code=404, content={"result": "error",
                                                   "content": "INVALID_REQUEST"}) 

def auth_exception_handler(request: Request, exc: Exception):
     return JSONResponse(status_code=403, content={"result": "error",
                                                   "content": "AUTH_ERROR"}) 

def missing_cred_exception_handler(request: Request, exc: Exception):
     return JSONResponse(status_code=403, content={"result": "error",
                                                   "content": "AUTH_ERROR"}) 

def database_exception_handler(request: Request, exc: Exception):
     return JSONResponse(status_code=200, content={"result": "error",
                                                   "content": exc.orig.args[1]}) # type: ignore

app.add_exception_handler(401, missing_cred_exception_handler)
app.add_exception_handler(403, auth_exception_handler)
app.add_exception_handler(404, route_exception_handler)
app.add_exception_handler(DBAPIError, database_exception_handler)

async def authenticate(scheme: str, player_id: int | None = None, session_key: str | None = None) -> bool:
    if player_id and session_key:
        engine = conn.get(scheme)
        if engine:
            with engine.connect() as connection:
                result = connection.execute(text(
                    "SELECT * FROM sessions "
                    "WHERE "
                    f"player_id = :1 AND "
                    f"session_key = :2"
                ), parameters={"1": player_id, "2": session_key}).fetchone()
                if result:
                    return True
    return False

async def common_parameters(scheme: str) -> Dict:
    if not conn.get(scheme):
         raise HTTPException(status_code=400, detail="SCHEME_ERROR")
    return {"scheme": scheme}

async def is_authenticated(scheme: str, session_key: str = "", player_id: int | None = None) -> None:
    if not (session_key and player_id):
         raise HTTPException(status_code=401)
    if not await authenticate(scheme, player_id, session_key):
         raise HTTPException(status_code=403)

def form_response(result: str, content: Any = None):
     return {
          "result": result,
          "content": content
     }

@app.get("/{scheme}/get_choices")
async def get_choices(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: # type: ignore
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
        return form_response("success", output)

@app.get("/{scheme}/log_user")
async def login(username: str, password: str, gmid: str | None = None, relogin: str = "", session_key: str = "", common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"]) 
    with engine.connect() as connection: # type: ignore
            if relogin == "true":
                profile = connection.execute(text(
                f"CALL relogin(:1, :2)"), parameters={"1": username, "2": password}).fetchone()
                if profile:
                    connection.commit()
                    return form_response("success", dict(profile._mapping))
            elif gmid:
                profile = connection.execute(text(
                f"CALL login(:1, :2, :3)"), parameters={"1": username, "2": password, "3": gmid}).fetchone()
                if profile:
                    if profile._mapping["player_id"] == -1:
                            return form_response("error", "acc_not_found")
                    connection.commit()
                    return form_response("success", dict(profile._mapping))
            else:
                    return form_response("error", "missing_gmid")
    return form_response("error", "INTERNAL_ERROR")

@app.get("/{scheme}/reg_new_user")
async def reg_new_user(mode: str, nick: str, name: str, mail: str, birthday: str, gmid: str, password: str, rassword: str, icq = "", site = "", sex = 0, country = 0, phone = "", common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    if mode in ('edit', 'creat'):
        if mode == 'creat' and \
        not password == rassword:
             return form_response("error", "PASSWORD_MISMATCH")
        with engine.connect() as connection: #type: ignore
            connection.execute(text(
                f'CALL reg_new_user(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)'
            ), parameters={
                    "1": mode,
                    "2": nick,
                    "3": name,
                    "4": mail,
                    "5": icq,
                    "6": site,
                    "7": sex,
                    "8": country,
                    "9": phone,
                    "10": birthday,
                    "11": gmid,
                    "12": password,
                    "13": rassword
            })
            connection.commit()
            return form_response("success")
    return form_response("error", "INCORRECT_MODE")

@app.get("/{scheme}/clan_admin2", dependencies=[Depends(is_authenticated)])
async def clan_admin2(player_id: int, new_jointer: int, leaver: int, clanID: int, again: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    if again == 'true':
        with engine.connect() as connection: #type: ignore
            connection.execute(text(
                f'CALL clan_admin(:1, :2, :3, :4, :5)'
            ), parameters={
                 "1": player_id,
                 "2": new_jointer,
                 "3": leaver,
                 "4": clanID,
                 "5": again
            })
            connection.commit()
        return form_response("success")
    else:
        return form_response("success", "CLAN_REMOVE_DLG")

@app.get("/{scheme}/create_clan", dependencies=[Depends(is_authenticated)])
async def create_clan(player_id: int, title: str, signature: str, info: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        connection.execute(text(
            f'CALL create_clan(:1, :2, :3, :4)'
        ), parameters={
             "1": player_id,
             "2": title,
             "3": signature,
             "4": info
        })
        connection.commit()
    return form_response("success")

@app.get("/{scheme}/get_clan_summary", dependencies=[Depends(is_authenticated)])
async def get_clan_summary(clanID: int, player_id: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:  
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
            summary = connection.execute(text(
                f"CALL get_clan_summary(:1, :2)"
            ), parameters={
                 "1": clanID,
                 "2": player_id
            }).fetchone()
            if summary:
                return form_response("success", dict(summary._mapping))
    return form_response("error", "CLAN_NOT_FOUND")
    
@app.get("/{scheme}/get_clan_members", dependencies=[Depends(is_authenticated)])
async def get_clan_members(clanID: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
            result = connection.execute(text(
                f"CALL get_clan_members(:1)"
            ), parameters={"1": clanID}).fetchall()
            if result:
                members = []
                for member in result:
                    members.append(dict(member._mapping))
                return form_response("success", members)
            return form_response("error", "CLAN_NOT_FOUND")

@app.get("/{scheme}/get_clans", dependencies=[Depends(is_authenticated)])
async def get_clans(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_clans()"
        )).fetchall()
        clans = []
        if result:
            for clan in result:
                clans.append(dict(clan._mapping))
        return form_response("success", clans)

@app.get("/{scheme}/get_lobbies", dependencies=[Depends(is_authenticated)])
async def get_lobbies(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_lobbies()"
        )).fetchall()
        lobbies = []
        if result:
            for lobby in result:
                lobbies.append(dict(lobby._mapping))
        return form_response("success", lobbies if lobbies else None)

@app.get("/{scheme}/send_thread_message", dependencies=[Depends(is_authenticated)])
async def thread_message(message: str, player_id: int, theme: str | None = None, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        if theme:
            connection.execute(text(
                'INSERT INTO thread_messages '
                '(author_id, thread_id, content) '
                f'VALUES (:1, :2, :3)'
            ), parameters={
                 "1": player_id,
                 "2": theme,
                 "3": message
            })
        else:
            connection.execute(text(
                'INSERT INTO threads '
                '(author_id, content) '
                f'VALUES (:1, :2)'
            ), parameters={
                 "1": player_id,
                 "2": message
            })
        connection.commit()
    return form_response("success")

@app.get("/{scheme}/get_thread", dependencies=[Depends(is_authenticated)])
async def get_thread(theme: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_thread(:1)"
        ), parameters={"1": theme}).fetchone()
        if result:
            return form_response("success", dict(result._mapping))
        return form_response("error", "THREAD_NOT_FOUND")

@app.get("/{scheme}/get_thread_messages", dependencies=[Depends(is_authenticated)])
async def get_thread_messages(theme: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_thread_messages(:1)"
        ), parameters={"1": theme}).fetchall()
        messages = []
        if result:
            for message in result:
                    messages.append(dict(message._mapping))
        return form_response("success", messages)

@app.get("/{scheme}/forum_search", dependencies=[Depends(is_authenticated)])
async def forum_search(search_nick: str = "", search_text: str = "", common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f'CALL forum_search(:1, :2)'
        ), parameters={"1": search_nick, "2": search_text}).fetchall()
        messages = []
        if result:
            for message in result:
                    messages.append(dict(message._mapping))
        return form_response("success", messages)

@app.get("/{scheme}/get_threads", dependencies=[Depends(is_authenticated)])
async def get_threads(mode: int = 1, next_message: int = 0, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f'CALL get_thread_list(:1, :2)'
        ), parameters = {"1": mode, "2": next_message}).fetchall()
        threads = []
        if result:
            for thread in result:
                    threads.append(dict(thread._mapping))
        return form_response("success", threads)

@app.get("/{scheme}/get_lobby", dependencies=[Depends(is_authenticated)])
async def get_lobby(id_room: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
        "SELECT players, "
        "max_players, "
        "ip, "
        "password, "
        "(SELECT nick "
        "FROM players "
        "WHERE players.player_id = lobbies.host_id) "
        "AS nick, "
        "host_id "
        "FROM lobbies "
        f"WHERE id = :1 LIMIT 1"), parameters={"1": id_room}).fetchone()
        if result:
            return form_response("success", dict(result._mapping))
        return form_response("error", "LOBBY_NOT_FOUND")

@app.get("/{scheme}/get_mail", dependencies=[Depends(is_authenticated)])
async def get_mail(player_id: str | int, messageID: str | None = None, order: str | None = None, resort: str | int | None = None, sent: str | None = None, readable: str | None = None, delete: str | None = None, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        if delete == "true":
            sender = connection.execute(text(
                f"SELECT id_from, id_to "
                f"FROM mail_messages "
                f"WHERE mail_messages.id = :1"
            ), parameters={"1": messageID}).fetchone()
            if sender:
                sender = sender._mapping
                connection.execute(text(
                    f"UPDATE mail_messages "
                    f"SET :1 = 1 "
                    f":2 "
                    f"WHERE id = :3"
                ), parameters={"1": 'removed_by_sender' if sender['id_from'] == int(player_id) else 'removed_by_recipient', 
                               "2": ', removed_by_recipient = 1' if sender['id_from'] == sender['id_to'] else '',
                               "3": messageID})
                connection.commit()
        summary = connection.execute(text(
            f"CALL mail_stats(:1) "
        ), parameters={"1": player_id}).fetchone()
        if summary:
            if sent == 'true':
                mode = "1"
            elif readable == '2':
                mode = "2"
            elif readable == '3':
                mode = "3"
            else:
                mode = "4"
            result = connection.execute(text(
                    f"CALL get_mail(:1, :2)"
                ), parameters={"1": mode, "2": player_id}).fetchall()
            messages = []
            for entry in result:
                    messages.append(dict(entry._mapping))
            return form_response("success", {
                 "messages": messages,
                 "summary": dict(summary._mapping)
            })
        return form_response("error", "USER_NOT_FOUND")

@app.get("/{scheme}/send_mail", dependencies=[Depends(is_authenticated)])
async def send_mail(player_id: int, send_to: str, subject: str, message: str, send: str | None, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        summary = connection.execute(text(
            f"CALL mail_stats(:1) "
        ), parameters={"1": common['player_id']}).fetchone()
        if summary:
            summary = summary._mapping
            if send == 'true':
                id = connection.execute(text(
                    f"CALL get_player_id_by_nick(:1)"
                ), parameters={"1": send_to}).fetchone()
                if id:
                    id = id._mapping.id
                    if id == player_id:
                            return form_response("error", "INVALID_RECIPIENT")
                    if subject and message:
                        connection.execute(text(
                            "INSERT INTO mail_messages "
                            "(id_from, id_to, subject, content) "
                            "VALUES "
                            f"(:1, :2, :3, :4)"
                        ), parameters={"1": player_id, "2": id._mapping, "3": subject, "4": message})
                        connection.commit()
                else:
                    return form_response("error", "RECIPIENT_NOT_FOUND")
            return form_response("success", summary)
        return form_response("error", "USER_NOT_FOUND")

@app.get("/{scheme}/view_mail", dependencies=[Depends(is_authenticated)])
async def view_mail(messageID: int = 1, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        summary = connection.execute(text(
            f"CALL mail_stats(:1) "
        ), parameters={"1": common['player_id']}).fetchone()
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
                f"WHERE mail_messages.id = :1 "
            ), parameters={"1": messageID}).fetchone()
            if message:
                message = message._mapping
                if message['status'] == 1:
                    connection.execute(text(
                        f"UPDATE mail_messages "
                        f"SET status = 2 "
                        f"WHERE id = :1"
                    ), parameters={"1": messageID})
                    connection.commit()
                return form_response("success", {
                        "summary": dict(summary),
                        "message": dict(message)
                })
        return form_response("error", "USER_NOT_FOUND")

@app.get("/{scheme}/get_news", dependencies=[Depends(is_authenticated)])
async def get_news(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
        "SELECT posted_at, content FROM news ORDER BY id DESC"
        )).fetchall()
        news = []
        for article in result:
                news.append(dict(article._mapping))
        return form_response("success", news)

@app.get("/{scheme}/get_polls", dependencies=[Depends(is_authenticated)])
async def get_polls(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
        "SELECT id, subject, published_at FROM votes"
        )).fetchall()
        polls = []
        for poll in result:
                attr = poll._mapping
                answers = connection.execute(
                    text(f"SELECT text, votes FROM vote_answers WHERE vote_id = :1 LIMIT 4;"
                     ), parameters={
                          "1": attr["id"]
                     }).fetchall()
                polls.append(dict(attr) | {"answers": [dict(answer._mapping) for answer in answers]})
        return form_response("success", polls)
    
@app.get("/{scheme}/get_latest_poll", dependencies=[Depends(is_authenticated)])
async def get_latest_poll(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
        "SELECT id, subject, published_at FROM votes LIMIT 1"
        )).fetchone()
        if result:
            poll = result._mapping
            answers = connection.execute(
                text(f"SELECT id, text, votes FROM vote_answers WHERE vote_id = :1 LIMIT 4;"
                    ), parameters={
                        "1": poll["id"]
                    }).fetchall()
            return form_response("success", dict(poll) | {"answers": [dict(answer._mapping) for answer in answers]})
    return form_response("error", "POLL_NOT_FOUND")

@app.get("/{scheme}/get_punishments", dependencies=[Depends(is_authenticated)])
async def get_punishments(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
        "CALL get_punishments()"
        )).fetchall()
        punishments = []
        for punishment in result:
                punishments.append(dict(punishment._mapping))
        return form_response("success", punishments)

@app.get("/{scheme}/get_scored_games", dependencies=[Depends(is_authenticated)])
async def get_scored_games(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
        "CALL get_punishments()"
        )).fetchall()
        scored_games = []
        for game in result:
                scored_games.append(dict(game._mapping))
        return form_response("success", scored_games)

@app.get("/{scheme}/get_user_details", dependencies=[Depends(is_authenticated)])
async def get_user_details(player_id: int, ID: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        profile = connection.execute(text(
            f"CALL get_user_details(:1)"
        ), parameters={"1": ID}).fetchone()
        if profile:
            profile = profile._mapping
            result = connection.execute(text(
                f"CALL can_be_excluded(:1, :2)"
            ), parameters={"1": ID, "2": player_id}).fetchone()
            if result:
                return form_response("success",
                    {
                    "profile": dict(profile),
                    "can_be_excluded": True if result.can_be_excluded else False
                    }
            )
        return form_response("error", "USER_NOT_FOUND")

@app.get("/{scheme}/get_user_list", dependencies=[Depends(is_authenticated)])
async def get_user_list(page: int = 0, resort: str | None = "1", order: str = "score", common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    order_by = "players." + order if order in ("nick", "name", "id", "country", "score") else "players.score"
    order = 'DESC' if resort == '1' else 'ASC'
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"SELECT get_display_nick(player_id) AS nick, "
            "players.name, "
            "players.player_id, "
            "countries.name AS 'country', "
            "players.score, "
            "ranks.name AS 'rank', "
            "row_number() OVER ( order by :1 :2 ) AS 'pos' "
            "FROM players "
            "INNER JOIN ranks ON players.clan_rank = ranks.id "
            "LEFT JOIN countries ON players.country = countries.id "
            "ORDER BY :1 :2 LIMIT 14 OFFSET :3;"), parameters={"1": order_by, "2": order, "3": page * 13}).fetchall()
        users = []
        for user in result:
                users.append(dict(user._mapping))
        return form_response("success", users)

@app.get("/{scheme}/get_poll", dependencies=[Depends(is_authenticated)])
async def get_poll(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
            result = connection.execute(text(
            f"SELECT id, subject, published_at FROM votes;"
            )).fetchone()
            if result:
                return form_response("success", dict(result._mapping))
    return form_response("error", "POLL_NOT_FOUND")

@app.get("/{scheme}/command_heartbeat", dependencies=[Depends(is_authenticated)])
async def command_heartbeat(player_count: int, host_id: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        connection.execute(text(
                f"UPDATE lobbies SET players = :1 WHERE host_id = :2"
        ), parameters={
             "1": player_count,
             "2": host_id
        })
        connection.commit()
    return form_response("success")

@app.get("/{scheme}/command_leave", dependencies=[Depends(is_authenticated)])
async def command_leave(player_id: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        connection.execute(text(
                f"DELETE FROM lobbies WHERE host_id = :1;"
        ), parameters={
             "1": player_id
        })
        connection.commit()
    return form_response("success")

@app.get("/{scheme}/command_setipaddr", dependencies=[Depends(is_authenticated)])
async def command_setipaddr(player_id: int, lobby_id: int, address: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        connection.execute(text(
                f"UPDATE lobbies SET ip = :1 WHERE id = :2 AND host_id = :3"
        ), parameters={
             "1": address,
             "2": lobby_id,
             "3": player_id
        })
        connection.commit()
    return form_response("success")

@app.get("/{scheme}/command_login")
async def command_login(session_key: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
                f"SELECT player_id "
                f"FROM sessions "
                f"WHERE session_key = :1 "
                f"LIMIT 1"
        ), parameters={
             "1": session_key
        }).fetchone()
        if result:
            profile = connection.execute(text(
                    f"CALL get_profile(:1)"
                ), parameters={
                     "1": result.player_id
                }).fetchone()
            if profile:
                return form_response("success", dict(profile._mapping))
    return form_response("error", "INVALID_SESSION")

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)