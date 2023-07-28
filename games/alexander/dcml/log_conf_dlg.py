def log_conf_dlg(options):
    return "".join((
        f"#ebox[%EBG](x:0,y:0,w:1024,h:768)",
        f"#edit[%E_AC](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})",
        f"#edit[%E_CUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_CLANS_LAST_UPDATE}})",
        f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})",
        # f"#exec(LW_cfile&138186\\00&Cookies/%GV_VE_ACCOUNTS)",
        f"#def_dtbl_button_hotkey(13,0,27)#table[%TBL](%EBG[x:251,y:247,w:523,h:381],{{}}{{}}{{GW|open&log_user.dcml\\00&relogin=true^icon_last_update=<%GV_CLANS_LAST_UPDATE>^VE_MODE=creat^VE_PROF={options['VE_PROF']}^VE_NAME={options['VE_NAME']}^VE_NICK={options['VE_NICK']}^VE_MAIL={options['VE_NICK']}^VE_PASS={options['VE_PASS']}^accounts={options['VE_PROF']}^VE_GMID={options['VE_GMID']}\\00|LW_lockall}}{{GW|open&log_new_form.dcml\\00&logs=1^VE_PROF={options['VE_PROF']}^VE_MODE=edit^VE_NAME={options['VE_NAME']}^VE_NICK={options['VE_NICK']}^VE_MAIL={options['VE_MAIL']}^VE_PASS={options['VE_PASS']}^accounts={options['VE_PROF']}^VE_ICQ={options['VE_ICQ']}^VE_HOMP={options['VE_HOMP']}^VE_SEX={options['VE_SEX']}^VE_CNTRY={options['VE_CNTRY']}^VE_PHON={options['VE_PHON']}^VE_BIRTH={options['VE_BIRTH']}\\00|LW_lockall}}{{LW_key&#CANCEL}},0,11,368,\"LOGIN CONFIRMATION\",,26,\"Login\",\"Edit Profile\",\"Cancel\")",
        f"#ebox[%LBX](x:270,y:230,w:500,h:220)",
        f"#pix[%PX1](%LBX[x:2,y:44,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)",
        f"#font(BC14,BC14,BC14)",
        f"#txt[%L_PROF](%LBX[x:4,y:85,w:100%,h:20],{{}},\"Profile ID#\")",
        f"#pan[%P_PROF](%LBX[x:157,y:85,w:318,h:14],1)",
        f"#txt[%E_PROF](%LBX[x:159,y:85,w:300,h:20],{{}},{options['VE_PROF']})",
        f"#txt[%L_NAME](%LBX[x:4,y:115,w:100%,h:20],{{}},\"Full Name\")",
        f"#pan[%P_NAME](%LBX[x:157,y:115,w:318,h:14],1)",
        f"#txt[%E_NAME](%LBX[x:159,y:115,w:310,h:20],{{}},{options['VE_NAME']})",
        f"#txt[%L_NICK](%LBX[x:4,y:145,w:100%,h:20],{{}},\"Nickname\")",
        f"#pan[%P_NICK](%LBX[x:157,y:145,w:318,h:14],1)",
        f"#txt[%E_NICK](%LBX[x:159,y:145,w:310,h:20],{{}},\"{options['VE_NICK']}\") ",
        f"#pix[%PX2](%LBX[x:4,y:167,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35) ",
        f"#txt[%L_MAIL](%LBX[x:4,y:205,w:100%,h:20],{{}},\"E-Mail Address\")",
        f"#pan[%P_MAIL](%LBX[x:157,y:205,w:318,h:14],1) ",
        f"#txt[%E_MAIL](%LBX[x:159,y:205,w:310,h:20],{{}},{options['VE_MAIL']})",
        f"#txt[%L_PASS](%LBX[x:4,y:235,w:100%,h:20],{{}},\"User Password\")",
        f"#pan[%P_PASS](%LBX[x:157,y:235,w:318,h:14],1)",
        f"#txt[%E_PASS](%LBX[x:159,y:235,w:310,h:24],{{}},\"******************\") ",
        f"#txt[%L_GMID](%LBX[x:4,y:265,w:100%,h:20],{{}},\"Game Box #ID\")",
        f"#pan[%P_GMID](%LBX[x:157,y:265,w:318,h:14],1)",
        f"#txt[%E_GMID](%LBX[x:159,y:265,w:310,h:20],{{}},\"****-****-****-****\")",
        f"#pix[%PX3](%LBX[x:4,y:287,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%T_CHANGE](%LBX[x:363,y:335,w:180,h:24],{{GW|open&change_account2.dcml\\00&accounts={options['VE_PROF']}\\00|LW_lockall}},\"Old Profile\")",
        f"#hint(%T_CHANGE,\"Use old profile\")",
        f"#font(R2C12,BC12,BC12)",
        f"#txt[%L_ESRB](%LBX[x:0-10,y:351,w:100%,h:24],{{}},\"ESRB Notice: Game Experience May Change During Online Play\")",
        f"<MESDLG>",
        f"<MESDLG>",
        f"#block(l_games_btn.cml,CAN)<MESDLG>",
        f"<MESDLG>",
        f"#end(CAN)",
        f"#hint(%L_NAME,\"Enter your name\")",
        f"#hint(%L_NICK,\"Enter your nickname\")",
        f"#hint(%L_MAIL,\"Enter your e-mail address\")",
        f"#hint(%L_PASS,\"Enter your password\")",
        f"#hint(%L_GMID,\"Enter your GameBox ID#\")",
        f"#hint(%Login,\"Join the server\")",
        f"#hint(%Edit Profile,\"Edit profile\")"
    ))