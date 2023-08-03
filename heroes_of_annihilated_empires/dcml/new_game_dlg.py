import sqlalchemy

def new_game_dlg(database: sqlalchemy.Engine):
    types = None
    with database.connect() as connection:
        result = connection.execute(sqlalchemy.text(f"SELECT name FROM lobby_types"))
        types = result.fetchall()
    return " ".join((
        f"<NGDLG> ",
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%) ",
        # f"#exec(LW_cfile&hardkode1\\00&Cookies/%GV_VE_TITLE) ",
        f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASSWD) ",
        f"#exec(LW_cfile&0\\00&Cookies/%GV_VE_MAX_PL) ",
        f"#table[%TBL](%L0[x:196,y:105,w:450,h:200],{{}}{{}}{{GW|open&new_game_dlg_create.dcml\\00&max_players=<%GV_VE_MAX_PL>^type=<%GV_VE_TYPE>^password=<%GV_VE_PASSWD>^title=<%GV_VE_TITLE>\\00|LW_lockall}}{{GW|open&cancel.dcml\\00|LW_lockall}},1,0,11,362,\"CREATE NEW GAME\",,24,\"Create\",\"Cancel\") ",
        # f"//#ctxt[%L_DUMMY](%L0[x:196,y:83,w:450,h:20],{{}},\"CREATE NEW GAME\") ",
        f"#ebox[%L](x:210,y:74,w:450,h:210) ",
        f"#font(BC14,RC14,RC14) ",
        f"#txt[%L_NAME](%L[x:15,y:52,w:180,h:20],{{}},\"Game Title:\") ",
        f"#pan[%P_NAME](%L[x:15,y:72,w:392,h:18],3) ",
        f"#font(BC12,GC12,GC12) ",
        f"#edit[%E_NAME](%L[x:19,y:73,w:384,h:18],{{%GV_VE_TITLE}},0,0,0,1) ",
        f"#font(BC14,RC14,RC14) ",
        f"#txt[%L_PASS](%L[x:15,y:98,w:180,h:20],{{}},\"Password:\") ",
        f"#pan[%P_PASS](%L[x:15,y:118,w:392,h:18],3) ",
        f"#font(BC12,GC12,GC12) ",
        f"#edit[%E_PASS](%L[x:19,y:119,w:384,h:18],{{%GV_VE_PASSWD}},0,0,1) ",
        f"#font(BC14,RC14,RC14) ",
        f"#txt[%L_MAXPL](%L[x:15,y:151,w:160,h:24],{{}},\"Max Players\") ",
        f"#cbb[%E_MAXPL](%L[x:161,y:147,w:247,h:24],{{%GV_VE_MAX_PL}},2,3,4,5,6,0) ",
        f"#font(BC14,RC14,RC12) ",
        f"#txt[%L_TYPE](%L[x:15,y:181,w:160,h:24],{{}},\"Type\") ",
        # f"#cbb[%E_TYPE](%L[x:161,y:177,w:247,h:24],{{%GV_VE_TYPE}},Rating Game,Custom Game,0) ",
        f"#cbb[%E_TYPE](%L[x:161,y:177,w:247,h:24],{{%GV_VE_TYPE}},{''.join([f'{type[0]},' for type in types])})",
        f"#def_combo_fix(%GV_VE_MAX_PL,%GV_VE_TYPE,1) ",
        f"<NGDLG>"))