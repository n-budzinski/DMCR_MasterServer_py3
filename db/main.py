from typing import Any, Dict
from fastapi import FastAPI, Depends, HTTPException
from database import get_engine
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

app = FastAPI()
conn = {
    "alexander": get_engine("alexander")
}

async def authenticate(scheme: str, player_id: int | None = None, session_key: str | None = None) -> bool:
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

async def common_parameters(scheme: str) -> Dict:
    if not conn.get(scheme):
         raise HTTPException(status_code=200, detail="SCHEME_ERROR")
    return {"scheme": scheme}

async def is_authenticated(scheme: str, session_key: str = "", player_id: int | None = None) -> None:
    if not await authenticate(scheme, player_id, session_key):
         raise HTTPException(status_code=200, detail="AUTH_ERROR")

def form_response(result: str, content: Any = None):
     return {
          "RESULT": result,
          "CONTENT": content
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
        return form_response("SUCCESS", output)

@app.get("/{scheme}/login")
async def relogin(username: str, password: str, gmid: str | None = None, relogin: str = "", common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"]) 
    with engine.connect() as connection: # type: ignore
            if relogin == "true":
                profile = connection.execute(text(
                f"CALL relogin(\'{username}\',\'{password}\')")).fetchone()
                if profile:
                    return form_response("SUCCESS", dict(profile._mapping))
            elif gmid:
                profile = connection.execute(text(
                f"CALL login(\'{username}\',\'{password}\', \'{gmid}\')")).fetchone()
                if profile:
                    if profile._mapping["profile_id"] == -1:
                            return form_response("ERROR", "ERR_ACC_NOTFOUND")
                    return form_response("SUCCESS", dict(profile._mapping))
            else:
                    return form_response("ERROR", "MISSING_GMID_ERROR")
    return form_response("ERROR", "INTERNAL_ERROR")

@app.get("/{scheme}/clan_admin2", dependencies=[Depends(is_authenticated)])
async def clan_admin2(new_jointer: int, leaver: int, clanID: int, again: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    if again == 'true':
        with engine.connect() as connection: #type: ignore
            connection.execute(text(
                f'CALL clan_admin({common["player_id"]}, {new_jointer}, {leaver}, {clanID}, "{again}")'
            ))
            connection.commit()
        return form_response("SUCCESS")
    else:
        return form_response("SUCCESS", "CLAN_REMOVE_DLG")

@app.get("/{scheme}/create_clan", dependencies=[Depends(is_authenticated)])
async def create_clan(title: str, signature: str, info: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        connection.execute(text(
            f'CALL create_clan({common["player_id"]}, "{title}", "{signature}", "{info}")'
        ))
        connection.commit()
    return form_response("SUCCESS")

@app.get("/{scheme}/get_clan_summary", dependencies=[Depends(is_authenticated)])
async def get_clan_summary( clanID: int,
                            common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
            summary = connection.execute(text(
                f"CALL get_clan_summary({clanID}, {common['player_id']})"
            )).fetchone()
            if summary:
                return form_response("SUCCESS", dict(summary._mapping))
    return form_response("ERROR", "CLAN_NOT_FOUND")
    
@app.get("/{scheme}/get_clan_members", dependencies=[Depends(is_authenticated)])
async def get_clan_members(clanID: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
            result = connection.execute(text(
                f"CALL get_clan_members({clanID})"
            )).fetchall()
            if result:
                members = []
                for member in result:
                    members.append(dict(member._mapping))
                return form_response("SUCCESS", members)
            return form_response("ERROR", "CLAN_NOT_FOUND")

@app.get("/{scheme}/get_clans", dependencies=[Depends(is_authenticated)])
async def get_clans(common: dict = Depends(common_parameters)) -> Dict[str, list]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_clans()"
        )).fetchall()
        clans = []
        if result:
            for clan in result:
                clans.append(dict(clan._mapping))
        return form_response("SUCCESS", clans)

@app.get("/{scheme}/get_lobbies", dependencies=[Depends(is_authenticated)])
async def get_lobbies(common: dict = Depends(common_parameters)) -> Dict[str, list]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_lobbies()"
        )).fetchall()
        lobbies = []
        if result:
            for lobby in result:
                lobbies.append(dict(lobby._mapping))
        return form_response("SUCCESS", lobbies)

@app.get("/{scheme}/send_thread_message", dependencies=[Depends(is_authenticated)])
async def thread_message(message: str, theme: str | None = None, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
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
    return form_response("SUCCESS")

@app.get("/{scheme}/get_thread", dependencies=[Depends(is_authenticated)])
async def get_thread(theme: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_thread({theme})"
        )).fetchone()
        if result:
            return form_response("SUCCESS", dict(result._mapping))
        return form_response("ERROR", "THREAD_NOT_FOUND")

@app.get("/{scheme}/get_thread_messages", dependencies=[Depends(is_authenticated)])
async def get_thread_messages(theme: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f"CALL get_thread_messages({theme})"
        )).fetchall()
        messages = []
        if result:
            for message in result:
                    messages.append(dict(message._mapping))
        return form_response("SUCCESS", messages)

@app.get("/{scheme}/search_forum", dependencies=[Depends(is_authenticated)])
async def search_forum(search_nick: str = "", search_text: str = "", common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f'CALL forum_search("{search_nick}", "{search_text}")'
        )).fetchall()
        messages = []
        if result:
            for message in result:
                    messages.append(dict(message._mapping))
        return form_response("SUCCESS", messages)

