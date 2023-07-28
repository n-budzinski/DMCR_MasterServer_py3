import sqlalchemy

def forum_add(options, database: sqlalchemy.Engine, player_id):
    if options['add_message']:
        try:
            with database.connect() as connection:
                if options['theme']:
                    connection.execute(sqlalchemy.text(f'INSERT INTO threads_messages (author_id, thread_id, content) VALUES ({player_id}, {options["theme"]}, "{options["add_message"]}")'))
                else:
                    connection.execute(sqlalchemy.text(f'INSERT INTO threads (author_id, content) VALUES ({player_id}, "{options["add_message"]}")'))
                connection.commit()
        finally:
            return "#exec(GW|open&forum.dcml\\00&mode=1^last_view=^noback=true\\00|LW_lockall)"
    return "".join((
    f"#block(l_games_btn.cml,l_g):<!goback!>\\00",
    f"#end(l_g)",
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
    f"#font(R2C14,R2C14,RC14)",
    f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")",
    f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")",
    f"#hint(%LIST2,\"List of punished players\")",
    f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=\\00|LW_lockall}},\"{{Forum}}\")",
    f"#hint(%LIST3,\"Read and write forum messages\")",
    f"#font(RC12,GC12,RC12)  ",
    f"#ctxt[%LIST4](%B[x:0,y:%LIST3-10,w:146,h:24],{{GW|open&forum_add.dcml\\00&cansel=true^theme=^last_view=\\00|LW_lockall}},\"{{Add theme}}\")",
    f"#hint(%LIST4,\"Create a new forum theme\")",
    f"#exec(LW_cfile&\\00&Cookies/%GV_MESSAGE)",
    f"#ebox[%B0](x:154,y:42,w:559,h:291)",
    f"#pan[%PAN](%B0[x:0,y:0,w:100%,h:100%],5)",
    f"#font(RC14,R2C14,RC14)",
    f"#txt[%TOP1](%B0[x:4,y:5,w:150,h:24],{{}},\"Add theme\")",
    f"#pix[%PX](%B0[x:4,y:27,w:100%,h:100%],{{}},Internet/pix/i_pri0,25,25,25,25)",
    f"#font(R2C12,R2C12,RC12)",
    f"#txt[%TOP2](%B0[x:4,y:41,w:150,h:24],{{}},\"Theme:\")",
    f"#font(BC12,GC12,GC12)",
    f"#pan[%PAN](%B0[x:8,y:60,w:543,h:218],1)",
    f"#edit[%NEWS](%B0[x:13,y:60,w:535,h:218],{{%GV_MESSAGE}},1,0,0,1)",
    f"#font(BC14,WC14,BC14)",
    f"#sbtn[%BT](%B[x:521,y:377,w:100,h:305],{{GW|open&forum_add.dcml\\00&cansel=true^last_view=^mode=1^add_message=<%GV_MESSAGE>\\00|LW_lockall}},\"Save\")",
    f"#sbtn[%BT](%B[x:641,y:377,w:100,h:305],{{LW_file&Internet/Cash/l_games_btn.cml}},\"Cancel\")<NGDLG><NGDLG>",
    f"#block(cancel.cml,CAN)",
    f"<NGDLG><NGDLG>",
    f"#end(CAN)"))