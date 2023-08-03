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
            f"#edit[%E_UD](%EBG[x:0,y:0,w:0,h:0],{{%GV_UPDATE_DAT}})",
            f"#exec(LW_xcfile&Cookies/.&1164726714&empty)",
            f"#block(cancel.cml,l_g):<!goback!>\\00",
            f"#end(l_g)",
            f"#def_dtbl_button_hotkey(13,0,27)",
            f"#def_dtbl_button_hint(Update,Create a new account)",
            f"#table[%TBL](%EBG[x:240,y:217,w:540,h:392],{{}}{{}}{{GW|open&reg_new_user.dcml\\00&cansel=true^VE_PROF=139671^VE_MODE=edit^VE_NAME=<%GV_VE_NAME>^VE_NICK=<%GV_VE_NICK>^VE_MAIL=<%GV_VE_MAIL>^VE_GMID=<%GV_VE_GMID>^VE_PASS=<%GV_VE_PASS>^VE_RASS=<%GV_VE_RASS>^VE_ICQ=<%GV_VE_ICQ>^VE_HOMP=<%GV_VE_HOMP>^VE_SEX=<%GV_VE_SEX>^VE_CNTRY=<%GV_VE_CNTRY>^VE_PHON=<%GV_VE_PHON>^VE_BIRTH=<%GV_VE_BIRTH>\\00|LW_lockall}}{{GW|open&log_new_form.dcml\\00&up_dat=1^cansel=true^VE_MODE=creat^accounts=139671\\00|LW_lockall}}{{ LW_file&Internet/Cash/cancel.cml}},0,0,477,EDIT PERSONAL PROFILE,,24,Update,\"New account\",\"Cancel\")",
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
            f"#txt[%L_RASS](%LBX[x:4,y:322,w:100%,h:20],{{}},\"Change password to\")",
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
            f"#hint(%L_RASS,\"Change password to\")",
            f"#hint(%L_GMID,\"Enter your GameBox ID#\")",
            f"#hint(%L_ICQ,\"Enter your ICQ number\")",
            f"#hint(%L_HOMP,\"Enter your homepage\")",
            f"#hint(%L_SEX,\"Select your sex\")",
            f"#hint(%L_CNTRY,\"Select country\")",
            f"#hint(%L_PHON,\"Enter your home phone number\")",
            f"#hint(%L_BIRTH,\"Enter your birth date (DD/MM/YYYY)\")"




        ))

    elif VE_MODE == "creat": ########################################################
        return "".join((
            f"#ebox[%EBG](x:0,y:0,w:1024,h:768)",
            f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})",
            f"#edit[%E_UD](%EBG[x:0,y:0,w:0,h:0],{{%GV_UPDATE_DAT}})",
            f"#exec(LW_xcfile&Cookies/.&1164726714&empty)",
            f"#def_dtbl_button_hotkey(13,0,27)",
            f"#def_dtbl_button_hint(Register,Use old profile)",
            f"#table[%TBL](%EBG[x:240,y:217,w:540,h:392],{{}}{{}}{{GW|open&reg_new_user.dcml\\00&cansel=^VE_PROF=^VE_MODE=creat^VE_NAME=<%GV_VE_NAME>^VE_NICK=<%GV_VE_NICK>^VE_MAIL=<%GV_VE_MAIL>^VE_GMID=<%GV_VE_GMID>^VE_PASS=<%GV_VE_PASS>^VE_RASS=<%GV_VE_RASS>^VE_ICQ=<%GV_VE_ICQ>^VE_HOMP=<%GV_VE_HOMP>^VE_SEX=<%GV_VE_SEX>^VE_CNTRY=<%GV_VE_CNTRY>^VE_PHON=<%GV_VE_PHON>^VE_BIRTH=<%GV_VE_BIRTH>^accounts=\\00|LW_lockall}}{{GW|open&change_account2.dcml\\00&cansel=^accounts=\\00|LW_lockall}}{{LW_key&#CANCEL}},0,0,477,CREATE PERSONAL PROFILE,,24,Register,Old Profile,\"Cancel\")",
            f"#def_dtbl_button_hint(,,)",
            f"#ebox[%LBX](x:260,y:200,w:500,h:220)",
            f"#font(BC14,RC14,RC14)",
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