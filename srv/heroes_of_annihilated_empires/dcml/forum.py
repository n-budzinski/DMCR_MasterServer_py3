import sqlalchemy

def forum(options, database: sqlalchemy.Engine, player_id):
    with database.connect() as connection:
        thread_list = []

        if options["mode"] == "1":
            threads = connection.execute(sqlalchemy.text(f"""SELECT id, author_id, created_at, content, (SELECT COUNT(*) AS count FROM thread_messages WHERE thread_messages.thread_id = threads.id) AS messages\
                FROM threads ORDER BY id DESC LIMIT 31 OFFSET {int(options["next_message"]) if options["next_message"] else 0}""")).fetchall()

        elif options["mode"] == "2":
            threads = connection.execute(sqlalchemy.text(f"""SELECT *\
                FROM thread_messages ORDER BY id DESC LIMIT 10""")).fetchall()

        elif options["mode"] == "3":
            threads = connection.execute(sqlalchemy.text(f"""SELECT *\
                FROM thread_messages WHERE created_at > now() - interval 1 day ORDER BY id DESC""")).fetchall()

        elif options["mode"] == "4":
            threads = connection.execute(sqlalchemy.text(f"""SELECT *\
                FROM thread_messages WHERE created_at > now() - interval 7 day ORDER BY id DESC""")).fetchall()

        else:
            threads = []

        for idx, entry in enumerate(threads[:30]):
            thread = entry._mapping
            thread_list.append("".join([
                f"#font(BC12,RC12,RC12)",
                f"#txt[%TXT{idx+1}](%SB[x:218,y:{'4' if idx == 0 else f'%P{idx}-21'},w:100%-215,h:24],{{}},\"{thread['content']}\")",
                f"#exec(LW_vis&0&%TXT2)",
                f"#apan[%PAN{idx+1}](%SB[x:0,y:{'4' if idx == 0 else f'%P{idx}-21'}-10,w:100%,y1:{'4' if idx == 0 else f'%P{idx}-21'}+{'42' if options['mode'] == '1' else '28'}>%TXT{idx+1}+5],{{GW|open&forum_view.dcml\\00&last_view=0^theme=9382\\00|LW_lockall}},14,\"\")",
                f"#font(BC12,RC12,RC12)",
                f"#txt[%TEXT{idx+1}](%SB[x:218,y:{'4' if idx == 0 else f'%P{idx}-21'},w:100%-220,h:24],{{}},\"{thread['content']}\")",
                f"#font(R2C12,R2C12,RC12)",
                f"#txt[%S_DATE{idx+1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'},w:170,h:24],{{}},\"Date:\")",
                f"#font(BC12,R2C12,RC12)",
                f"#txt[%DATE{idx+1}](%SB[x:%S_DATE{idx+1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'},w:170,h:24],{{}},\"{thread['created_at']}\")",
                f"#font(R2C12,BC12,RC12)",
                f"#txt[%S_CR{idx+1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+14,w:170,h:24],{{}},\"Author:\")",
                f"#txt[%CR{idx+1}](%SB[x:%S_CR{idx+1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+14,w:170,h:24],{{GW|open&user_details.dcml\\00&ID=73858\\00|LW_lockall}},\"{{{thread['author_id']}}}\")",
                f"#txt[%S_COU{idx+1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+28,w:170,h:24],{{}},\"Message:\")#font(BC12,BC12,BC12)#txt[%COU{idx+1}](%SB[x:%S_COU{idx+1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+28,w:170,h:24],{{}},\"{thread['messages']}\")" if options["mode"] == "1" else "",
                f"#pan[%P{idx+1}](%SB[x:0-32,y:{'4' if idx == 0 else f'%P{idx}-21'}+{'42' if options['mode'] == '1' else '28'}>%TEXT{idx+1}+38,w:100%+65,h:0],9)",
            ]))
    print(len(thread_list))
    return "".join((
    f"#exec(LW_cfile&20230722144507&Cookies/%GV_FORUM_LAST_TIME)",
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
    f"#ebox[%B](x:0,y:0,w:100%,h:10%)",
    f"#font(R2C14,R2C14,RC14)",
    f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")",
    f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")",
    f"#hint(%LIST2,\"List of punished players\")",
    f"#font(RC14,GC14,RC14)",
    f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=0\\00|LW_lockall}},\"{{Forum}}\")",
    f"#hint(%LIST3,\"Read and write forum messages\")",
    f"##font(RC12,GC12,RC12)" if options['mode'] == "1" else "#font(RC12,R2C12,RC12)",
    f"#ctxt[%LIST4](%B[x:0,y:%LIST3-10,w:146,h:24],{{GW|open&forum.dcml\\00&mode=1^last_view=0\\00|LW_lockall}},\"{{All themes}}\")",
    f"##font(RC12,GC12,RC12)" if options['mode'] == "2" else "#font(RC12,R2C12,RC12)",
    f"#ctxt[%LIST5](%B[x:0,y:%LIST4-1,w:146,h:24],{{GW|open&forum.dcml\\00&mode=2^last_view=0\\00|LW_lockall}},\"{{Last 10 messages}}\")",
    f"##font(RC12,GC12,RC12)" if options['mode'] == "3" else "#font(RC12,R2C12,RC12)",
    f"#ctxt[%LIST6](%B[x:0,y:%LIST5-1,w:146,h:24],{{GW|open&forum.dcml\\00&mode=3^last_view=0\\00|LW_lockall}},\"{{Messages for this day}}\")",
    f"##font(RC12,GC12,RC12)" if options['mode'] == "4" else "#font(RC12,R2C12,RC12)",
    f"#ctxt[%LIST7](%B[x:0,y:%LIST6-1,w:146,h:24],{{GW|open&forum.dcml\\00&mode=4^last_view=0\\00|LW_lockall}},\"{{Messages for this week}}\")",
    f"#font(RC12,R2C12,RC12)",
    f"#ctxt[%LIST8](%B[x:0,y:%LIST7-1,w:146,h:24],{{GW|open&forum_add.dcml\\00&last_view=0\\00|LW_lockall}},\"{{Add theme}}\")",
    f"#hint(%LIST8,\"Create a new forum theme\")",
    f"#font(RC12,R2C12,RC12)",
    f"#ctxt[%LIST9](%B[x:0,y:%LIST8-1,w:146,h:24],{{GW|open&forum_search.dcml\\00&last_view=0\\00|LW_lockall}},\"{{Search}}\")",
    f"#hint(%LIST9,\"Search a message by author or text\")",
    f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)",
    f"#sbox[%SB](x:150,y:42+4,w:526+4,h:291-8)",
    
    "".join(thread_list) if thread_list else "".join([
        f"#ebox[%B1](x:0,y:0,w:100%,h:100%)",
        f"#pan[%PAN0](%B1[x:390,y:8,w:0,h:359],10)",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%BT3](%B[x:684,y:377,w:15,h:305],{{GW|open&forum.dcml\\00&mode=^message_total=3246^next_message={int(options['next_message']) + 30 if options['next_message'] else 0}^last_view=0^search_nick=^search_text=\\00|LW_lockall}},\"Next\")" if len(threads) > 29 else "",
    ]) if threads else "".join([
            f"#font(RG18,RG18,RG18) ",
            f"#ctxt[%T0](%B[x:154,y:179,w:523,h:20],{{}},\"No search results\")",
            ]),

    f"<NGDLG><NGDLG>",
    f"#block(cancel.cml,CAN)",
    f"<NGDLG>",
    f"<NGDLG>",
    f"#end(CAN)"))