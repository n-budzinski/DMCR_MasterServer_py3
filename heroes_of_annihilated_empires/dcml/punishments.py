import sqlalchemy

def punishments(database: sqlalchemy.Engine):
    with database.connect() as connection:
        punishment_list = []
        punishments = connection.execute(sqlalchemy.text("SELECT *\
                            FROM punishments ORDER BY id DESC")).fetchall()
        for idx, entry in enumerate(punishments):
            punishment = entry._mapping
            punishment_list.append("".join([
                f"#font(R2C12,BC12,RC12)",
                f"#txt[%MSG{idx+1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'},w:570,h:20],{{}},\"Cancelled game ```` (#).\")",
                f"#font(R2C12,BC12,BC12)",
                f"#txt[%DAT{idx+1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:90,h:20],{{}},\"Date:\")",
                f"#font(BC12,BC12,BC12)",
                f"#txt[%DATE{idx+1}](%SB[x:%DAT{idx+1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:200,h:20],{{}},\"04.04.2005 [07:36]\")",
                f"#font(R2C12,BC12,BC12)",
                f"#txt[%MD{idx+1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+43,w:90,h:20],{{}},\"Moderator:\")",
                f"#font(R2C12,BC12,RC12)",
                f"#txt[%MDR{idx+1}](%SB[x:%MD{idx+1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+43,w:200,h:20],{{GW|open&user_details.dcml\\00&ID=5436\\00|LW_lockall}},\"{{_5436}}\")",
                f"#font(R2C12,BC12,BC12)",
                f"#txt[%CM{idx+1}](%SB[x:210,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:100,h:20],{{}},\"Comments:\")",
                f"#font(BC12,BC12,BC12)",
                f"#txt[%CMT{idx+1}](%SB[x:%CM{idx+1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:256,h:20],{{}},\"ok\")",
                f"#pan[%P{idx+1}](%SB[x:0-32,y:%MDR{idx+1}>%CMT{idx+1}+38,w:100%+65,h:0],9)",
            ]))
    print("".join(punishment_list))

    return "".join((
    f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
    f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
    f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
    f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
    f"#font(RG18,RG18,RG18)",
    f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")",
    f"#font(BG18,BG18,BG18)",
    f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")",
    f"#font(R2C12,R2C12,R2C12)",
    f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
    f"#font(RC12,RC12,RC12)",
    f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
    f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")",
    f"#hint(%BT1,\"News, events, forum and punishment list\")",
    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)	     ",
    f"#font(RC12,R2C12,RC12)",
    f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
    f"#hint(%BT2,\"Player list, personal mail and clan information\")",
    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)	     ",
    f"#font(RC12,R2C12,RC12)",
    f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")",
    f"#hint(%BT4,\"Play custom games\")",
    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)	     ",
    f"#font(RC12,R2C12,RC12)",
    f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
    f"#hint(%BT5,\"Played games and their scores\")"
    f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)",
    f"<VOTING>",
    f"#exec(GW|open&voting.dcml\\00&question=46\\00)",
    f"<VOTING>",
    f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
    f"#font(RC14,R2C14,RC14)",
    f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")",
    f"#font(RC14,GC14,RC14)",
    f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")",
    f"#hint(%LIST2,\"List of punished players\")",
    f"#font(R2C14,R2C14,RC14)",
    f"#edit[%E_FT](%B[x:0,y:0,w:0,h:0],{{%GV_FORUM_LAST_TIME}})",
    f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=<%GV_FORUM_LAST_TIME>\\00|LW_lockall}},\"{{Forum}}\")",
    f"#hint(%LIST3,\"Read and write forum messages\")",
    f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)",
    f"#sbox[%SB](x:150,y:46,w:526+4,h:291-8)",
    "".join(punishment_list),
    f"<NGDLG>",
    f"<NGDLG>",
    f"#block(cancel.cml,CAN)",
    f"<NGDLG>",
    f"<NGDLG>",
    f"#end(CAN)"))