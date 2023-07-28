import sqlalchemy

def log_new_form(options: dict, database: sqlalchemy.Engine) -> str:
    print(options)
    VE_MODE=options.get("VE_MODE", "creat")
    VE_NAME=options.get("VE_NAME", "")
    VE_NICK=options.get("VE_NICK", "")
    VE_MAIL=options.get("VE_MAIL", "")
    VE_PROF=options.get("VE_PROF", "")
    VE_ICQ=options.get("VE_ICQ", "n/a")
    VE_HOMP=options.get("VE_HOMP", "n/a")
    VE_SEX=options.get("VE_SEX", "2")
    VE_CNTRY=options.get("VE_CNTRY", "n/a")
    VE_PHON=options.get("VE_PHON", "n/a")
    VE_BIRTH=options.get("VE_BIRTH", "")
    accounts=options.get("accounts", "")
    genders = []
    countries = []
    with database.connect() as connection:
        
        cursor_out = connection.execute(sqlalchemy.text(f'select name from sexes')).fetchall()
        for row in cursor_out:
            genders.append(f'\"{row[0]}\"')
        genders = ",".join(genders)
        
        cursor_out = connection.execute(sqlalchemy.text(f'select name from countries')).fetchall()
        for row in cursor_out:
            countries.append(f'\"{row[0]}\"')
        countries = ",".join(countries)

    if VE_MODE == "edit":
        return "".join((
            f"#ebox[%EBG](x:0,y:0,w:1024,h:768)",
            f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})",
            f"#block(cancel.cml,l_g):<!goback!>\\00",
            f"#end(l_g)",
            f"#def_dtbl_button_hotkey(13,0,27)",
            f"#table[%TBL](%EBG[x:251,y:247,w:523,h:381],{{}}{{}}{{GW|open&reg_new_user.dcml\\00&cansel=true^VE_PROF={VE_PROF}^VE_MODE=edit^VE_NAME=<%GV_VE_NAME>^VE_NICK=<%GV_VE_NICK>^VE_MAIL=<%GV_VE_MAIL>^VE_GMID=<%GV_VE_GMID>^VE_PASS=<%GV_VE_PASS>^VE_RASS=<%GV_VE_RASS>^VE_ICQ=<%GV_VE_ICQ>^VE_HOMP=<%GV_VE_HOMP>^VE_SEX=<%GV_VE_SEX>^VE_CNTRY=<%GV_VE_CNTRY>^VE_PHON=<%GV_VE_PHON>^VE_BIRTH=<%GV_VE_BIRTH>^accounts={accounts}\\00|LW_lockall}}{{GW|open&log_new_form.dcml\\00&logs=1^cansel=true^VE_MODE=creat^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},0,11,368,EDIT PERSONAL PROFILE,,26,Update,\"New account\",\"Cancel\")",
            f"#ebox[%LBX](x:270,y:210,w:500,h:220)",
            f"#font(BC14,RC14,RC14))",
            f"#txt[%L_NAME](%LBX[x:4,y:56,w:100%,h:20],{{}},\"Full Name\")",
            f"#pan[%P_NAME](%LBX[x:159,y:56,w:317,h:14],1)",
            f"#exec(LW_cfile&{VE_NAME}\\00&Cookies/%GV_VE_NAME)",
            f"#edit[%E_NAME](%LBX[x:164,y:53,w:302,h:18],{{%GV_VE_NAME}},0,0,0,1)",
            f"#txt[%L_NICK](%LBX[x:4,y:84,w:100%,h:20],{{}},\"Nickname\")",
            f"#pan[%P_NICK](%LBX[x:159,y:84,w:317,h:14],1)",
            f"#exec(LW_cfile&{VE_NICK}\\00&Cookies/%GV_VE_NICK)",
            f"#edit[%E_NICK](%LBX[x:164,y:81,w:302,h:18],{{%GV_VE_NICK}})",
            f"#txt[%L_MAIL](%LBX[x:4,y:112,w:100%,h:20],{{}},\"E-Mail Address\")",
            f"#pan[%P_MAIL](%LBX[x:159,y:112,w:317,h:14],1)",
            f"#exec(LW_cfile&{VE_MAIL}\\00&Cookies/%GV_VE_MAIL)",
            f"#edit[%E_MAIL](%LBX[x:164,y:109,w:302,h:18],{{%GV_VE_MAIL}})",
            f"#txt[%L_GMID](%LBX[x:4,y:140,w:100%,h:20],{{}},\"Game Box #ID\")",
            f"#pan[%P_GMID](%LBX[x:159,y:140,w:317,h:14],1)",
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_GMID)",
            f"#edit[%E_GMID](%LBX[x:164,y:137,w:302,h:18],{{%GV_VE_GMID}},0,0,1)",
            f"#txt[%L_PASS](%LBX[x:4,y:168,w:100%,h:20],{{}},\"User Password\")",
            f"#pan[%P_PASS](%LBX[x:159,y:168,w:317,h:14],1)",
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASS)",
            f"#edit[%E_PASS](%LBX[x:164,y:165,w:302,h:18],{{%GV_VE_PASS}},0,0,1)",
            f"#txt[%L_RASS](%LBX[x:4,y:196,w:100%,h:20],{{}},\"Change password to\")",
            f"#pan[%P_RASS](%LBX[x:159,y:196,w:317,h:14],1)",
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_RASS)",
            f"#edit[%E_RASS](%LBX[x:164,y:193,w:302,h:18],{{%GV_VE_RASS}},0,0,1)",
            f"#txt[%L_ICQ](%LBX[x:4,y:224,w:100%,h:20],{{}},\"ICQ #ID\")",
            f"#pan[%P_ICQ](%LBX[x:159,y:224,w:317,h:14],1)",
            f"#exec(LW_cfile&{VE_ICQ}\\00&Cookies/%GV_VE_ICQ)",
            f"#edit[%E_ICQ](%LBX[x:164,y:221,w:302,h:18],{{%GV_VE_ICQ}})",
            f"#txt[%L_HOMP](%LBX[x:4,y:252,w:100%,h:20],{{}},\"Internet Homepage\")",
            f"#pan[%P_HOMP](%LBX[x:159,y:252,w:317,h:14],1)",
            f"#exec(LW_cfile&{VE_HOMP}\\00&Cookies/%GV_VE_HOMP)",
            f"#edit[%E_HOMP](%LBX[x:164,y:249,w:302,h:18],{{%GV_VE_HOMP}})",
            f"#txt[%L_SEX](%LBX[x:4,y:280,w:100%,h:20],{{}},\"Gender\")",
            f"#exec(LW_cfile&{VE_SEX}\\00&Cookies/%GV_VE_SEX)",
            f"#cbb[%E_SEX](%LBX[x:153,y:273,w:329,h:18],{{%GV_VE_SEX}},{genders},0)",
            f"#txt[%L_CNTRY](%LBX[x:4,y:308,w:100%,h:20],{{}},\"Country\")",
            f"#exec(LW_cfile&{VE_CNTRY}\\00&Cookies/%GV_VE_CNTRY)",
            f"#cbb[%E_CNTRY](%LBX[x:153,y:301,w:329,h:18],{{%GV_VE_CNTRY}},{countries},0)",
            f"#txt[%L_PHON](%LBX[x:4,y:336,w:100%,h:20],{{}},\"Home Phone\")",
            f"#pan[%P_PHON](%LBX[x:159,y:336,w:317,h:14],1)",
            f"#exec(LW_cfile&{VE_PHON}\\00&Cookies/%GV_VE_PHON)",
            f"#edit[%E_PHON](%LBX[x:164,y:333,w:302,h:18],{{%GV_VE_PHON}})",
            f"#txt[%L_BIRTH](%LBX[x:4,y:364,w:100%,h:20],{{}},\"Birthday (D/M/Y)\")",
            f"#pan[%P_BIRTH](%LBX[x:159,y:364,w:317,h:14],1)",
            f"#exec(LW_cfile&{VE_BIRTH}\\00&Cookies/%GV_VE_BIRTH)",
            f"#edit[%E_BIRTH](%LBX[x:164,y:361,w:302,h:18],{{%GV_VE_BIRTH}})<MESDLG><MESDLG>",
            f"#block(l_games_btn.cml,CAN)<MESDLG><MESDLG>",
            f"#end(CAN)",
            f"#hint(%L_NAME,\"Enter your name\")",
            f"#hint(%L_NICK,\"Enter your nickname\")",
            f"#hint(%L_MAIL,\"Enter your e-mail address\")",
            f"#hint(%L_PASS,\"Enter your password\")",
            f"#hint(%L_RASS,\"Change password to\")",
            f"#hint(%L_GMID,\"Enter your GameBox ID#\")",
            f"#hint(%L_ICQ,\"Enter your ICQ number\")",
            f"#hint(%L_HOMP,\"Enter your homepage\")",
            f"#hint(%L_SEX,\"Select your sex\")",
            f"#hint(%L_CNTRY,\"Select country\")",
            f"#hint(%L_PHON,\"Enter your home phone number\")",
            f"#hint(%L_BIRTH,\"Enter your birth date (DD/MM/YYYY)\")",
            f"#hint(%New account,\"Create a new account\")",
        ))

    elif VE_MODE == "creat":
        return "".join((
            f"#ebox[%EBG](x:0,y:0,w:1024,h:768)",
            f"#edit[%E_AC](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})",
            f"#edit[%E_CUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_CLANS_LAST_UPDATE}})",
            f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})",
            f"#def_dtbl_button_hotkey(13,0,27)",
            f"#def_dtbl_button_hint(Register,Use old profile)",
            f"#table[%TBL](%EBG[x:240,y:217,w:540,h:392],{{}}{{}}{{GW|open&log_user.dcml\\00&relogin=true^icon_last_update=<%GV_CLANS_LAST_UPDATE>^VE_MODE=creat^VE_PROF={options['VE_PROF']}^VE_NAME={options['VE_NAME']}^VE_NICK={options['VE_NICK']}^VE_MAIL={options['VE_NICK']}^VE_PASS={options['VE_PASS']}^accounts={options['VE_PROF']}^VE_GMID={options['VE_GMID']}\\00|LW_lockall}}{{GW|open&log_new_form.dcml\\00&logs=1^VE_PROF={options['VE_PROF']}^VE_MODE=edit^VE_NAME={options['VE_NAME']}^VE_NICK={options['VE_NICK']}^VE_MAIL={options['VE_MAIL']}^VE_PASS={options['VE_PASS']}^accounts={options['VE_PROF']}^VE_ICQ={options['VE_ICQ']}^VE_HOMP={options['VE_HOMP']}^VE_SEX={options['VE_SEX']}^VE_CNTRY={options['VE_CNTRY']}^VE_PHON={options['VE_PHON']}^VE_BIRTH={options['VE_BIRTH']}\\00|LW_lockall}}{{LW_key&#CANCEL}},0,11,368,\"LOGIN CONFIRMATION\",,26,\"Login\",\"Edit Profile\",\"Cancel\")",
            f"#ctxt[%L_DUMMY](%EBG[x:240,y:195,w:540,h:20],{{}},\"CREATE PERSONAL PROFILE\")",
            f"#def_dtbl_button_hint(,,)",
            f"#ebox[%LBX](x:260,y:200,w:500,h:220)",
            f"#font(BC14,RC14,RC14))",
            f"#pan[%P_PROF](%LBX[x:22,y:42,w:460,h:120],3)",
            f"#pix[%PX2](%LBX[x:20,y:40,w:100%,h:100%],{{}},Interf3/InGame/druids_win_lose,1,1,1,1)",
            f"#txt[%L_NICK](%LBX[x:4,y:223,w:100%,h:20],{{}},\"Nickname\")",
            f"#pan[%P_NICK](%LBX[x:183,y:220,w:310,h:18],3)",
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_NICK)",
            f"#edit[%E_NICK](%LBX[x:187,y:223,w:302,h:18],{{%GV_VE_NICK}})",
            f"#txt[%L_GMID](%LBX[x:4,y:256,w:100%,h:20],{{}},\"Game Box #ID\")",
            f"#pan[%P_GMID](%LBX[x:183,y:253,w:310,h:18],3)",
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_GMID)",
            f"#edit[%E_GMID](%LBX[x:187,y:256,w:302,h:18],{{%GV_VE_GMID}})",
            f"#txt[%L_PASS](%LBX[x:4,y:289,w:100%,h:20],{{}},\"User Password\")",
            f"#pan[%P_PASS](%LBX[x:183,y:286,w:310,h:18],3)",
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASS)",
            f"#edit[%E_PASS](%LBX[x:187,y:289,w:302,h:18],{{%GV_VE_PASS}},0,0,1)",
            f"#txt[%L_RASS](%LBX[x:4,y:322,w:100%,h:20],{{}},\"Retype Password\")",
            f"#pan[%P_RASS](%LBX[x:183,y:319,w:310,h:18],3)",
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_RASS)",
            f"#edit[%E_RASS](%LBX[x:187,y:322,w:302,h:18],{{%GV_VE_RASS}},0,0,1)",
            f"<MESDLG>",
            f"<MESDLG>",
            f"#block(l_games_btn.cml,CAN)",
            f"<MESDLG>",
            f"<MESDLG>",
            f"#end(CAN)",
            f"#hint(%L_NAME,\"Enter your name\")",
            f"#hint(%L_NICK,\"Enter your nickname\")",
            f"#hint(%L_MAIL,\"Enter your e-mail address\")",
            f"#hint(%L_PASS,\"Enter your password\")",
            f"#hint(%L_RASS,\"Enter your password\")",
            f"#hint(%L_GMID,\"Enter your GameBox ID#\")",
            f"#hint(%L_ICQ,\"Enter your ICQ number\")",
            f"#hint(%L_HOMP,\"Enter your homepage\")",
            f"#hint(%L_SEX,\"Select your sex\")",
            f"#hint(%L_CNTRY,\"Select country\")",
            f"#hint(%L_PHON,\"Enter your home phone number\")",
            f"#hint(%L_BIRTH,\"Enter your birth date (DD/MM/YYYY)\")",
        ))
    return ""