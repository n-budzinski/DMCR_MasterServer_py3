import sqlalchemy

def forum_view(options, database: sqlalchemy.Engine):
    with database.connect() as connection:
        if options['thread']:
            thread = connection.execute(sqlalchemy.text(f"""SELECT id, created_at, author_id, content FROM threads WHERE id = {options['thread']} LIMIT 1""")).fetchone()
            if thread:
                thread = thread._mapping
                messages = connection.execute(sqlalchemy.text(f"""SELECT * FROM thread_messages WHERE thread_id = {thread['id']} ORDER BY id ASC"""))
                message_list = []
                for idx, entry in enumerate(messages):
                        message = entry._mapping
                        message_list.append("".join([
                            f"#font(R2C12,R2C12,RC12)",
                            f"#txt[%S_DATE{idx+1}](%SB[x:7,y:{'6' if idx == 0 else f'%P{idx}-22'},w:170,h:24],{{}},\"Date:\")",
                            f"#font(BC12,R2C12,RC12)",
                            f"#txt[%DATE{idx+1}](%SB[x:%S_DATE{idx+1}+5,y:{'6' if idx == 0 else f'%P{idx}-22'},w:170,h:24],{{}},\"{message['created_at']}\")",
                            f"#font(R2C12,BC12,RC12)",
                            f"#txt[%S_CR{idx+1}](%SB[x:7,y:{'6' if idx == 0 else f'%P{idx}-22'}+14,w:170,h:24],{{}},\"Author:\")",
                            f"#txt[%CR{idx+1}](%SB[x:%S_CR{idx+1}+5,y:{'6' if idx == 0 else f'%P{idx}-22'}+14,w:170,h:24],{{GW|open&user_details.dcml\\00&ID=38682\\00|LW_lockall}},\"{{{message['author_id']}}}\")",
                            f"#font(BC12,RC12,RC12)",
                            f"#txt[%TEXT{idx+1}](%SB[x:215,y:{'6' if idx == 0 else f'%P{idx}-22'},w:100%-220+0,h:24],{{}},\"{message['content']}\")",
                            f"#pan[%P{idx+1}](%SB[x:0-32,y:%CR{idx+1}>%TEXT{idx+1}+37,w:100%+65,h:0],9)",
                        ]))
    
                return "".join([
                f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
                f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
                f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
                f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
                f"#font(RG18,RG18,RG18)",
                f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")",
                f"#font(BG18,BG18,BG18)",
                f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")",
                f"#font(R2C12,R2C12,R2C12)",
                f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")  ",
                f"#font(RC12,RC12,RC12)  ",
                f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
                f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")",
                f"#hint(%BT1,\"News, events, forum and punishment list\")",
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
                f"#font(RC12,R2C12,RC12)  ",
                f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
                f"#hint(%BT2,\"Player list, personal mail and clan information\")",
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)  ",
                f"#font(RC12,R2C12,RC12)  ",
                f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")",
                f"#hint(%BT4,\"Play custom games\")",
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)  ",
                f"#font(RC12,R2C12,RC12)  ",
                f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
                f"#hint(%BT5,\"Played games and their scores\") ",
                f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103) <VOTING> ",
                f"#exec(GW|open&voting.dcml\\00&question=46\\00) <VOTING>",
                f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
                f"#font(R2C14,R2C14,RC14)",
                f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\") ",
                f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\") ",
                f"#hint(%LIST2,\"List of punished players\") ",
                f"#font(RC14,GC14,RC14)",
                f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=\\00|LW_lockall}},\"{{Forum}}\")",
                f"#hint(%LIST3,\"Read and write forum messages\") ",
                f"#font(RC12,R2C12,RC12) ",
                f"#ctxt[%LIST4](%B[x:0,y:%LIST3-10,w:146,h:24],{{GW|open&forum_add.dcml\\00&theme=4259^last_view=\\00|LW_lockall}},\"{{Add message}}\")",
                f"#hint(%LIST4,\"Write new post on current theme\") ",
                f"#ctxt[%LIST5](%B[x:0,y:%LIST4-1,w:146,h:24],{{GW|open&forum_search.dcml\\00&last_view=\\00|LW_lockall}},\"{{Search}}\") ",
                f"#hint(%LIST5,\"Search a message by author or text\")",
                f"#ebox[%B01](x:154,y:42,w:559,h:291)",
                f"#font(GC12,R2C12,RC12)",
                f"#txt[%TEXT01](%B01[x:220,y:7,w:330+0,h:24],{{}},\"D2BUTANT SUR INTERNET QUI VEUT JOUER\")",
                f"#exec(LW_vis&0&%TEXT01)",
                f"#pan[%PAN_T](%B01[x:0,y:0,w:100%,y1:%TEXT01>35+3],7)",
                f"#pan[%PAN01](%B01[x:245,y:0-34,w:0,y1:%PAN_T+34],10)",
                f"#font(R2C12,R2C12,RC12)",
                f"#txt[%S_DATE0](%B01[x:8,y:7,w:170,h:24],{{}},\"Date:\")",
                f"#font(BC12,R2C12,RC12)",
                f"#txt[%DATE0](%B01[x:%S_DATE0+5,y:7,w:170,h:24],{{}},\"22.07.2006 [19:30]\")",
                f"#font(R2C12,BC12,RC12)",
                f"#txt[%S_CR0](%B01[x:8,y:21,w:170,h:24],{{}},\"Author:\")",
                f"#txt[%CR0](%B01[x:%S_CR0+5,y:21,w:170,h:24],{{GW|open&user_details.dcml\\00&ID=38521\\00|LW_lockall}},\"{{[MAC2DOIN]gilles}}\")",
                f"#font(GC12,R2C12,RC12)",
                f"#txt[%TEXT0](%B01[x:220,y:7,w:330+0,h:24],{{}},\"D2BUTANT SUR INTERNET QUI VEUT JOUER\")",
                f"#pan[%PAN](%B01[x:0,y:%PAN_T+10,w:559,y1:D],5)",
                f"#pan[%PAN](%B01[x:9,y:%PAN_T+19,w:526-17,y1:D-9],3)",
                f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-4,8)",
                f"#sbox[%SB](%B01[x:7,y:%PAN_T+20,w:526-14,y1:D-11])",
                f"#pan[%PAN0](%B01[x:245,y:%PAN_T-15,w:0,y1:%PAN+34],10)",
                "".join(message_list),
                f"#font(BC14,WC14,BC14)",
                f"#sbtn[%BTXT1](%B[x:641,y:377,w:100,h:305],{{<!goback!>}},\"Back\")<NGDLG><NGDLG>",
                f"#block(cancel.cml,CAN)<NGDLG><NGDLG>",
                f"#end(CAN)"])
            else:
                return ""