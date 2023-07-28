from ...common import genID
from ..config import IRCADDRESS, IRCCH1, IRCCH2
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
        f"%CHAT&{IRCADDRESS}&"\
        f"%CHNL1&{IRCCH1}\\00&"\
        f"%CHNL2&{IRCCH2}\\00)",
        f"<MESDLG>"))