def games():
 return "".join((
    f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
    f"#pix[%PXT1](%TB[x:8,y:39,w:100%,h:100%],{{}},Interf3/elements/internet_menu,1,1,1,1)",
    f"#pix[%PXT2](%TB[x:8,y:308,w:100%,h:100%],{{}},Interf3/elements/internet_menu,0,0,0,0)",
    f"#pan[%P_PROF0](%TB[x:0-21,y:402,w:214,h:0],9)",
    f"#font(RG18,RG18,RG18)",
    f"#txt[%PL](%TB[x:734,y:6,w:100,h:20],{{}},\"Players\")",
    f"#font(WG16,WG16,WG16)",
    f"#ctxt[%TTTEXT](%TB[x:0-67,y:0-40,w:1024,h:20],{{}},\"GAMES\")",
    f"#font(R2C14,R2C14,R2C14)",
    f"#txt[%TMTEXT](%TB[x:14,y:517,w:100,h:20],{{}},\"Message\")",
    f"#font(RC14,R2C14,RC14)",
    f"#def_gp_btn(Interf3/elements/tab,3,3,0,6)",
    f"#gpbtn[%BT1](%TB[x:237,y:27,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")",
    f"#hint(%BT1,\"News, events, forum and punishment list\")",
    f"#font(RC14,R2C14,RC14)",
    f"#def_gp_btn(Interf3/elements/tab,3,3,0,6)",
    f"#gpbtn[%BT2](%TB[x:372,y:27,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
    f"#hint(%BT2,\"Player list, personal mail and clan information\")",
    f"#font(RC14,RC14,RC14)",
    f"#def_gp_btn(Interf3/elements/tab,2,2,0,2)",
    f"#gpbtn[%BT3](%TB[x:503,y:27,w:-22,h:-18],{{}},\"Games\")",
    f"#hint(%BT3,\"Games\")",
    f"#font(RC14,R2C14,RC14)",
    f"#def_gp_btn(Interf3/elements/tab,3,3,0,6)",
    f"#gpbtn[%BT4](%TB[x:635,y:27,w:-22,h:-18],{{GW|open&scored_games.dcml\\00|LW_lockall}},\"Scored Games\")",
    f"#hint(%BT4,\"Played games and their scores\")",
    f"#ebox[%B_VOTE](x:13,y:400,w:148,h:103)",
    f"<VOTING>",
    f"#exec(GW|open&voting.dcml\\00&question=\\00)<VOTING>#ebox[%B](x:0,y:0,w:100%,h:100%)",
    f"#font(RC14,GC14,RC14)",
    f"#ctxt[%LIST1](%B[x:0,y:106,w:150,h:24],{{GW|open&games.dcml\\00|LW_lockall}},\"{{Games}}\")",
    f"#hint(%LIST1,\"Games\")",
    f"#edit[%E_FT](%B[x:0,y:0,w:0,h:0],{{%GV_HELP_MODE}})",
    f"#font(R2C14,R2C14,RC14)",
    # f"//#ctxt[%LIST2](%B[x:0,y:%LIST1+4,w:150,h:24],{{GW|open&games_playing.dcml\\00|LW_lockall}},\"{{Current games}}\")",
    # f"//#hint(%LIST2,\"Current games\")",
    f"#ctxt[%LIST3](%B[x:0,y:%LIST1+4,w:150,h:24],{{GW|open&games_stats.dcml\\00|LW_lockall}},\"{{Statics}}\")",
    f"#hint(%LIST3,\"Games statistics\")",
    # f"//#ctxt[%LIST4](%B[x:0,y:%LIST3+4,w:150,h:24],{{GW|open&rating_help.dcml\\00&mode=<%GV_HELP_MODE>\\00|LW_lockall}},\"{{Rating describe}}\")",
    # f"//#hint(%LIST4,\"Rating describe\")
    f"<MAINFRM>",
    f"#pan[%PAN](%B[x:150,y:42,w:545,h:296],7)",
    f"#font(GC14,RC14,RC14)",
    f"#sbtn[%B_C](%B[x:580,y:354,w:0,h:0],{{GW|open&new_game_dlg.dcml\\00&delete_old=true\\00|LW_lockall}},\"Create\")",
    f"#def_panel_vars(%GV_SELECTED_PAN,id_room,%JPAN)",
    f"<DBTBL>",
    f"#exec(GW|open&dbtbl.dcml\\00)",
    f"<DBTBL>",
    f"#pan[%P_PROF](%TB[x:0-21,y:379,w:768,h:0],9)",
    f"<MAINFRM>",
    f"<NGDLG>",
    f"#exec(LW_time&3000&l_games_btn.cml\\00)",
    f"<NGDLG>",
    f"#block(cancel.cml,CAN)",
    f"<NGDLG>",
    f"#exec(LW_time&3000&l_games_btn.cml\\00)",
    f"<NGDLG>",
    f"#end(CAN)"
))