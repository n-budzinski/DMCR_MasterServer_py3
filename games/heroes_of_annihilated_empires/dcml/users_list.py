import sqlalchemy

def users_list(options, database: sqlalchemy.Engine):
    page=options.get("next_user", 0)
    resort=options.get("resort", "1")
    order = options.get("order", "score")
    if order == 'nick':
        order = 'players.nick'
    elif order == 'name':
        order = 'players.name'
    elif order == 'id':
        order = 'players.player_id'
    elif order == 'country':
        order = 'players.country'
    else:
        order = 'players.score'
    
    players = None
    with database.connect() as connection:
        players = connection.execute(sqlalchemy.text(f"SELECT players.nick, players.name, players.player_id, countries.name, players.score, clan_ranks.name, row_number()\
                        OVER ( order by players.score {'DESC' if order == 'players.score' and resort == '0' else 'ASC'} ) AS 'pos'\
                        FROM players\
                        INNER JOIN clan_ranks ON players.clan_rank = clan_ranks.id\
                        LEFT JOIN countries ON players.country = countries.id - 1\
                        ORDER BY {order} DESC LIMIT 14 OFFSET {13*page};")).fetchall()
    return "".join((
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
        f"#font(RG18,RG18,RG18)",
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")\"",
        f"#font(BG18,BG18,BG18)",
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\")",
        f"#font(R2C12,R2C12,R2C12)",
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")",
        f"#hint(%BT1,\"News, events, forum and punishment list\")",
        f"#font(RC12,RC12,RC12)",
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
        f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{}},\"Player List\")",
        f"#hint(%BT2,\"Player list, personal mail and clan information\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")",
        f"#hint(%BT4,\"Play custom games\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
        f"#hint(%BT5,\"Played games and their scores\")",
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)",
        f"<VOTING>",
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)",
        f"<VOTING>",
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
        f"#font(RC14,GC14,RC14)",
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\")",
        f"#font(R2C12,R2C12,RC12)",
        f"#ctxt[%LIST10](%B[x:0,y:%LIST1-10,w:146,h:24],{{GW|open&mail_list.dcml\\00|LW_lockall}},\"{{Mail}}\")",
        f"#hint(%LIST10,\"Manage your personal mail\")",
        f"#font(RC14,R2C14,RC14)",
        f"#ctxt[%LIST2](%B[x:0,y:%LIST10+7,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\")",
        f"#hint(%LIST2,\"Clans, their members and details\")",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%BT](%B[x:401,y:377,w:100,h:305],{{GW|open&users_list.dcml\\00&page=0^order=score^resort=1\\00|LW_lockall}},\"First Page\")" if page != 0 else "",
        f"#sbtn[%BT](%B[x:521,y:377,w:100,h:305],{{<!goback!>}},\"Back\")" if page != 0 else "",
        f"#font(R0C14,R0C14,R0C14)",
        f"#pix[%BTXT10](%B[x:602,y:353,w:118,h:25],{{}},Internet/pix/i_pri0,54,54,54,54)",
        f"#ctxt[%BTIT10](%B[x:602,y:359,w:118,h:20],{{}},\"Next\")",
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%)",
        f"#font(RC12,R2C12,RC12)",
        f"#stbl[%TIT](%BB[x:154,y:42,w:559,h:291],",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=score^resort={'1' if order == 'players.score' and resort == '0' else '0'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=nick^resort={'0' if order == 'players.nick' and resort == '1' else '1'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=name^resort={'0' if order == 'players.name' and resort == '1' else '1'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=id^resort={'0' if order == 'players.player_id' and resort == '1' else '1'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=country^resort={'0' if order == 'players.country' and resort == '1' else '1'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=score^resort={'0' if order == 'players.score' and resort == '1' else '1'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=score^resort={'0' if order == 'players.score' and resort == '1' else '1'}\\00|LW_lockall}},7,7,7,1,21,1,25,1,6,1,15,1,7,1,19,1,20,\"{{Pos\",\"{{Nickname\",\"{{Full Name\",\"{{#\",\"{{Country\",\"{{Scores\",\"{{Rank\")",
        "".join([f"#apan[%APAN0](%BB[x:150,y:{60+(21*idx)}-1,w:100%-161,h:20],{{GW|open&user_details.dcml\\00&ID={player[2]}\\00|LW_lockall}},8)" for idx, player in enumerate(players[:13])]),
        f"#font(BC12,BC12,BC12)",
        f"#stbl[%TBL](%BB[x:154,y:42+18,w:559,h:270],{{}},7,0,7,1,21,1,25,1,6,1,15,1,7,1,19,1,",
        "".join([f"21,\"{player[6]}\",\"{player[0]}\",\"{player[1]}\",\"{player[2]}\",\"{player[3]}\",\"{player[4]}\",\"{player[5]}\"," for idx, player in enumerate(players[:13])]),
        f")",
        f"#font(RC12,R2C12,RC12)",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%BT](%BB[x:641,y:377,w:100,h:305],{{GW|open&users_list.dcml\\00&page={page+1}^order={order}^resort=\\00|LW_lockall}},\"Next\")" if len(players) > 13 else '',
        f"<NGDLG>",
        f"<NGDLG>",
        f"#block(cancel.cml,CAN)<NGDLG>",
        f"<NGDLG>",
        f"#end(CAN)"
    ))