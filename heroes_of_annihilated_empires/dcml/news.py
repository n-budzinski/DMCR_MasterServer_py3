import sqlalchemy
from datetime import datetime

def news(database: sqlalchemy.Engine):
    news = None
    with database.connect() as connection:
        news = connection.execute(sqlalchemy.text(f"SELECT posted_at, content FROM news ORDER BY id DESC")).fetchall()
    news_board = []
    if news:
        news_board.append(f"\
                    #font(BC12,BC12,RC12)\
                    #txt[%TEXT0](%SB[x:85,y:8,w:100%-90,h:24],{{}},\"{news[0][1]}\")\
                    #font(BC14,BC14,RC14)\
                    #ctxt[%DATE0](%SB[x:0,y:8,w:78,h:24],{{}},\
                    {' - ' if not isinstance(news[0][0], datetime) else news[0][0].strftime('%d/%m/%Y')})") # type: ignore
        if len(news) > 1:
            for idx, n in enumerate(news[1:]):
                news_board.append(f"\
                    #font(BC12,BC12,RC12)\
                    #txt[%TEXT{idx+1}](%SB[x:85,y:%TEXT{idx}+27,w:100%-90,h:24],{{}},\"{n[1]}\")\
                    #font(BC14,BC14,RC14)\
                    #ctxt[%DATE{idx+1}](%SB[x:0,y:%TEXT{idx}+27,w:78,h:24],{{}},\
                    {' - ' if not isinstance(news[0][0], datetime) else n[0].strftime('%d/%m/%Y')})") # type: ignore
    news_board = "".join(news_board)
    return "".join((
    f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
    f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
    f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
    f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
    f"#font(RG18,RG18,RG18)",
    f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")\"",
    f"#font(BG18,BG18,BG18)",
    f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")",
    f"#font(R2C12,R2C12,R2C12)",
    f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
    f"#font(RC12,RC12,RC12)",
    f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
    f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{}},\"News & Events\")",
    f"#hint(%BT1,\"News, events, forum and punishment list\")",
    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
    f"#font(RC12,R2C12,RC12)",
    f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
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
    f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")",
    f"#font(R2C14,R2C14,RC14)",
    f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")",
    f"#hint(%LIST2,\"List of punished players\")",
    f"#edit[%E_FT](%B[x:0,y:0,w:0,h:0],{{%GV_FORUM_LAST_TIME}})",
    f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=<%GV_FORUM_LAST_TIME>\\00|LW_lockall}},\"{{Forum}}\")",
    f"#hint(%LIST3,\"Read and write forum messages\")",
    f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)",
    f"#sbox[%SB](x:150,y:46,w:526+4,h:291-8)",
    f"{news_board}",
    f"#ebox[%B1](x:0,y:0,w:100%,h:100%)",
    f"#pan[%PANV](%B1[x:260,y:8,w:0,h:359],10)",
    f"<NGDLG>",
    f"<NGDLG>",
    f"#block(cancel.cml,CAN)<NGDLG>",
    f"<NGDLG>",
    f"#end(CAN)"
))