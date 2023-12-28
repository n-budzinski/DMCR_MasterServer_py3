import sqlalchemy

def create_game(options: dict, player_id, address, database: sqlalchemy.Engine):
    gameTitle = options.get('title', 'Lobby')
    gameType = options.get('type', 0)
    with database.connect() as connection:
        output = connection.execute(sqlalchemy.text(f"SELECT allow_designed, allow_ai FROM lobby_types WHERE id = {gameType} LIMIT 1")).fetchone()
        if output:
            allow_designed, allow_ai = output
        else:
            allow_designed, allow_ai = False, False
        gameMaxPlayers = int(options['max_players'])+2
        password = options.get('password', '')
        print(player_id)
        result = connection.execute(sqlalchemy.text(f'INSERT INTO lobbies\
                    (title,\
                    host_id,\
                    type,\
                    max_players,\
                    password,\
                    ip)\
                    VALUES ("{gameTitle}",\
                    "{player_id}",\
                    "{gameType}",\
                    "{gameMaxPlayers}",\
                    "{password}",\
                    "{address}")'))
        connection.commit()
        gameID = result.lastrowid
    return "".join((
        f"<NGDLG>",
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)",
        f"#exec(LW_file&Internet/Cash/cancel.cml|LW_gvar&%GOPT&/OPT00 /OPT10 /OPT20 /OPT30 /OPT60 /PAGE{ '1' if allow_designed else '2'} /{'' if allow_ai else 'NO'}COMP&%CG_GAMEID&{gameID}&%CG_MAXPL&{gameMaxPlayers}&%CG_GAMENAME&\"{gameTitle}\"&%COMMAND&CGAME)",
        f"<NGDLG>"))