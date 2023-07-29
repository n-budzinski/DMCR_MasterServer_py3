import sqlalchemy

def new_game_dlg(database: sqlalchemy.Engine):
    types = None
    with database.connect() as connection:
        result = connection.execute(sqlalchemy.text(f"SELECT name FROM lobby_types"))
        types = result.fetchall()
    return " ".join((
        f"<NGDLG>",
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)",
        # f"#exec(LW_cfile&{player.nickname}\\00&Bastet/%GV_VE_TITLE)",
        f"#exec(LW_cfile&\\00&Bastet/%GV_VE_PASSWD)",
        f"#exec(LW_cfile&\\00&Bastet/%GV_VE_MAX_PL)",
        f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&new_game_dlg_create.dcml\\00&max_players=<%GV_VE_MAX_PL>^type=<%GV_VE_TYPE>^password=<%GV_VE_PASSWD>^title=<%GV_VE_TITLE>\\00|LW_lockall}}{{GW|open&cancel.dcml\\00|LW_lockall}},1,0,13,252,\"CREATE NEW GAME\",,26,\"Create\",\"Cancel\")",
        f"#ebox[%L](x:245,y:100,w:450,h:210)",
        f"#font(BC12,RC12,RC12)",
        f"#txt[%L_NAME](%L[x:11,y:48,w:160,h:20],{{}},\"Game Title:\")",
        f"#pan[%P_NAME](%L[x:15,y:68,w:382,h:14],1)",
        f"#font(BC12,GC12,GC12)",
        f"#edit[%E_NAME](%L[x:19,y:67,w:377,h:18],{{%GV_VE_TITLE}},0,0,0,1)",
        f"#font(BC12,RC12,RC12)",
        f"#txt[%L_PASS](%L[x:11,y:95,w:160,h:20],{{}},\"Password:\")",
        f"#pan[%P_PASS](%L[x:15,y:114,w:382,h:14],1)",
        f"#font(BC12,GC12,GC12)",
        f"#edit[%E_PASS](%L[x:19,y:113,w:377,h:18],{{%GV_VE_PASSWD}},0,0,1)",
        f"#font(BC14,RC14,RC14)",
        f"#txt[%L_MAXPL](%L[x:11,y:145,w:150,h:24],{{}},\"Max Players:\")",
        f"#cbb[%E_MAXPL](%L[x:130,y:139,w:273,h:24],{{%GV_VE_MAX_PL}},2,3,4,5,6,7,0)",
        f"#font(BC14,RC14,RC14)",
        f"#txt[%L_MAXPL](%L[x:11,y:175,w:151,h:24],{{}},\"Type:\")",
        f"#cbb[%E_TYPE](%L[x:130,y:169,w:273,h:24],{{%GV_VE_TYPE}},{''.join([f'{type[0]},' for type in types])})",
        # f"{''.join([f'{_type.name},' for _type in gameTypes.types])}"
        f"<NGDLG>"))