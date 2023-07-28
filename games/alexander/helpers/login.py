import sqlalchemy

def login(lgd: str, database: sqlalchemy.Engine) -> str:
    with database.connect() as connection:
        if lgd:
            profileid = connection.execute(sqlalchemy.text(f"Select player_id from sessions where session_key = '{lgd}' LIMIT 1")).fetchone()
            if profileid:
                profile = connection.execute(sqlalchemy.text(f"\
                            Select player_id,\
                            name,\
                            nick,\
                            mail,\
                            pass,\
                            icq,\
                            site,\
                            sex,\
                            country,\
                            phone,\
                            birthday from players where player_id = '{profileid[0]}' LIMIT 1")).fetchone()
                if profile:
                    VE_PROF = profile[0]
                    VE_NAME = profile[1]
                    VE_NICK = profile[2]
                    VE_MAIL = profile[3]
                    VE_PASS = profile[4]
                    VE_ICQ = profile[5]
                    VE_HOMP = profile[6]
                    VE_SEX = profile[7]
                    VE_CNTRY = profile[8]
                    VE_PHON = profile[9]
                    VE_BIRTH = profile[10]
                    return "".join((
                        f"#ebox[%EBG](x:0,y:0,w:1024,h:768)",
                        f"#edit[%E_AC](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})",
                        f"#edit[%E_CUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_CLANS_LAST_UPDATE}})",
                        f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})",
                        f"#edit[%E_AC2](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_AC}})",
                        f"#exec(LW_cfile&&Cookies/%GV_VE_AC)",
                        f"#exec(LW_time&10&l_games_btn.cml\\00)",
                        f"#block(l_games_btn.cml,l_g):GW|open&log_conf_dlg.dcml\\00&logs=true^last_update=<%GV_LAST_UPDATE>^accounts=<%GV_VE_ACCOUNTS>^VE_PROF={VE_PROF}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_PASS={VE_PASS}^VE_ICQ={VE_ICQ}^VE_HOMP={VE_HOMP}^VE_SEX={VE_SEX}^VE_CNTRY={VE_CNTRY}^VE_PHON={VE_PHON}^VE_BIRTH={VE_BIRTH}\\00|LW_lockall",
                        f"#end(l_g)"
                    ))

    return "".join((
        f"#ebox[%EBG](x:0,y:0,w:1024,h:768) ",
        f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}}) ",
        f"#exec(LW_time&10&l_games_btn.cml\\00) ",
        f"#block(l_games_btn.cml,l_g):GW|open&log_new_form.dcml\\00&logs=2^VE_MODE=creat^last_update=<%GV_LAST_UPDATE>\\00|LW_lockall ",
        f"#end(l_g)",
    ))