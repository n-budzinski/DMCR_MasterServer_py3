import sqlalchemy

def join_game(options, database: sqlalchemy.Engine):
    id_room = options.get("id_room", "")
    with database.connect() as connection:
            lobby = connection.execute(sqlalchemy.text(f"SELECT players, max_players, ip, password, (SELECT nick FROM players WHERE players.player_id = lobbies.host_id) as nick FROM lobbies WHERE id = {id_room} LIMIT 1")).fetchone()
    if lobby:
        if lobby.max_players <= lobby.players:
            return "".join((
                f"<NGDLG>",
                f"#ebox[%L0](x:0,y:0,w:100%,h:100%)",
                f"#pix[%PX1](%L0[x:0-62,y:0-136,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
                f"#exec(LW_enbbox&0&%L0)",
                f"#exec(LW_enbbox&0&%B)",
                f"#exec(LW_enbbox&0&%FLBOX)",
                f"#exec(LW_enbbox&0&%BP)",
                f"#exec(LW_enbbox&0&%L)",
                f"#exec(LW_enbbox&0&%BB)",
                f"#exec(LW_enbbox&0&%B1)",
                f"#exec(LW_enbbox&0&%BG)",
                f"#exec(LW_enbbox&0&%B2)",
                f"#exec(LW_enbbox&0&%BPANEL)",
                f"#exec(LW_enbbox&0&%BPANEL2)",
                f"#exec(LW_enbbox&0&%TB)",
                f"#exec(LW_enbbox&0&%B_VOTE)",
                f"#exec(LW_enbbox&0&%MBG)",
                f"#exec(LW_enbbox&0&%B0)",
                f"#exec(LW_enbbox&0&%M)",
                f"#exec(LW_enbbox&0&%LB)",
                f"#exec(LW_enbbox&0&%MB)",
                f"#exec(LW_enbbox&0&%EBG)",
                f"#exec(LW_enbbox&0&%LBX)",
                f"#exec(LW_enbbox&0&%BARDLD)",
                f"#exec(LW_enbbox&0&%BF2)",
                f"#exec(LW_enbbox&0&%B01)",
                f"#exec(LW_enbbox&0&%BF)",
                f"#exec(LW_enbbox&0&%BTABLE2)",
                f"#exec(LW_enbbox&0&%SB)",
                f"#ebox[%BTABLE](x:0,y:0,w:100%,h:100%)",
                f"#font(BC12,BC12,BC12)",
                f"#def_panel(11,Interf3/elements/b02,21,20,14,15,4,5,12,16,8,8)",
                f"#pan[%MPN](%BTABLE[x:242,y:115+15,w:415,h:220-15],11)",
                f"#pix[%PXP1](%BTABLE[x:242+20,y:115+20,w:100%,h:100%],{{}},Internet/pix/i_pri0,32,32,32,32)",
                f"#pix[%PX2](%BTABLE[x:522,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                f"#pix[%PX3](%BTABLE[x:327,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                f"#pix[%PX4](%BTABLE[x:377,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                f"#pix[%PX5](%BTABLE[x:427,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                f"#pix[%PX6](%BTABLE[x:477,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                f"#pix[%PX0](%BTABLE[x:317,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)",
                f"#pix[%PX1](%BTABLE[x:572,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)",
                f"#font(BG18,BG18,RG18)",
                f"#ctxt[%TTEXT](%BTABLE[x:242,y:115-1,w:415,h:20],{{0}},\"ERROR\")",
                f"#font(BC12,RC12,RC12)",
                f"#ctxt[%MTEXT0](%BTABLE[x:242+20,y:115+22,w:415-40,h:20],{{}},\"This lobby is full\")",
                f"#exec(LW_vis&0&%MTEXT0)",
                f"#ctxt[%MTEXT](%BTABLE[x:242+20,yc:225-3,w:415-40,h:%MTEXT0-115-159],{{}},\"This lobby is full\")",
                f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
                f"#font(WG14,BG14,WG14)",
                f"#gpbtn[%PXBT](%BTABLE[x:520-433,y:303-16,w:100%,h:70],{{GW|open&cancel.dcml\\00|LW_lockall}},\"OK\")"
                f"<NGDLG>"
            ))

        # elif lobby.host.profileID == player.profileID:
        #     id_room=options.get("id_room", "")
        #     return "".join((
        #         f"<NGDLG>",
        #         f"#exec(LW_cfile&\\00&Bastet/%GV_VE_PASSWD)",
        #         f"#ebox[%BF](x:0,y:0,w:100%,h:100%)",
        #         f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&cancel.dcml\\00&id_room={id_room}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"You cannot join your own room!\",26,\"OK\")",
        #         f"<NGDLG>",
        #     ))

        else:
            if lobby.password:
                if options.get("password", "") == "":
                    id_room=options.get("id_room", "")
                    return "".join((
                        f"<NGDLG>",
                        f"#exec(LW_cfile&\\00&Bastet/%GV_VE_PASSWD)",
                        f"#ebox[%BF](x:0,y:0,w:100%,h:100%)",
                        f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&join_game.dcml\\00&delete_old=true^id_room={id_room}^password=<%GV_VE_PASSWD>\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"JOIN\",,26,\"JOIN\",\"Cancel\")",
                        f"#ebox[%L](x:245,y:100,w:450,h:210)",
                        f"#font(BC12,RC12,RC12)",
                        f"#txt[%L_PASS](%L[x:11,y:95,w:360,h:20],{{}},\"Enter the password:\")",
                        f"#pan[%P_PASS](%L[x:15,y:114,w:382,h:14],1)",
                        f"#font(BC12,GC12,GC12)",
                        f"#edit[%E_PASS](%L[x:19,y:113,w:377,h:18],{{%GV_VE_PASSWD}},0,0,1,1)",
                        f"<NGDLG>"
                    ))
                elif options.get("password", "") != lobby.password:
                    return "".join((
                        f"<NGDLG>",
                        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)",
                        f"#pix[%PX1](%L0[x:0-62,y:0-136,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
                        f"#exec(LW_enbbox&0&%L0)",
                        f"#exec(LW_enbbox&0&%B)",
                        f"#exec(LW_enbbox&0&%FLBOX)",
                        f"#exec(LW_enbbox&0&%BP)",
                        f"#exec(LW_enbbox&0&%L)",
                        f"#exec(LW_enbbox&0&%BB)",
                        f"#exec(LW_enbbox&0&%B1)",
                        f"#exec(LW_enbbox&0&%BG)",
                        f"#exec(LW_enbbox&0&%B2)",
                        f"#exec(LW_enbbox&0&%BPANEL)",
                        f"#exec(LW_enbbox&0&%BPANEL2)",
                        f"#exec(LW_enbbox&0&%TB)",
                        f"#exec(LW_enbbox&0&%B_VOTE)",
                        f"#exec(LW_enbbox&0&%MBG)",
                        f"#exec(LW_enbbox&0&%B0)",
                        f"#exec(LW_enbbox&0&%M)",
                        f"#exec(LW_enbbox&0&%LB)",
                        f"#exec(LW_enbbox&0&%MB)",
                        f"#exec(LW_enbbox&0&%EBG)",
                        f"#exec(LW_enbbox&0&%LBX)",
                        f"#exec(LW_enbbox&0&%BARDLD)",
                        f"#exec(LW_enbbox&0&%BF2)",
                        f"#exec(LW_enbbox&0&%B01)",
                        f"#exec(LW_enbbox&0&%BF)",
                        f"#exec(LW_enbbox&0&%BTABLE2)",
                        f"#exec(LW_enbbox&0&%SB)",
                        f"#ebox[%BTABLE](x:0,y:0,w:100%,h:100%)",
                        f"#font(BC12,BC12,BC12)",
                        f"#def_panel(11,Interf3/elements/b02,21,20,14,15,4,5,12,16,8,8)",
                        f"#pan[%MPN](%BTABLE[x:242,y:115+15,w:415,h:220-15],11)",
                        f"#pix[%PXP1](%BTABLE[x:242+20,y:115+20,w:100%,h:100%],{{}},Internet/pix/i_pri0,32,32,32,32)",
                        f"#pix[%PX2](%BTABLE[x:522,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                        f"#pix[%PX3](%BTABLE[x:327,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                        f"#pix[%PX4](%BTABLE[x:377,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                        f"#pix[%PX5](%BTABLE[x:427,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                        f"#pix[%PX6](%BTABLE[x:477,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
                        f"#pix[%PX0](%BTABLE[x:317,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)",
                        f"#pix[%PX1](%BTABLE[x:572,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)",
                        f"#font(BG18,BG18,RG18)",
                        f"#ctxt[%TTEXT](%BTABLE[x:242,y:115-1,w:415,h:20],{{0}},\"ERROR\")",
                        f"#font(BC12,RC12,RC12)",
                        f"#ctxt[%MTEXT0](%BTABLE[x:242+20,y:115+22,w:415-40,h:20],{{}},\"Incorrect password!\")",
                        f"#exec(LW_vis&0&%MTEXT0)",
                        f"#ctxt[%MTEXT](%BTABLE[x:242+20,yc:225-3,w:415-40,h:%MTEXT0-115-159],{{}},\"Incorrect password!\")",
                        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
                        f"#font(WG14,BG14,WG14)",
                        f"#gpbtn[%PXBT](%BTABLE[x:520-433,y:303-16,w:100%,h:70],{{GW|open&cancel.dcml\\00|LW_lockall}},\"OK\")",
                        f"<NGDLG>"
                    ))
            id_room = options.get("id_room", "")
            return "".join((
                f"<NGDLG>",
                f"#exec(LW_cfile&\\00&Bastet/%GV_VE_PASSWD)",
                f"#ebox[%BF](x:0,y:0,w:100%,h:100%)",
                f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&cancel.dcml\\00|LW_lockall}},2,0,3,13,252,\"JOIN\",\"Connecting...\\Please, wait.\",26,\"Cancel\")",
                f"#exec(LW_gvar&%CG_GAMEID&{id_room}&%CG_MAXPL&{str(lobby.max_players)}&%CG_GAMENAME&{'namehere'}&%COMMAND&JGAME&%CG_IP&{lobby.ip}:{34000})",
                f"<NGDLG>"
                ))
    return "".join((
        f"<NGDLG>",
        f"#exec(LW_cfile&\\00&Bastet/%GV_VE_PASSWD)",
        f"#ebox[%BF](x:0,y:0,w:100%,h:100%)",
        f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&join_game.dcml\\00&id_room={id_room}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"You cannot join the room! This is an incorrect room. Press Cancel button to exit\",26,\"Try Again\",\"Cancel\")",
        f"<NGDLG>"
    ))