@app.get("/{scheme}/get_threads", dependencies=[Depends(is_authenticated)])
async def get_threads(mode: int = 1, next_message: int = 0, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
            f'CALL get_thread_list({mode}, {next_message})'
        )).fetchall()
        threads = []
        if result:
            for thread in result:
                    threads.append(dict(thread._mapping))
        return form_response("SUCCESS", threads)

@app.get("/{scheme}/get_lobby", dependencies=[Depends(is_authenticated)])
async def get_lobby(id_room: int, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        result = connection.execute(text(
        "SELECT players, max_players, ip, password, "
        "(SELECT nick "
        "FROM players "
        "WHERE players.player_id = lobbies.host_id) "
        "AS nick, host_id "
        "FROM lobbies "
        f"WHERE id = {id_room} LIMIT 1")).fetchone()
        if result:
            return form_response("SUCCESS", dict(result._mapping))
        return form_response("ERROR", "LOBBY_NOT_FOUND")

@app.get("/{scheme}/mail", dependencies=[Depends(is_authenticated)])
async def mail(messageID: int, sent: str | None = None, readable: str | None = None, delete: str | None = None, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
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
            return form_response("SUCCESS", mail)
        return form_response("ERROR", "USER_NOT_FOUND")

@app.get("/{scheme}/send_mail", dependencies=[Depends(is_authenticated)])
async def send_mail(send_to: str, subject: str, message: str, send: str | None, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
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
                            return form_response("ERROR", "INVALID_RECIPIENT")
                    if subject and message:
                        connection.execute(text(
                            "INSERT INTO mail_messages "
                            "(id_from, id_to, subject, content) "
                            "VALUES "
                            f"({common['player_id']}, {id._mapping}, \"{subject}\", \"{message}\")"
                        ))
                        connection.commit()
                else:
                    return form_response("ERROR", "RECIPIENT_NOT_FOUND")
            return form_response("SUCCESS", summary)
        return form_response("ERROR", "USER_NOT_FOUND")

@app.get("/{scheme}/view_mail", dependencies=[Depends(is_authenticated)])
async def view_mail(messageID: int = 1, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
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
                return form_response("SUCCESS", {
                        "summary": dict(summary),
                        "message": dict(message)
                })
        return form_response("ERROR", "USER_NOT_FOUND")

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
        return form_response("SUCCESS", news)

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
        return form_response("SUCCESS", punishments)

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
        return form_response("SUCCESS", scored_games)

@app.get("/{scheme}/get_user_details", dependencies=[Depends(is_authenticated)])
async def get_user_details(ID: str, common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
        profile = connection.execute(text(
            f"CALL get_user_details({ID})"
        )).fetchone()
        if profile:
            profile = profile._mapping
            can_be_excluded = connection.execute(text(
                f"CALL can_be_excluded({ID}, {common['player_id']})"
            )).fetchone()

            return form_response("SUCCESS", [
                {
                "profile": dict(profile),
                "can_be_excluded": True if can_be_excluded else False
                }
            ])
        return form_response("ERROR", "USER_NOT_FOUND")

@app.get("/{scheme}/get_user_list", dependencies=[Depends(is_authenticated)])
async def get_user_list(page: int = 0, resort: int | None = None, order: str = "1", common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    order_by = "players." + order if order in ("nick", "name", "id", "country", "score") else "players.score"
    order = 'DESC' if resort == '1' else 'ASC'
    with engine.connect() as connection: #type: ignore
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
        return form_response("SUCCESS", users)

@app.get("/{scheme}/get_poll", dependencies=[Depends(is_authenticated)])
async def get_poll(common: dict = Depends(common_parameters)) -> Dict[str, Any]:
    engine = conn.get(common["scheme"])
    with engine.connect() as connection: #type: ignore
            result = connection.execute(text(
            f"SELECT id, subject, published_at FROM votes;"
            )).fetchone()
            if result:
                return form_response("SUCCESS", dict(result._mapping))
    return form_response("ERROR", "POLL_NOT_FOUND")

@app.get("/{path:path}")
@app.get("/")
async def invalid(_: str | None = None):
    return form_response("ERROR", "INVALID_REQUEST")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)