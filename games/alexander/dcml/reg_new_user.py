import sqlalchemy
import sqlalchemy.exc

def reg_new_user(options: dict, database: sqlalchemy.Engine) -> str:
    VE_PROF=options.get("VE_PROF", "")
    VE_MODE=options.get("VE_MODE", "creat")
    VE_NAME=options.get("VE_NAME", "")
    VE_NICK=options.get("VE_NICK", "")
    VE_MAIL=options.get("VE_MAIL", "")
    VE_GMID=options.get("VE_GMID", "")
    VE_PASS=options.get("VE_PASS", "")
    VE_RASS=options.get("VE_RASS", "")
    VE_ICQ=options.get("VE_ICQ", "n/a")
    VE_HOMP=options.get("VE_HOMP", "n/a")
    VE_SEX=options.get("VE_SEX", "3")
    VE_CNTRY=options.get("VE_CNTRY", "n/a")
    VE_PHON=options.get("VE_PHON", "n/a")
    VE_BIRTH=options.get("VE_BIRTH", "")
    accounts=options.get("accounts", "0")
    cansel=options.get("cansel", "")
    logs=options.get("logs", "1")

    try:
        with database.connect() as connection:
            if VE_MODE == "edit":
                out = connection.execute(sqlalchemy.text(f"SELECT * FROM players \
                            WHERE gmid = '{VE_GMID}' AND \
                            pass = '{VE_PASS}' LIMIT 1")).fetchone()

                if not out:
                    return " ".join((f"<MESDLG> ",
                            f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
                            f"#def_dtbl_button_hotkey(13,27) ",
                            f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={logs}^cansel={cansel}^VE_MODE=edit^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"Incorrect GMID or password! Press Edit button to retry. Press Cancel button to exit\",26,\"Edit\",\"Cancel\") ",
                            f"<MESDLG>"))

                connection.execute(sqlalchemy.text(f'\
                            UPDATE players\
                            SET\
                            nick="{VE_NICK}",\
                            name="{VE_NAME}",\
                            mail="{VE_MAIL}",\
                            pass="{VE_PASS}",\
                            icq="{VE_ICQ}",\
                            site="{VE_HOMP}",\
                            sex={int(VE_SEX)+1},\
                            country={int(VE_CNTRY)+1},\
                            phone="{VE_PHON}",\
                            birthday="{VE_BIRTH}"\
                            WHERE gmid = "{VE_GMID}" AND pass = "{VE_PASS}" AND pass = "{VE_RASS}"'))

            elif VE_MODE == "creat":

                    connection.execute(sqlalchemy.text(f'INSERT INTO players\
                                    (nick,\
                                    name,\
                                    mail,\
                                    gmid,\
                                    pass,\
                                    icq,\
                                    site,\
                                    sex,\
                                    country,\
                                    phone,\
                                    birthday) VALUES ("{VE_NICK}",\
                                        f"{VE_NAME}",\
                                        f"{VE_MAIL}",\
                                        f"{VE_GMID}",\
                                        f"{VE_PASS}",\
                                        f"{VE_ICQ}",\
                                        f"{VE_HOMP}",\
                                        f"{VE_SEX}",\
                                        f"{VE_CNTRY}",\
                                        f"{VE_PHON}",\
                                        f"{VE_BIRTH}")'))

            connection.commit()
            
    except sqlalchemy.exc.SQLAlchemyError as error:

        if error._message == "ERR_NICK_EXISTS":
            return " ".join((f"<MESDLG> ",
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
                f"#def_dtbl_button_hotkey(13,27) ",
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={logs}^cansel={cansel}^VE_PROF={VE_PROF}^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"User with that nickname already exists! Press Edit button to change nickname. Press Cancel button to exit\",26,\"Edit\",\"Cancel\")",
                f"<MESDLG>"))

        elif error._message == "ERR_BIRTH_FORMAT":
            return " ".join((f"<MESDLG> ",
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
                f"#def_dtbl_button_hotkey(13,27) ",
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={logs}^cansel={cansel}^VE_PROF={VE_PROF}^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"Incorrect birthday date! Birthday must be in DD/MM/YYYY or DD.MM.YYYY format. Where DD - day (1-31), MM - month (1-12), YYYY - year. Press Edit button to check birthday date. Press Cancel to exit\",26,\"Edit\",\"Cancel\")",
                f"<MESDLG>"))

        elif error._message == "ERR_GMID_INVALID":
            return " ".join((f"<MESDLG> ",
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
                f"#def_dtbl_button_hotkey(13,27) ",
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={logs}^cansel={cansel}^VE_PROF={VE_PROF}^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"An invalid Game Box Identifier was entered! Please enter more carefully. The number of attempts is limited. Press Edit button to check Game Box Identifier. Press Cancel to exit\",26,\"Edit\",\"Cancel\")",
                f"<MESDLG>"))

        elif error._message == "ERR_GMID_USED":
            return " ".join((f"<MESDLG> ",
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
                f"#def_dtbl_button_hotkey(13,27) ",
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={logs}^cansel={cansel}^VE_PROF={VE_PROF}^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"The provided Game Box Identifier has already been used. The number of attempts is limited. Press Edit button to check Game Box Identifier. Press Cancel to exit\",26,\"Edit\",\"Cancel\")",
                f"<MESDLG>"))

        elif error._message == "ERR_EMAIL_USED":
            return " ".join((f"<MESDLG>",
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
                f"#def_dtbl_button_hotkey(13,27) ",
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={logs}^cansel={cansel}^VE_PROF={VE_PROF}^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"The provided E-Mail address has already been used. Press Edit button to check E-Mail address. Press Cancel to exit\",26,\"Edit\",\"Cancel\")",
                f"<MESDLG>"))
        
        else:
            print("Huh?")
            return "".join((
                f"<MESDLG>",
                f"#exec(LW_time&10&<!goback!>\\00)",
                f"<MESDLG>"))
        
    except Exception as error:
        print(error)
        return " ".join((f"<MESDLG> ",
            f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
            f"#def_dtbl_button_hotkey(13,27) ",
            f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={logs}^cansel={cansel}^VE_PROF={VE_PROF}^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^accounts={accounts}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"{error}. Press Edit button to try again. Press Cancel to exit\",26,\"Edit\",\"Cancel\")",
            f"<MESDLG>"))

    print("ALL GOOD")
    return " ".join((
    f"<MESDLG> ",
    f"#ebox[%MBG](x:0,y:0,w:1024,h:768) ",
    f"#edit[%E_AC](%MBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}}) ",
    f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASS) ",
    f"#exec(LW_cfile&\\00&Cookies/%GV_VE_RASS) ",
    f"#exec(LW_cfile&\\00&Cookies/%GV_VE_GMID) ",
    f"#def_dtbl_button_hotkey(13,27) ",
    f"#def_dtbl_button_hotkey(13,27) ",
    f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_user.dcml\\00&VE_PROF={VE_PROF}^save_pass=true^cansel=^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_PASS={VE_PASS}^VE_RASS={VE_RASS}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^VE_GMID={VE_GMID}\\00|LW_lockall}}{{GW|open&log_user.dcml\\00&VE_PROF={VE_PROF}^cansel={cansel}^VE_MODE={VE_MODE}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_PASS={VE_PASS}^VE_RASS={VE_RASS}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}^VE_GMID={VE_GMID}\\00|LW_lockall}},2,0,3,13,252,\"INFORMATION\",\"Your personal profile data has been successfully created!\\Press OK button to save password, in other case press Cancel.\\This option saves your password and Game Box #ID. Don't use it, if you play from computer accessible for other people.\",26,\"OK\",\"Cancel\")  ",
    f"<MESDLG>"))