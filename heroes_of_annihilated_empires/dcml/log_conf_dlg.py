def log_conf_dlg(options):
    return "".join((
        f"#ebox[%EBG](x:0,y:0,w:1024,h:768)",
        f"#edit[%E_AC](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})",
        f"#edit[%E_CUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_CLANS_LAST_UPDATE}})",
        f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})",
        f"#edit[%E_UD](%EBG[x:0,y:0,w:0,h:0],{{%GV_UPDATE_DAT}})",
        f"#exec(LW_cfile&139671\\00&Cookies/%GV_VE_ACCOUNTS)",
        f"#def_dtbl_button_hotkey(13,0,27)",
        f"#def_dtbl_button_hint(Join the server)",
        f"#table[%TBL](%EBG[x:240,y:217,w:540,h:392],{{}}{{}}{{GW|open&log_user.dcml\\00&relogin=true^icon_last_update=<%GV_CLANS_LAST_UPDATE>^VE_PROF={options['VE_PROF']}^VE_NICK={options['VE_NICK']}^VE_PASS={options['VE_PASS']}\\00|LW_lockall}}{{GW|open&log_new_form.dcml\\00&up_dat=1^VE_MODE=edit^VE_PROF={options['VE_PROF']}^VE_NICK={options['VE_NICK']}^VE_PASS={options['VE_PASS']}\\00|LW_lockall}}{{LW_key&#CANCEL}},0,0,477,\"LOGIN CONFIRMATION\",,24,\"Login\",\"Edit Profile\",\"Cancel\")",
        f"#def_dtbl_button_hint(,,) ",
        f"#ebox[%LBX](x:260,y:200,w:500,h:220) ",
        f"#font(BC14,RC14,RC14) ",
        f"#txt[%L_PROF](%LBX[x:8,y:210,w:100%,h:20],{{}},\"Profile ID#\") ",
        f"#pan[%P_PROF](%LBX[x:183,y:207,w:310,h:18],3) ",
        f"#txt[%E_PROF](%LBX[x:187,y:210,w:300,h:20],{{}},{options['VE_PROF']}) ",
        f"#txt[%L_NICK](%LBX[x:8,y:243,w:100%,h:20],{{}},\"Nickname\") ",
        f"#pan[%P_NICK](%LBX[x:183,y:240,w:310,h:18],3) ",
        f"#txt[%E_NICK](%LBX[x:187,y:243,w:310,h:20],{{}},\"{options['VE_NICK']}\") ",
        f"#pan[%P_PROF](%LBX[x:22,y:42,w:460,h:120],3) ",
        f"#pix[%PX2](%LBX[x:20,y:40,w:100%,h:100%],{{}},Interf3/InGame/_common_pictures,0,0,0,0) ",
        f"#font(GC14,RC14,BC14) ",
        f"#sbtn[%T_CHANGE](%LBX[x:358,y:320,w:0,h:0],{{GW|open&change_account2.dcml\\00|LW_lockall}},\"Old Profile\") ",
        f"#hint(%T_CHANGE,\"Use old profile\") ",
        f"#font(R2C12,BC12,BC12) ",
        f"#txt[%L_ESRB](%LBX[x:4,y:361,w:100%,h:24],{{}},\"ESRB Notice: Game Experience May Change During Online Play\") ",
        f"#font(R2C12,BC12,BC12) ",
        f"#mtxt[%L_ESRB](%LBX[x:4,y:290,w:100%,h:24],{{}},\"New version available. Please visit http://www.heroesofae.com/ for additional information.\") ",
        f"<MESDLG> ",
        f"<MESDLG> ",
        f"#block(l_games_btn.cml,CAN)<MESDLG> ",
        f"<MESDLG> ",
        f"#end(CAN)"
    ))