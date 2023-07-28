import sqlalchemy

def leave_lobby(player_id: str, database: sqlalchemy.Engine):
    with database.connect() as connection:
        connection.execute(sqlalchemy.text(f"DELETE FROM lobbies WHERE host_id={player_id};"))
        connection.commit()
    return