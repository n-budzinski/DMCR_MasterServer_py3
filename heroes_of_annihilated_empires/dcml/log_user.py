from ...common import genID
from config import HOAE_IRC
import sqlalchemy

def log_user(options: dict, database: sqlalchemy.Engine) -> str:
    VE_NICK = options.get("VE_NICK")
    VE_GMID=options.get("VE_GMID", "")
    VE_NAME=options.get("VE_NAME", "")
    VE_NICK=options.get("VE_NICK", "")
    VE_PROF=options.get("VE_PROF", "")
    VE_MAIL=options.get("VE_MAIL", "")
    VE_PASS=options.get("VE_PASS", "")
    save_pass = options.get("save_pass", None)
    relogin=options.get("relogin", "false")
    accounts=options.get("accounts", "")
    cansel=options.get("cansel", "")
    profile = None
    if VE_PASS == "":
        return "".join((
        f"<MESDLG>",
        f"#ebox[%D](x:0,y:0,w:1024,h:768)",
        f"#def_dtbl_button_hotkey(13,27)",
        f"#table[%TBL](%D[x:306,y:325,w:415,h:205],{{}}{{}}{{LW_file&Internet/Cash/l_games_btn.cml}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"The Password is an obligatory field to be filled in. Attention! The Password will be required in case you need to change account information in future.\",26,\"Edit\",\"Cancel\")",
        f"<MESDLG>"
    ))
    with database.connect() as connection:
        if relogin == "true":
            profile = connection.execute(sqlalchemy.text(f"\
                    SELECT player_id, nick, pass, gmid\
                    FROM players\
                    WHERE nick = '{VE_NICK}' AND pass = '{VE_PASS}'\
                    LIMIT 1")).fetchone()
        else:
            profile = connection.execute(sqlalchemy.text(f"\
                    SELECT player_id, nick, pass, gmid\
                    FROM players\
                    WHERE nick = '{VE_NICK}' AND pass = '{VE_PASS}' AND gmid = '{VE_GMID}'\
                    LIMIT 1")).fetchone()
        if profile:
            sessionid = genID()
            connection.execute(sqlalchemy.text(f"REPLACE INTO sessions \
                            (session_key,\
                            player_id) VALUES ('{sessionid}', '{profile[0]}')"))
            connection.commit()
        else:
            return "".join((
            f"<MESDLG>",
            f"#ebox[%D](x:0,y:0,w:1024,h:768)",
            f"#def_dtbl_button_hotkey(13,27)",
            f"#table[%TBL](%D[x:306,y:325,w:415,h:205],{{}}{{}}{{LW_file&Internet/Cash/l_games_btn.cml}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"Incorrect login data.\",26,\"Edit\",\"Cancel\")",
            f"<MESDLG>"
        ))
    return "".join((
        f"<MESDLG>",
        f"#ebox[%MBG](x:0,y:0,w:1024,h:768)",
        f"#pix[%PX1](%MBG[x:0,y:0,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
        f"#exec(LW_cfile&{sessionid}&lgdta.log)"
        f"#exec(LW_key&{profile[0]})",
        f"#exec(LW_gvar&"\
        f"%PROF&{profile[0]}&"\
        f"%NAME&{VE_NAME}&"\
        f"%NICK&{profile[1]}&"\
        f"%MAIL&{VE_MAIL}&"\
        f"%PASS&{VE_PASS}&"\
        f"%GMID&{VE_GMID}&"\
        f"%CHAT&{HOAE_IRC.address}&"\
        f"%CHNL1&{HOAE_IRC.ch1}\\00&"\
        f"%CHNL2&{HOAE_IRC.ch2}\\00)",
        f"<MESDLG>"))

# <MESDLG> 
# #ebox[%MBG](x:0,y:0,w:1024,h:768) 
# #def_dtbl_button_hotkey(13,27) 
# #table[%TBL](%MBG[x:287,y:285,w:450,h:200],{}{}{GW|open&log_new_form.dcml\00&up_dat=1^cansel=true^VE_PROF=139671^VE_MODE=edit^VE_NAME=<%GV_VE_NAME>^VE_NICK=hardkode1^VE_MAIL=<%GV_VE_MAIL>^VE_PASS=^VE_RASS=^VE_ICQ=<%GV_VE_ICQ>^VE_HOMP=<%GV_VE_HOMP>^VE_SEX=<%GV_VE_SEX>^VE_CNTRY=<%GV_VE_CNTRY>^VE_PHON=<%GV_VE_PHON>^VE_BIRTH=<%GV_VE_BIRTH>^accounts=139671\00|LW_lockall}{LW_file&Internet/Cash/l_games_btn.cml},1,0,11,362,"ERROR","An invalid Game Box Identifier was entered! Please enter more carefully. The number of attempts is limited. Press Edit button to check Game Box Identifier. Press Cancel to exit",24,"Edit","Cancel") 
# <MESDLG>