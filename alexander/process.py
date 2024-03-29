from collections import defaultdict
from datetime import datetime
from common import clip, clip_string, reverse_address, extract_variables
from config import mysql_error_messages, alexander
from sqlalchemy import Engine, text
from sqlalchemy.exc import DBAPIError
from math import floor, ceil
from struct import unpack
from typing import Callable
from sqlalchemy.engine.row import RowMapping, Row


@alexander.route('cancel.dcml')
def cancel(**kwargs) -> str:
    return (
        '<NGDLG>'
        '<NGDLG>'
    )


@alexander.route('change_account2.dcml')
def change_account2(**kwargs) -> str:
    return (
        f'#ebox[%EBG](x:0,y:0,w:1024,h:768)'
        f'#edit[%E_CUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_CLANS_LAST_UPDATE}})'
        f'#exec(LW_cfile&\\00&Cookies/%GV_VE_NICK)'
        f'#exec(LW_cfile&\\00&Cookies/%GV_VE_PASS)'
        f'#exec(LW_cfile&\\00&Cookies/%GV_VE_GMID)'
        f'#exec(LW_cfile&\\00&Cookies/%GV_VE_AC)'
        f'#block(cancel.cml,l_g):<!goback!>\\00 '
        f'#end(l_g)'
        f'#table[%TBL](%EBG[x:251,y:247,w:523,h:381],{{}}{{}}{{GW|open&change.dcml\\00&cansel=true^accounts=^VE_NICK=<%GV_VE_NICK>^VE_GMID=<%GV_VE_GMID>^VE_PASS=<%GV_VE_PASS>^icon_last_update=<%GV_CLANS_LAST_UPDATE>^save_pass=<%GV_SAVE_PASS>\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},3,-1,1,2,11,368,\"OLD PROFILE\",,26,\"Login\",\"Cancel\")'
        f'#ebox[%LBX](x:270,y:143,w:500,h:220)'
        f'#pix[%PX2](%LBX[x:4,y:195,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)'
        f'#font(BC14,BC14,BC14)'
        f'#txt[%L_NICK](%LBX[x:4,y:234,w:100%,h:20],{{}},\"Nickname\")'
        f'#pan[%P_NICK](%LBX[x:151,y:234,w:324,h:14],1)'
        f'#edit[%E_NICK](%LBX[x:156,y:231,w:302,h:18],{{%GV_VE_NICK}},0,0,0,1)'
        f'#txt[%L_PASS](%LBX[x:4,y:265,w:100%,h:20],{{}},\"User Password\")'
        f'#pan[%P_PASS](%LBX[x:151,y:265,w:324,h:14],1)'
        f'#edit[%E_PASS](%LBX[x:156,y:262,w:302,h:20],{{%GV_VE_PASS}},0,0,1)'
        f'#txt[%L_BOXID](%LBX[x:4,y:296,w:100%,h:20],{{}},\"Game Box #ID\")'
        f'#pan[%P_BOXID](%LBX[x:151,y:296,w:324,h:14],1)'
        f'#edit[%E_BOXID](%LBX[x:156,y:293,w:302,h:20],{{%GV_VE_GMID}},0,0,1)'
        f'#pix[%PX3](%LBX[x:4,y:317,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)'
        f'#chk[%E_SAVE](%LBX[x:4,y:351,w:302,h:20],{{%GV_SAVE_PASS}},\"  Save password\",0,1,0)'
        f'#hint(%L_NICK,\"Enter your nickname\")'
        f'#hint(%L_PASS,\"Enter your password\")'
        f'#hint(%L_BOXID,\"Enter your GameBox ID#\")'
        f'#hint(%T_DELETE,\"Delete account\")'
        f'#hint(%E_SAVE,\"This option saves your password and Game Box #ID. Don\'t use it, if you play from computer accessible for other people.\")'
        f'<MESDLG> '
        f'<MESDLG> '
        f'#block(l_games_btn.cml,CAN)<MESDLG><MESDLG> '
        f'#end(CAN)'
    )


@alexander.route('change.dcml')
def change(variables: dict, **kwargs) -> str:
    if not (variables["VE_NICK"], variables["VE_PASS"], variables["VE_GMID"]):
        return (
            "<MESDLG>"
            "#ebox[%D](x:0,y:0,w:1024,h:768)"
            "<MESDLG>"
        )
    else:
        return (
            f'<MESDLG>'
            f'#ebox[%D](x:0,y:0,w:1024,h:768)'
            f'#exec(LW_cfile&{variables["accounts"]}\\00&Cookies/%GV_VE_ACCOUNTS)'
            f'#exec(GW|open&log_user.dcml\\00'
            f'&cansel={variables["cansel"]}'
            f'^save_pass={variables["save_pass"]}'
            f'^icon_last_update=1098287226'
            f'^VE_PROF={variables["VE_PROF"]}'
            f'^VE_NAME={variables["VE_NAME"]}'
            f'^VE_NICK={variables["VE_NICK"]}'
            f'^VE_MAIL={variables["VE_MAIL"]}'
            f'^VE_PASS={variables["VE_PASS"]}'
            f'^VE_GMID={variables["VE_GMID"]}'
            f'^accounts={variables["accounts"]}'
            f'\\00|LW_lockall)'
            f'<MESDLG>'
        )

@alexander.route('clan_admin2.dcml')
def clan_admin2(variables: dict, player_id, **kwargs) -> str:
    try:
        with alexander.engine.connect() as connection:
            connection.execute(text(
                f'CALL clan_admin({player_id}, {variables.get("new_jointer", 0)}, {variables.get("leaver", 0)}, {variables.get("clanID", 0)}, "{variables["again"]}")'
            ))
            connection.commit()
            return (
                f'<NGDLG>'
                f'#exec(GW|open&clan_users.dcml\\00&clanID={variables["clanID"]}\\00|LW_lockall)'
                f'<NGDLG>'
            )

    except DBAPIError as err:
        if err.orig:
            error_message = err.orig.args[1]
            if error_message == 'DLG_CLAN_REMOVE':
                return (
                    f'<NGDLG>'
                    f'#ebox[%L0](x:0,y:0,w:100%,h:100%)'
                    f'#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&clan_admin2.dcml\\00&again=true^clanID={variables["clanID"]}^new_jointer={player_id}\\00}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"NOTICE\",\"Delete clan [ SIGNATURE HERE ]?\",26,\"OK\",\"Cancel\")'
                    f'<NGDLG>'
                )
    return (
        f'<NGDLG>'
        f'#exec(GW|open&clans_list.dcml\\00|LW_lockall)'
        f'<NGDLG>'
    )


@alexander.route('clan_load_image.dcml')
def clan_load_image(variables: dict, **kwargs) -> str:
    if variables['signature'] and variables['icon_name']:
        return (
            f'<NGDLG>'
            f'#exec(GW|setclan&{variables["signature"]}.png\\00&<@%GV_CURFILE>&)'
            f'#exec(GW|open&clan_load_image.dcml\\00'
            f'&help=true^signature={variables["signature"]}^icon_name={variables["icon_name"]}.png^gdwrite=true'
            f'\\00|LW_lockall)'
            f'<NGDLG>'
        )
    else:
        return (
            f'<NGDLG> '
            f'#ebox[%L0](x:0,y:0,w:100%,h:100%)'
            f'#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&clan_load_image.dcml\\00'
            f'&help=true^signature={variables["signature"]}^icon_name=<%GV_CLAN_ICON>\\00|LW_lockall}}'
            f'{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"CLAN ICON\",\"\",26,\"Upload\",\"Cancel\")'
            f'#ebox[%BI](x:254,y:138,w:416,h:167)'
            f'#pan[%P1](%BI[x:181,y:14,w:175,h:141],5)'
            f'#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-3,6)'
            f'#def_scroll(Interf3/elements/scroll3,0,0)'
            f'#sbox[%FLBOX](x:437,y:152,w:175,h:140)'
            f'#font(BC12,BC12,BC12)'
            f'#txt[%L](%BI[x:5,y:14,w:100,h:24],{{}},\"Icon:\")'
            f'#pan[%P2](%BI[x:9,y:33,w:150,h:14],1)'
            f'#font(BC12,BC12,BC12)'
            f'#edit[%Eic](%BI[x:13,y:32,w:152,h:18],{{%GV_CLAN_ICON}})'
            f'#exec(LW_enb&0&%Eic)'
            f'#font(BC12,BC12,BC12)'
            f'#txt[%L](%BI[x:5,y:59,w:100,h:24],{{}},\"Disk:\")'
            f'#cbb[%DISK](%BI[x:4,y:71,w:162,h:18],{{%CBVAR}},\"-\")'
            f'#fbrowse({{%GV_FULLWAY}}{{%GV_CURFILE}}{{%GV_CLAN_ICON}},%DISK,%FLBOX,*.*)'
            f'<%FLBOX>'
            f'<%FLBOX>'
            f'<NGDLG>'
        )


@alexander.route('clan_new.dcml')
def clan_new(variables: dict, player_id: str | int, **kwargs) -> str:
    if variables['title'] and variables['signature']:
        with alexander.engine.connect() as connection:
            connection.execute(text(
                f'CALL create_clan({player_id}, "{variables["title"]}", "{variables["signature"]}", "{variables["info"]}")'))
            connection.commit()
        return (
            f'#ebox[%TB](x:0,y:0,w:100%,h:100%)'
            f'#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)'
            f'#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)'
            f'#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)'
            f'#font(RG18,RG18,RG18)'
            f'#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")'
            f'#font(BG18,BG18,BG18)'
            f'#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\")'
            f'#font(R2C12,R2C12,R2C12)'
            f'#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")'
            f'#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)'
            f'#font(RC12,R2C12,RC12)'
            f'#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")'
            f'#hint(%BT1,\"News, events, forum and punishment list\")'
            f'#font(RC12,RC12,RC12)'
            f'#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)'
            f'#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},'
            f'\"Player List\")'
            f'#hint(%BT2,\"Player list, personal mail and clan information\")'
            f'#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)'
            f'#font(RC12,R2C12,RC12)'
            f'#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")'
            f'#hint(%BT4,\"Play custom games\")#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)'
            f'#font(RC12,R2C12,RC12)'
            f'#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},'
            f'\"Scored Games\")'
            f'#hint(%BT5,\"Played games and their scores\")'
            f'#ebox[%B_VOTE](x:5,y:396,w:140,h:103)'
            f'<VOTING>'
            f'#exec(GW|open&voting.dcml\\00&question=46\\00)'
            f'<VOTING>'
            f'#exec(GW|open&clans_list.dcml\\00&create_icon=true^signature={variables["signature"]}\\00|LW_lockall)'
        )
    return (
        f'#block(l_games_btn.cml,l_g):<!goback!>\\00'
        f'#end(l_g)'
        f'#ebox[%TB](x:0,y:0,w:100%,h:100%)'
        f'#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)'
        f'#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)'
        f'#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)'
        f'#font(RG18,RG18,RG18)'
        f'#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")'
        f'#font(BG18,BG18,BG18)'
        f'#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\")'
        f'#font(R2C12,R2C12,R2C12)'
        f'#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")'
        f'#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)'
        f'#font(RC12,R2C12,RC12)'
        f'#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")'
        f'#hint(%BT1,\"News, events, forum and punishment list\")'
        f'#font(RC12,RC12,RC12)'
        f'#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)'
        f'#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},'
        f'\"Player List\")'
        f'#hint(%BT2,\"Player list, personal mail and clan information\")'
        f'#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)'
        f'#font(RC12,R2C12,RC12)'
        f'#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")'
        f'#hint(%BT4,\"Play custom games\")'
        f'#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)'
        f'#font(RC12,R2C12,RC12)'
        f'#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},'
        f'\"Scored Games\")'
        f'#hint(%BT5,\"Played games and their scores\")'
        f'#ebox[%B_VOTE](x:5,y:396,w:140,h:103)'
        f'<VOTING>'
        f'#exec(GW|open&voting.dcml\\00&question=46\\00)'
        f'<VOTING>'
        f'#ebox[%B](x:0,y:0,w:100%,h:100%)'
        f'#font(BC14,R2C14,RC14)'
        f'#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\")'
        f'#hint(%LIST1,\"Player list, personal mail and clan information\")'
        f'#font(RC14,GC14,RC14)'
        f'#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\")'
        f'#hint(%LIST2,\"Clans, their members and details\")'
        f'#exec(LW_cfile&\\00&Cookies/%GV_CLAN_TITLE)'
        f'#exec(LW_cfile&\\00&Cookies/%GV_CLAN_SIGNA)'
        f'#exec(LW_cfile&\\00&Cookies/%GV_CLAN_INFO)'
        f'#ebox[%B0](x:154,y:42,w:559,h:291)'
        f'#pan[%PAN](%B0[x:0,y:0,w:100%,h:100%],5)'
        f'#font(RC12,R2C12,RC12)'
        f'#txt[%TOP1](%B0[x:5,y:7,w:150,h:24],{{}},\"Create new clan\")'
        f'#pix[%PX](%B0[x:5,y:27,w:100%,h:100%],{{}},Internet/pix/i_pri0,25,25,25,25)'
        f'#font(R2C12,R2C12,RC12)'
        f'#txt[%T1](%B0[x:5,y:43,w:150,h:24],{{}},\"Clan title:\")'
        f'#font(BC12,BC12,RC12)'
        f'#pan[%P2](%B0[x:9,y:62,w:542,h:14],1)'
        f'#edit[%E1](%B0[x:13,y:61,w:535,h:18],{{%GV_CLAN_TITLE}},0,0,0,1)'
        f'#font(R2C12,R2C12,RC12)'
        f'#txt[%T2](%B0[x:5,y:88,w:120,h:24],{{}},\"Signature:\")'
        f'#font(BC12,BC12,RC12)'
        f'#pan[%P3](%B0[x:9,y:107,w:542,h:14],1)'
        f'#edit[%E2](%B0[x:13,y:106,w:535,h:18],{{%GV_CLAN_SIGNA}})'
        f'#font(R2C12,R2C12,RC12)'
        f'#txt[%T3](%B0[x:5,y:133,w:120,h:24],{{}},\"Clan info:\")'
        f'#font(BC12,BC12,RC12)'
        f'#pan[%P3](%B0[x:9,y:152,w:542,h:130],1)'
        f'#edit[%E3](%B0[x:13,y:152,w:535,h:130],{{%GV_CLAN_INFO}},1)'
        f'#font(BC14,WC14,BC14)'
        f'#sbtn[%Create](%B[x:521,y:377,w:100,h:305],{{GW|open&clan_new.dcml\\00&cansel=true^title=<%GV_CLAN_TITLE>^signature=<%GV_CLAN_SIGNA>^info=<%GV_CLAN_INFO>\\00|LW_lockall}},\"Create\")'
        f'#sbtn[%BT](%B[x:641,y:377,w:100,h:305],{{LW_file&Internet/Cash/l_games_btn.cml}},\"Cancel\")'
        f'<NGDLG>'
        f'<NGDLG>'
        f'#block(cancel.cml,CAN)'
        f'<NGDLG>'
        f'<NGDLG>'
        f'#end(CAN)'
    )


@alexander.route('clan_users.dcml')
def clan_users(variables: dict, player_id, **kwargs) -> str | None:
    members_list = []
    members_buttons = []
    if variables['clanID']:
        with alexander.engine.connect() as connection:
            clan = connection.execute(text(
                f"CALL get_clan_summary({variables['clanID']}, {player_id})"
            )).fetchone()
            if clan:
                clan = clan._mapping
                members = connection.execute(text(
                    f"CALL get_clan_members({variables['clanID']})"
                )).fetchall()
                for idx, member in enumerate(members):
                    member = member._mapping
                    members_buttons.append(
                        f"#apan[%APAN{idx}](%SB[x:0,y:{idx * 21}-2,w:100%,h:20],{{GW|open&user_details.dcml\\00&ID={member['player_id']}\\00|LW_lockall}},8) ")
                    members_list.append(
                        f",21,\"{member['state']}\",\"{member['nick']}\",\"{member['name']}\",\"{member['position']}\",\"{member['player_id']}\",\"{member['country']}\",\"{member['score']}\",\"{member['player_rank']}\"")
                members_list = "".join(members_list)
                members_buttons = "".join(members_buttons)
                join_leave_button = \
                    f"#sbtn[%BTXT1](%B[x:641,y:377,w:100,h:305],{{GW|open&clan_admin2.dcml\\00&clanID={variables['clanID']}^leaver={player_id}\\00|LW_lockall}},\"Leave clan\")" if \
                        clan['is_member'] == 1 else \
                        f"#sbtn[%BTXT1](%B[x:641,y:377,w:100,h:305],{{GW|open&clan_admin2.dcml\\00&clanID={variables['clanID']}^new_jointer={player_id}\\00|LW_lockall}},\"Join clan\")"
                return (
                    f"#ebox[%TB](x:0,y:0,w:100%,h:100%) "
                    f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12) "
                    f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13) "
                    f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10) "
                    f"#font(RG18,RG18,RG18) "
                    f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
                    f"#font(BG18,BG18,BG18) "
                    f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\") "
                    f"#font(R2C12,R2C12,R2C12) "
                    f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\") "
                    f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
                    f"#font(RC12,R2C12,RC12) "
                    f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
                    f"#hint(%BT1,\"News, events, forum and punishment list\")"
                    f"#font(RC12,RC12,RC12) "
                    f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1) "
                    f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},\"Player List\")"
                    f"#hint(%BT2,\"Player list, personal mail and clan information\")"
                    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                    f"#font(RC12,R2C12,RC12) "
                    f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
                    f"#hint(%BT4,\"Play custom games\")"
                    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                    f"#font(RC12,R2C12,RC12) "
                    f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
                    f"#hint(%BT5,\"Played games and their scores\")"
                    f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103) "
                    f"<VOTING> "
                    f"#exec(GW|open&voting.dcml\\00&question=46\\00) "
                    f"<VOTING> "
                    f"#ebox[%B](x:0,y:0,w:100%,h:100%) "
                    f"#font(BC14,R2C14,RC14) "
                    f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\") "
                    f"#hint(%LIST1,\"Player list, personal mail and clan information\") "
                    f"#font(RC14,GC14,RC14) "
                    f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\") "
                    f"#hint(%LIST2,\"Clans, their members and details\") "
                    f"#ebox[%B0](x:154,y:42,w:559,h:291) "
                    f"#font(BC12,BC12,RC12) "
                    f"#txt[%INFO0](%B0[x:12,y:64,w:540,h:18],{{}},\"{clan['info']}\") "
                    f"#exec(LW_vis&0&%INFO0) "
                    f"#pan[%PAN](%B0[x:0,y:0,w:100%,y1:%INFO0+9],5) "
                    f"#font(RC12,R2C12,RC12) "
                    f"#txt[%TOP1](%B0[x:5,y:7,w:150,h:24],{{}},\"Clan {clan['signature']}\") "
                    f"#pix[%PX](%B0[x:3,y:27,w:100%,h:100%],{{}},Internet/pix/i_pri0,25,25,25,25) "
                    f"#font(R2C12,R2C12,RC12) "
                    f"\\#txt[%TOP2](%B0[x:5,y:43,w:150,h:24],{{}},\"Info:\") "
                    f"#font(BC12,BC12,RC12) "
                    f"#pan[%PAN0](%B0[x:7,y:62,w:545,y1:%INFO0],1)"
                    f"#font(BC12,BC12,RC12) "
                    f"#txt[%INFO](%B0[x:12,y:64,w:540,h:20],{{}},\"{clan['info']}\")"
                    f"#font(R2C12,R2C12,RC12) "
                    f"#stbl[%TBL0](%B0[x:0,y:%INFO0+19,w:526-3,y1:D],{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=state^resort=\\00|LW_lockall}}{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=nick^resort=\\00|LW_lockall}}{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=name^resort=\\00|LW_lockall}}{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=position^resort=\\00|LW_lockall}}{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=id^resort=\\00|LW_lockall}}{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=country^resort=\\00|LW_lockall}}{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=score^resort=1\\00|LW_lockall}}{{GW|open&clan_users.dcml\\00&clanID={variables['clanID']}^order=score^resort=1\\00|LW_lockall}},8,7,10%,1,21%,1,20%,1,8%,1,6%,1,14%,1,8%,1,13%,1,20,\"{{State\",\"{{Nickname\",\"{{Full Name\",\"{{Pos\",\"{{#\",\"{{Country\",\"{{Scores\",\"{{Rank\") "
                    f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-21,25) "
                    f"#sbox[%SB](%B0[x:0-4,y:%PAN+28,w:526+4,y1:D-2]) "
                    f"{members_buttons}"
                    f"#ebox[%LB](x:0,y:4,w:100%,h:100%) "
                    f"#font(BC12,R2C12,RC12) "
                    f"#stbl[%TBL](%SB[x:4,y:0,w:526-3,h:42],{{}},8,0,10%,1,21%,1,20%,1,8%,1,6%,1,14%,1,8%,1,13%,1{members_list})"
                    f"#font(BC14,WC14,BC14) "
                    f"{join_leave_button}"
                    f"<NGDLG> "
                    f"<NGDLG> "
                    f"#block(cancel.cml,CAN)<NGDLG> "
                    f"<NGDLG> "
                    f"#end(CAN)"
                    )
    return (
        f'<NGDLG>'
        f'#exec(GW|open&clans_list.dcml\\00|LW_lockall)'
        f'<NGDLG>'
    )


@alexander.route('clans_list.dcml')
def clans_list(variables: dict, **kwargs) -> str:
    button_list = []
    clan_list = []
    icon_dialog = ""
    if variables['create_icon'] == "true":
        icon_dialog = (
            f"#ebox[%L0](x:0,y:0,w:100%,h:100%)"
            f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&clan_load_image.dcml\\00&help=true^signature=SAM\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"CLAN ICON\",\"You are recommended to use a .jpg or .png 32x24 file as a clan icon.If the resolution of the file is greater, then it will be automatically miniaturized to 32x24 resolution saving the proportions. Size must be smaller than 16 KB. It is restricted to use pornographic or erotic images, nazi symbols and obscenities. The icon will be displayed in chat window within a day.\",26,\"OK\",\"Cancel\")"
        )
    with alexander.engine.connect() as connection:
        clans = connection.execute(text(
            "CALL get_clans()"
        )).fetchall()
        if clans:
            for idx, entry in enumerate(clans):
                clans = entry._mapping
                button_list.append(
                    f"#apan[%BT{idx}](%SB[x:0,y:{idx * 21}-2,w:100%,h:20],{{GW|open&clan_users.dcml\\00&clanID={clans.id}\\00|LW_lockall}},8)"
                )
                clan_list.append(
                    f",21,\"{clans.title}\",\"{clans.signature}\",\"{clans.created_at}\",\"{clans.nick}\",\"{clans.members}\",\"{clans.score}\",\"{clans.average_score}\""
                )
    button_list = "".join(button_list)
    clan_list = "".join(clan_list)
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(BC14,R2C14,RC14)"
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\")"
        f"#hint(%LIST1,\"Player list, personal mail and clan information\")"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\")"
        f"#hint(%LIST2,\"Clans, their members and details\")"
        f"#font(BC14,WC14,BC14)"
        f"#sbtn[%BT](%B[x:641,y:377,w:100,h:305],{{GW|open&clan_new.dcml\\00|LW_lockall}},\"Create new clan\")"
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%)"
        f"#font(RC12,R2C12,RC12)"
        f"#stbl[%TBL](%B[x:154,y:42,w:526-3,h:291],{{GW|open&clans_list.dcml\\00&order=title^resort=1\\00|LW_lockall}}{{GW|open&clans_list.dcml\\00&order=sign^resort=1\\00|LW_lockall}}{{GW|open&clans_list.dcml\\00&order=c.birthday^resort=\\00|LW_lockall}}{{GW|open&clans_list.dcml\\00&order=father^resort=1\\00|LW_lockall}}{{GW|open&clans_list.dcml\\00&order=count^resort=\\00|LW_lockall}}{{GW|open&clans_list.dcml\\00&order=score^resort=1\\00|LW_lockall}}{{GW|open&clans_list.dcml\\00&order=avg^resort=\\00|LW_lockall}},7,7,16,1,15,1,12,1,20,1,10,1,13,1,14,1,20,\"{{Title\",\"{{Signature\",\"{{Birthday\",\"{{Creator\",\"{{Members\",\"{{Total score\",\"{{Avg(score)\")"
        f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-21,25)"
        f"#sbox[%SB](x:150,y:60,w:526+4,h:271)"
        f"{button_list}"
        f"#font(BC12,BC12,BC12)"
        f"#stbl[%CLA_LST](%SB[x:4,y:0,w:526-3,h:588],{{}},7,0,16,1,15,1,12,1,20,1,10,1,13,1,14,1{clan_list})"
        f"<NGDLG>"
        f"{icon_dialog}"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('dbtbl.dcml')
def dbtbl(**kwargs) -> str:
    with alexander.engine.connect() as connection:
        lobbies = connection.execute(text(
            f"CALL get_lobbies()")).fetchall()
    ping_list = "".join(
        [f"#apan[%APAN{idx}](%SB[x:0,y:{idx * 21}-2,w:100%,h:20]," \
         f"{{GW|open&join_game.dcml\\00&delete_old=true^id_room={str(lobby[0])}\\00|LW_lockall}},8)" \
         f"#font(BC12,BC12,BC12)" \
         f"#ping[%PING{idx}](%SB[x:86%+30,y:{str(idx * 21)}+4,w:14,h:20]," \
         f"{reverse_address(lobby[-2])})"
         for idx, lobby in enumerate(lobbies)])
    lobbies = "".join(
        [f',21,{str(lobby[1])} [{"Y" if lobby[6] else "N"}], {lobby[-1]},"{lobby[3]}","{lobby[5]}/{lobby[4]}",""' for
         lobby in lobbies])
    return (
        f"<DBTBL>"
        f"#exec(LW_time&{1000 * alexander.dbtbl_interval}&l_games_btn.cml\\00)"
        f"#block(l_games_btn.cml,l_g):GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall"
        f"#end(l_g)"
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%)"
        f"#font(R2C12,R2C12,RC12)"
        f"#stbl[%TBL](%BB[x:154,y:42,w:523,h:291],{{GW|open&dbtbl.dcml\\00&order=r.title^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=u.nick^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=t.name^resort=\\00|LW_lockall}}{{}}{{}},5,7,33,1,25,1,14,1,14,1,14,1,20,\"{{Game Title [Password]\",\"{{Host\",\"{{Type\",\"Players\",\"Ping\")"
        f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-21,25)"
        f"#sbox[%SB](x:150,y:60,w:526+4,h:271)"
        f"{ping_list}"
        f"#font(BC12,BC12,BC12)"
        f"#stbl[%ROOM_LST](%SB[x:4,y:0,w:523,h:21],{{}},5,0,33,0,25,1,14,1,14,1,14,1"
        f"{lobbies}"
        f")#font(BC14,WC14,BC14)"
        f"#sbtn[%B_J](%BB[x:401,y:377,w:100,h:305],{{GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall}},\"Refresh\")"
        f"<DBTBL>"
    )


@alexander.route('forum_add.dcml')
def forum_add(variables: dict, player_id: str | int, **kwargs) -> str:
    if variables['add_message']:
        with alexander.engine.connect() as connection:
            if variables['theme'] != '':
                connection.execute(text(
                    f'INSERT INTO thread_messages (author_id, thread_id, content) VALUES ({player_id}, {variables["theme"]}, "{variables["add_message"]}")'))
            else:
                connection.execute(text(
                    f'INSERT INTO threads (author_id, content) VALUES ({player_id}, "{variables["add_message"]}")'))
            connection.commit()
            return "#exec(GW|open&forum.dcml\\00&mode=1^last_view=^noback=true\\00|LW_lockall)"
    return (
        f"#block(l_games_btn.cml,l_g):<!goback!>\\00"
        f"#end(l_g)"
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(R2C14,R2C14,RC14)"
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")"
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")"
        f"#hint(%LIST2,\"List of punished players\")"
        f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=\\00|LW_lockall}},\"{{Forum}}\")"
        f"#hint(%LIST3,\"Read and write forum messages\")"
        f"#font(RC12,GC12,RC12)  "
        f"#ctxt[%LIST4](%B[x:0,y:%LIST3-10,w:146,h:24],{{GW|open&forum_add.dcml\\00&cansel=true^theme=^last_view=\\00|LW_lockall}},\"{{Add theme}}\")"
        f"#hint(%LIST4,\"Create a new forum theme\")"
        f"#exec(LW_cfile&\\00&Cookies/%GV_MESSAGE)"
        f"#ebox[%B0](x:154,y:42,w:559,h:291)"
        f"#pan[%PAN](%B0[x:0,y:0,w:100%,h:100%],5)"
        f"#font(RC14,R2C14,RC14)"
        f"#txt[%TOP1](%B0[x:4,y:5,w:150,h:24],{{}},\"Add theme\")"
        f"#pix[%PX](%B0[x:4,y:27,w:100%,h:100%],{{}},Internet/pix/i_pri0,25,25,25,25)"
        f"#font(R2C12,R2C12,RC12)"
        f"#txt[%TOP2](%B0[x:4,y:41,w:150,h:24],{{}},\"Theme:\")"
        f"#font(BC12,GC12,GC12)"
        f"#pan[%PAN](%B0[x:8,y:60,w:543,h:218],1)"
        f"#edit[%NEWS](%B0[x:13,y:60,w:535,h:218],{{%GV_MESSAGE}},1,0,0,1)"
        f"#font(BC14,WC14,BC14)"
        f"#sbtn[%BT](%B[x:521,y:377,w:100,h:305],{{GW|open&forum_add.dcml\\00&cansel=true^last_view=^mode=1^add_message=<%GV_MESSAGE>^theme={variables['theme']}\\00|LW_lockall}},\"Save\")"
        f"#sbtn[%BT](%B[x:641,y:377,w:100,h:305],{{LW_file&Internet/Cash/l_games_btn.cml}},\"Cancel\")<NGDLG><NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG><NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('forum_search.dcml')
def forum_search(**kwargs) -> str:
    return (
        f"<NGDLG>"
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)"
        f"#ebox[%L](x:244,y:140,w:415,h:165)"
        f"#exec(LW_cfile&\\00&Cookies/%GV_SEARCH_NICK)"
        f"#exec(LW_cfile&\\00&Cookies/%GV_SEARCH_TEXT)"
        f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&forum.dcml\\00&last_view=^search_nick=<%GV_SEARCH_NICK>^search_text=<%GV_SEARCH_TEXT>\\00|LW_lockall}}{{GW|open&forum.dcml\\00|LW_lockall}},2,0,3,13,252,\"SEARCH\",,26,\"Search\",\"Cancel\")"
        f"#font(BC12,RC12,RC12)"
        f"#txt[%L_NICK](%L[x:10,y:14,w:120,h:20],{{}},\"Author:\")"
        f"#pan[%P_NICK](%L[x:15,y:33,w:382,h:14],1)"
        f"#font(BC12,GC12,GC12)"
        f"#edit[%E_NICK](%L[x:19,y:32,w:386,h:18],{{%GV_SEARCH_NICK}},0,0,0,1)"
        f"#font(BC12,RC12,RC12)"
        f"#txt[%L_TEXT](%L[x:10,y:62,w:320,h:20],{{}},\"Text:\")"
        f"#pan[%P_TEXT](%L[x:15,y:81,w:382,h:65],1)"
        f"#font(BC12,GC12,GC12)"
        f"#edit[%E_TEXT](%L[x:19,y:81,w:382,h:65],{{%GV_SEARCH_TEXT}},1)"
        f"<NGDLG>"
    )


@alexander.route('forum_view.dcml')
def forum_view(variables: dict, **kwargs) -> str:
    with alexander.engine.connect() as connection:
        if variables['theme']:
            thread = connection.execute(text(f"""CALL get_thread({variables['theme']})""")).fetchone()
            if thread:
                thread = thread._mapping
                messages = connection.execute(text(f"""CALL get_thread_messages({thread['id']})"""))
                message_list = []
                for idx, entry in enumerate(messages):
                    message = entry._mapping
                    message_list.append("".join([
                        f"#font(R2C12,R2C12,RC12)",
                        f"#txt[%S_DATE{idx + 1}](%SB[x:7,y:{'6' if idx == 0 else f'%P{idx}-22'},w:170,h:24],{{}},\"Date:\")",
                        f"#font(BC12,R2C12,RC12)",
                        f"#txt[%DATE{idx + 1}](%SB[x:%S_DATE{idx + 1}+5,y:{'6' if idx == 0 else f'%P{idx}-22'},w:170,h:24],{{}},\"{message['created_at']}\")",
                        f"#font(R2C12,BC12,RC12)",
                        f"#txt[%S_CR{idx + 1}](%SB[x:7,y:{'6' if idx == 0 else f'%P{idx}-22'}+14,w:170,h:24],{{}},\"Author:\")",
                        f"#txt[%CR{idx + 1}](%SB[x:%S_CR{idx + 1}+5,y:{'6' if idx == 0 else f'%P{idx}-22'}+14,w:170,h:24],{{GW|open&user_details.dcml&ID={message['author_id']}|LW_lockall}},\"{{{message['nick']}}}\")",
                        f"#font(BC12,RC12,RC12)",
                        f"#txt[%TEXT{idx + 1}](%SB[x:215,y:{'6' if idx == 0 else f'%P{idx}-22'},w:100%-220+0,h:24],{{}},\"{message['content']}\")",
                        f"#pan[%P{idx + 1}](%SB[x:0-32,y:%CR{idx + 1}>%TEXT{idx + 1}+37,w:100%+65,h:0],9)",
                    ]))
                message_list = "".join(message_list)
                return (
                    f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
                    f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
                    f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
                    f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
                    f"#font(RG18,RG18,RG18)"
                    f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
                    f"#font(BG18,BG18,BG18)"
                    f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")"
                    f"#font(R2C12,R2C12,R2C12)"
                    f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")  "
                    f"#font(RC12,RC12,RC12)  "
                    f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
                    f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")"
                    f"#hint(%BT1,\"News, events, forum and punishment list\")"
                    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                    f"#font(RC12,R2C12,RC12)  "
                    f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
                    f"#hint(%BT2,\"Player list, personal mail and clan information\")"
                    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)  "
                    f"#font(RC12,R2C12,RC12)  "
                    f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
                    f"#hint(%BT4,\"Play custom games\")"
                    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)  "
                    f"#font(RC12,R2C12,RC12)  "
                    f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
                    f"#hint(%BT5,\"Played games and their scores\") "
                    f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103) <VOTING> "
                    f"#exec(GW|open&voting.dcml\\00&question=46\\00) <VOTING>"
                    f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
                    f"#font(R2C14,R2C14,RC14)"
                    f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\") "
                    f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\") "
                    f"#hint(%LIST2,\"List of punished players\") "
                    f"#font(RC14,GC14,RC14)"
                    f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=\\00|LW_lockall}},\"{{Forum}}\")"
                    f"#hint(%LIST3,\"Read and write forum messages\") "
                    f"#font(RC12,R2C12,RC12) "
                    f"#ctxt[%LIST4](%B[x:0,y:%LIST3-10,w:146,h:24],{{GW|open&forum_add.dcml\\00&theme={thread['id']}^last_view=\\00|LW_lockall}},\"{{Add message}}\")"
                    f"#hint(%LIST4,\"Write new post on current theme\") "
                    f"#ctxt[%LIST5](%B[x:0,y:%LIST4-1,w:146,h:24],{{GW|open&forum_search.dcml\\00&last_view=\\00|LW_lockall}},\"{{Search}}\") "
                    f"#hint(%LIST5,\"Search a message by author or text\")"
                    f"#ebox[%B01](x:154,y:42,w:559,h:291)"
                    f"#font(GC12,R2C12,RC12)"
                    f"#txt[%TEXT01](%B01[x:220,y:7,w:330+0,h:24],{{}},\"{thread['content']}\")"
                    f"#exec(LW_vis&0&%TEXT01)"
                    f"#pan[%PAN_T](%B01[x:0,y:0,w:100%,y1:%TEXT01>35+3],7)"
                    f"#pan[%PAN01](%B01[x:245,y:0-34,w:0,y1:%PAN_T+34],10)"
                    f"#font(R2C12,R2C12,RC12)"
                    f"#txt[%S_DATE0](%B01[x:8,y:7,w:170,h:24],{{}},\"Date:\")"
                    f"#font(BC12,R2C12,RC12)"
                    f"#txt[%DATE0](%B01[x:%S_DATE0+5,y:7,w:170,h:24],{{}},\"{thread['created_at']}\")"
                    f"#font(R2C12,BC12,RC12)"
                    f"#txt[%S_CR0](%B01[x:8,y:21,w:170,h:24],{{}},\"Author:\")"
                    f"#txt[%CR0](%B01[x:%S_CR0+5,y:21,w:170,h:24],{{GW|open&user_details.dcml\\00&ID={thread['author_id']}\\00|LW_lockall}},\"{{{thread['nick']}}}\")"
                    f"#font(GC12,R2C12,RC12)"
                    f"#txt[%TEXT0](%B01[x:220,y:7,w:330+0,h:24],{{}},\"{thread['content']}\")"
                    f"#pan[%PAN](%B01[x:0,y:%PAN_T+10,w:559,y1:D],5)"
                    f"#pan[%PAN](%B01[x:9,y:%PAN_T+19,w:526-17,y1:D-9],3)"
                    f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-4,8)"
                    f"#sbox[%SB](%B01[x:7,y:%PAN_T+20,w:526-14,y1:D-11])"
                    f"#pan[%PAN0](%B01[x:245,y:%PAN_T-15,w:0,y1:%PAN+34],10)"
                    f"{message_list}"
                    f"#font(BC14,WC14,BC14)"
                    f"#sbtn[%BTXT1](%B[x:641,y:377,w:100,h:305],{{<!goback!>}},\"Back\")<NGDLG><NGDLG>"
                    f"#block(cancel.cml,CAN)<NGDLG><NGDLG>"
                    f"#end(CAN)"
                )
    return (
        f'<NGDLG>'
        f'#exec(GW|open&forum.dcml\\00|LW_lockall)'
        f'<NGDLG>'
    )

@alexander.route('forum.dcml')
def forum(variables: dict, **kwargs) -> str:
    thread_strings = ""
    thread_list = []
    search = False
    if variables['mode'] not in ('1', '2', '3', '4'):
        variables['mode'] = '1'
    if variables['search_nick'] or variables['search_text']:
        search = True
    with alexander.engine.connect() as connection:
        threads = connection.execute(
            text(f'CALL forum_search(\"{variables["search_nick"]}\", \"{variables["search_text"]}\" )')).fetchall()
        threads = connection.execute(text(
            f"CALL get_thread_list({variables['mode']}, {int(variables['next_message']) if variables['next_message'] else 0})")).fetchall()
        for idx, entry in enumerate(threads[:30]):
            thread = entry._mapping
            thread_list.append(" ".join([
                f"#font(BC12,RC12,RC12)",
                f"""#txt[%TXT{idx + 1}](%SB[x:218,y:{'4' if idx == 0 else f'%P{idx}-21'},w:100%-215,h:24],{{}},\"{thread['content'].replace(variables['search_text'], '{' + variables['search_text'] + '}') if search else thread['content']}\")""",
                f"#exec(LW_vis&0&%TXT{idx + 1})",
                f"#apan[%PAN{idx + 1}](%SB[x:0,y:{'4' if idx == 0 else f'%P{idx}-21'}-10,w:100%,y1:{'4' if idx == 0 else f'%P{idx}-21'}+{'42' if variables['mode'] == '1' else '28'}>%TXT{idx + 1}+5],{{GW|open&forum_view.dcml&last_view=0^theme={thread['id']}|LW_lockall}},14,\"\")",
                f"#font(BC12,RC12,RC12)",
                f"#txt[%TEXT{idx + 1}](%SB[x:218,y:{'4' if idx == 0 else f'%P{idx}-21'},w:100%-220,h:24],{{}},\"{thread['content'].replace(variables['search_text'], '{' + variables['search_text'] + '}') if search else thread['content']}\")",
                f"#font(R2C12,R2C12,RC12)",
                f"#txt[%S_DATE{idx + 1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'},w:170,h:24],{{}},\"Date:\")",
                f"#font(BC12,R2C12,RC12)",
                f"#txt[%DATE{idx + 1}](%SB[x:%S_DATE{idx + 1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'},w:170,h:24],{{}},\"{thread['created_at']}\")",
                f"#font(R2C12,BC12,RC12)",
                f"#txt[%S_CR{idx + 1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+14,w:170,h:24],{{}},\"Author:\")",
                f"#txt[%CR{idx + 1}](%SB[x:%S_CR{idx + 1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+14,w:170,h:24],{{GW|open&user_details.dcml&ID={thread['author_id']}|LW_lockall}},\"{{{thread['nick']}}}\")",
                f"#txt[%S_COU{idx + 1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+28,w:170,h:24],{{}},\"Message:\")" if
                variables['mode'] == '1' else '',
                f"#font(BC12,BC12,BC12)",
                f"#txt[%COU{idx + 1}](%SB[x:%S_COU{idx + 1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+28,w:170,h:24],{{}},\"{thread['messages']}\")" if
                variables["mode"] == "1" else "",
                f"#pan[%P{idx + 1}](%SB[x:0-32,y:{'4' if idx == 0 else f'%P{idx}-21'}+{'42' if variables['mode'] == '1' else '28'}>%TEXT{idx + 1}+38,w:100%+65,h:0],9)",
            ]))
    thread_strings = "".join(thread_list) + \
                     f"#ebox[%B1](x:0,y:0,w:100%,h:100%)\
        #pan[%PAN0](%B1[x:390,y:8,w:0,h:359],10)" if thread_list else "".join([
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%BT3](%B[x:684,y:377,w:15,h:305],{{GW|open&forum.dcml\\00&mode=^next_message={int(variables['next_message']) + 30 if variables['next_message'] else 0}^last_view=0^search_nick=^search_text=\\00|LW_lockall}},\"Next\")" if len(
            threads) > 29 else "",
    ]) if threads else "".join([
        f"#font(RG18,RG18,RG18)", f"#ctxt[%T0](%B[x:154,y:179,w:523,h:20],{{}},\"{{No search results}}\")"]),
    return (
        f"#exec(LW_cfile&20230722144507&Cookies/%GV_FORUM_LAST_TIME)"
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:10%)"
        f"#font(R2C14,R2C14,RC14)"
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")"
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")"
        f"#hint(%LIST2,\"List of punished players\")"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=0\\00|LW_lockall}},\"{{Forum}}\")"
        f"#hint(%LIST3,\"Read and write forum messages\")"
        f"{'#font(RC12,GC12,RC12)' if variables['mode'] == '1' else '#font(RC12,R2C12,RC12)'}"
        f"#ctxt[%LIST4](%B[x:0,y:%LIST3-10,w:146,h:24],{{GW|open&forum.dcml\\00&mode=1^last_view=0\\00|LW_lockall}},\"{{All themes}}\")"
        f"{'#font(RC12,GC12,RC12)' if variables['mode'] == '2' else '#font(RC12,R2C12,RC12)'}"
        f"#ctxt[%LIST5](%B[x:0,y:%LIST4-1,w:146,h:24],{{GW|open&forum.dcml\\00&mode=2^last_view=0\\00|LW_lockall}},\"{{Last 10 messages}}\")"
        f"{'#font(RC12,GC12,RC12)' if variables['mode'] == '3' else '#font(RC12,R2C12,RC12)'}"
        f"#ctxt[%LIST6](%B[x:0,y:%LIST5-1,w:146,h:24],{{GW|open&forum.dcml\\00&mode=3^last_view=0\\00|LW_lockall}},\"{{Messages for this day}}\")"
        f"{'#font(RC12,GC12,RC12)' if variables['mode'] == '4' else '#font(RC12,R2C12,RC12)'}"
        f"#ctxt[%LIST7](%B[x:0,y:%LIST6-1,w:146,h:24],{{GW|open&forum.dcml\\00&mode=4^last_view=0\\00|LW_lockall}},\"{{Messages for this week}}\")"
        f"#font(RC12,R2C12,RC12)"
        f"#ctxt[%LIST8](%B[x:0,y:%LIST7-1,w:146,h:24],{{GW|open&forum_add.dcml\\00&last_view=0\\00|LW_lockall}},\"{{Add theme}}\")"
        f"#hint(%LIST8,\"Create a new forum theme\")"
        f"#font(RC12,R2C12,RC12)"
        f"#ctxt[%LIST9](%B[x:0,y:%LIST8-1,w:146,h:24],{{GW|open&forum_search.dcml\\00&last_view=0\\00|LW_lockall}},\"{{Search}}\")"
        f"#hint(%LIST9,\"Search a message by author or text\")"
        f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)"
        f"#sbox[%SB](x:150,y:42+4,w:526+4,h:291-8)"
        f"{thread_strings}"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('games.dcml')
def games(**kwargs) -> str:
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"CUSTOM GAMES\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1) "
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"Lobbies\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1) "
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1) "
        f"#gpbtn[%BT4](%TB[x:318,y:22,w:-22,h:-18],{{}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1) "
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%TIT1](%B[x:0,y:106,w:146,h:24],{{GW|open&games.dcml\\00|LW_lockall}},\"{{Custom Games}}\")"
        f"#hint(%TIT1,\"Play custom games\")"
        f"#font(R2C14,R2C14,RC14)"
        f"#ctxt[%LIST33](%B[x:0,y:%TIT1-9,w:146,h:24],{{GW|open&rating_help.dcml\\00|LW_lockall}},\"{{Rating Describe}}\")"
        f"#pan[%PAN](%B[x:154,y:42,w:523,h:291],7)"
        f"#font(BC14,WC14,BC14)"
        f"#sbtn[%B_R](%B[x:521,y:377,w:100,h:305],{{GW|open&random_game_dlg.dcml\\00|LW_lockall}},\"Fight\")"
        f"#sbtn[%B_C](%B[x:641,y:377,w:100,h:305],{{GW|open&new_game_dlg.dcml\\00&delete_old=true\\00|LW_lockall}},\"Create\")<DBTBL>"
        f"#exec(GW|open&dbtbl.dcml\\00)<DBTBL><NGDLG><NGDLG>"
        f"#block(cancel.cml,CAN)<NGDLG><NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('join_game.dcml')
def join_game(variables: dict, player_id: str, **kwargs) -> str:
    with alexander.engine.connect() as connection:
        lobby = connection.execute(text(
            f"SELECT players, max_players, ip, password, (SELECT nick FROM players WHERE players.player_id = "
            f"lobbies.host_id) as nick, host_id FROM lobbies WHERE id = {variables['id_room']} LIMIT 1")).fetchone()
    if lobby:
        if lobby.max_players <= lobby.players:
            return (
                f"<NGDLG>"
                f"#ebox[%L0](x:0,y:0,w:100%,h:100%)"
                f"#pix[%PX1](%L0[x:0-62,y:0-136,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)"
                f"#exec(LW_enbbox&0&%L0)"
                f"#exec(LW_enbbox&0&%B)"
                f"#exec(LW_enbbox&0&%FLBOX)"
                f"#exec(LW_enbbox&0&%BP)"
                f"#exec(LW_enbbox&0&%L)"
                f"#exec(LW_enbbox&0&%BB)"
                f"#exec(LW_enbbox&0&%B1)"
                f"#exec(LW_enbbox&0&%BG)"
                f"#exec(LW_enbbox&0&%B2)"
                f"#exec(LW_enbbox&0&%BPANEL)"
                f"#exec(LW_enbbox&0&%BPANEL2)"
                f"#exec(LW_enbbox&0&%TB)"
                f"#exec(LW_enbbox&0&%B_VOTE)"
                f"#exec(LW_enbbox&0&%MBG)"
                f"#exec(LW_enbbox&0&%B0)"
                f"#exec(LW_enbbox&0&%M)"
                f"#exec(LW_enbbox&0&%LB)"
                f"#exec(LW_enbbox&0&%MB)"
                f"#exec(LW_enbbox&0&%EBG)"
                f"#exec(LW_enbbox&0&%LBX)"
                f"#exec(LW_enbbox&0&%BARDLD)"
                f"#exec(LW_enbbox&0&%BF2)"
                f"#exec(LW_enbbox&0&%B01)"
                f"#exec(LW_enbbox&0&%BF)"
                f"#exec(LW_enbbox&0&%BTABLE2)"
                f"#exec(LW_enbbox&0&%SB)"
                f"#ebox[%BTABLE](x:0,y:0,w:100%,h:100%)"
                f"#font(BC12,BC12,BC12)"
                f"#def_panel(11,Interf3/elements/b02,21,20,14,15,4,5,12,16,8,8)"
                f"#pan[%MPN](%BTABLE[x:242,y:115+15,w:415,h:220-15],11)"
                f"#pix[%PXP1](%BTABLE[x:242+20,y:115+20,w:100%,h:100%],{{}},Internet/pix/i_pri0,32,32,32,32)"
                f"#pix[%PX2](%BTABLE[x:522,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                f"#pix[%PX3](%BTABLE[x:327,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                f"#pix[%PX4](%BTABLE[x:377,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                f"#pix[%PX5](%BTABLE[x:427,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                f"#pix[%PX6](%BTABLE[x:477,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                f"#pix[%PX0](%BTABLE[x:317,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)"
                f"#pix[%PX1](%BTABLE[x:572,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)"
                f"#font(BG18,BG18,RG18)"
                f"#ctxt[%TTEXT](%BTABLE[x:242,y:115-1,w:415,h:20],{{0}},\"ERROR\")"
                f"#font(BC12,RC12,RC12)"
                f"#ctxt[%MTEXT0](%BTABLE[x:242+20,y:115+22,w:415-40,h:20],{{}},\"This lobby is full\")"
                f"#exec(LW_vis&0&%MTEXT0)"
                f"#ctxt[%MTEXT](%BTABLE[x:242+20,yc:225-3,w:415-40,h:%MTEXT0-115-159],{{}},\"This lobby is full\")"
                f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)"
                f"#font(WG14,BG14,WG14)"
                f"#gpbtn[%PXBT](%BTABLE[x:520-433,y:303-16,w:100%,h:70],{{GW|open&cancel.dcml\\00|LW_lockall}},\"OK\")"
                f"<NGDLG>"
            )
        elif lobby.host_id == player_id:
            return (
                "<NGDLG>"
                "#exec(LW_cfile&\\00&Cookies/%GV_VE_PASSWD)"
                "#ebox[%BF](x:0,y:0,w:100%,h:100%)"
                "#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&cancel.dcml\\00&id_room={id_room}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"You cannot join your own room!\",26,\"OK\")"
                "<NGDLG>"
            )
        else:
            if lobby.password:
                if variables['password'] == "":
                    return (
                        f"<NGDLG>"
                        f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASSWD)"
                        f"#ebox[%BF](x:0,y:0,w:100%,h:100%)"
                        f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{"
                        f"GW|open&join_game.dcml\\00&delete_old=true^id_room="
                        f"{variables['id_room']}^password=<%GV_VE_PASSWD>\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,"
                        f"0,3,13,252,\"JOIN\",,26,\"JOIN\",\"Cancel\")"
                        f"#ebox[%L](x:245,y:100,w:450,h:210)"
                        f"#font(BC12,RC12,RC12)"
                        f"#txt[%L_PASS](%L[x:11,y:95,w:360,h:20],{{}},\"Enter the password:\")"
                        f"#pan[%P_PASS](%L[x:15,y:114,w:382,h:14],1)"
                        f"#font(BC12,GC12,GC12)"
                        f"#edit[%E_PASS](%L[x:19,y:113,w:377,h:18],{{%GV_VE_PASSWD}},0,0,1,1)"
                        f"<NGDLG>"
                    )
                elif variables['password'] != lobby.password:
                    return (
                        f"<NGDLG>"
                        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)"
                        f"#pix[%PX1](%L0[x:0-62,y:0-136,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)"
                        f"#exec(LW_enbbox&0&%L0)"
                        f"#exec(LW_enbbox&0&%B)"
                        f"#exec(LW_enbbox&0&%FLBOX)"
                        f"#exec(LW_enbbox&0&%BP)"
                        f"#exec(LW_enbbox&0&%L)"
                        f"#exec(LW_enbbox&0&%BB)"
                        f"#exec(LW_enbbox&0&%B1)"
                        f"#exec(LW_enbbox&0&%BG)"
                        f"#exec(LW_enbbox&0&%B2)"
                        f"#exec(LW_enbbox&0&%BPANEL)"
                        f"#exec(LW_enbbox&0&%BPANEL2)"
                        f"#exec(LW_enbbox&0&%TB)"
                        f"#exec(LW_enbbox&0&%B_VOTE)"
                        f"#exec(LW_enbbox&0&%MBG)"
                        f"#exec(LW_enbbox&0&%B0)"
                        f"#exec(LW_enbbox&0&%M)"
                        f"#exec(LW_enbbox&0&%LB)"
                        f"#exec(LW_enbbox&0&%MB)"
                        f"#exec(LW_enbbox&0&%EBG)"
                        f"#exec(LW_enbbox&0&%LBX)"
                        f"#exec(LW_enbbox&0&%BARDLD)"
                        f"#exec(LW_enbbox&0&%BF2)"
                        f"#exec(LW_enbbox&0&%B01)"
                        f"#exec(LW_enbbox&0&%BF)"
                        f"#exec(LW_enbbox&0&%BTABLE2)"
                        f"#exec(LW_enbbox&0&%SB)"
                        f"#ebox[%BTABLE](x:0,y:0,w:100%,h:100%)"
                        f"#font(BC12,BC12,BC12)"
                        f"#def_panel(11,Interf3/elements/b02,21,20,14,15,4,5,12,16,8,8)"
                        f"#pan[%MPN](%BTABLE[x:242,y:115+15,w:415,h:220-15],11)"
                        f"#pix[%PXP1](%BTABLE[x:242+20,y:115+20,w:100%,h:100%],{{}},Internet/pix/i_pri0,32,32,32,32)"
                        f"#pix[%PX2](%BTABLE[x:522,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                        f"#pix[%PX3](%BTABLE[x:327,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                        f"#pix[%PX4](%BTABLE[x:377,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                        f"#pix[%PX5](%BTABLE[x:427,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                        f"#pix[%PX6](%BTABLE[x:477,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)"
                        f"#pix[%PX0](%BTABLE[x:317,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)"
                        f"#pix[%PX1](%BTABLE[x:572,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)"
                        f"#font(BG18,BG18,RG18)"
                        f"#ctxt[%TTEXT](%BTABLE[x:242,y:115-1,w:415,h:20],{{0}},\"ERROR\")"
                        f"#font(BC12,RC12,RC12)"
                        f"#ctxt[%MTEXT0](%BTABLE[x:242+20,y:115+22,w:415-40,h:20],{{}},\"Incorrect password!\")"
                        f"#exec(LW_vis&0&%MTEXT0)"
                        f"#ctxt[%MTEXT](%BTABLE[x:242+20,yc:225-3,w:415-40,h:%MTEXT0-115-159],{{}},\"Incorrect password!\")"
                        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)"
                        f"#font(WG14,BG14,WG14)"
                        f"#gpbtn[%PXBT](%BTABLE[x:520-433,y:303-16,w:100%,h:70],{{GW|open&cancel.dcml\\00|LW_lockall}},\"OK\")"
                        f"<NGDLG>"
                    )
            return (
                f"<NGDLG>"
                f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASSWD)"
                f"#ebox[%BF](x:0,y:0,w:100%,h:100%)"
                f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&cancel.dcml\\00|LW_lockall}},2,0,3,13,252,\"JOIN\",\"Connecting...\\Please, wait.\",26,\"Cancel\")"
                f"#exec(LW_gvar&%CG_GAMEID&{variables['id_room']}&%CG_MAXPL&{str(lobby.max_players)}&%CG_GAMENAME&{'namehere'}&%COMMAND&JGAME&%CG_IP&{lobby.ip}:{34000})"
                f"<NGDLG>"
            )
    return (
        f"<NGDLG>"
        f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASSWD)"
        f"#ebox[%BF](x:0,y:0,w:100%,h:100%)"
        f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&join_game.dcml\\00&id_room={variables['id_room']}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"You cannot join the room! This is an incorrect room. Press Cancel button to exit\",26,\"Try Again\",\"Cancel\")"
        f"<NGDLG>"
    )

# TODO: PLACEHOLDER
@alexander.route('join_pl_cmd.dcml')
def join_pl_cmd(variables: dict, player_id: str | int, **kwargs) -> str:
    if variables['VE_PLAYER'] == str(player_id):
        return (
            f"<NGDLG> "
            f"#ebox[%BF2](x:0,y:0,w:100%,h:100%) "
            f"#table[%TBL](%BF2[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&join_pl_cmd.dcml\\00&VE_PLAYER=136995\\00}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"You cannot join the room! This is an incorrect room. Press Cancel button to exit\",26,\"Try Again\",\"Cancel\")"
            f"<NGDLG>"
        )
    else:
        return ""


@alexander.route('log_conf_dlg.dcml')
def log_conf_dlg(variables: dict, **kwargs) -> str:
    return (
        f"#ebox[%EBG](x:0,y:0,w:1024,h:768)"
        f"#edit[%E_AC](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})"
        f"#edit[%E_CUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_CLANS_LAST_UPDATE}})"
        f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})"
        # f"#exec(LW_cfile&138186\\00&Cookies/%GV_VE_ACCOUNTS)"
        f"#def_dtbl_button_hotkey(13,0,27)#table[%TBL](%EBG[x:251,y:247,w:523,h:381],{{}}{{}}{{GW|open&log_user.dcml\\00&relogin=true^icon_last_update=<%GV_CLANS_LAST_UPDATE>^VE_MODE=creat^VE_PROF={variables['VE_PROF']}^VE_NAME={variables['VE_NAME']}^VE_NICK={variables['VE_NICK']}^VE_MAIL={variables['VE_NICK']}^VE_PASS={variables['VE_PASS']}^accounts={variables['VE_PROF']}^VE_GMID={variables['VE_GMID']}\\00|LW_lockall}}{{GW|open&log_new_form.dcml\\00&logs=1^VE_PROF={variables['VE_PROF']}^VE_MODE=edit^VE_NAME={variables['VE_NAME']}^VE_NICK={variables['VE_NICK']}^VE_MAIL={variables['VE_MAIL']}^VE_PASS={variables['VE_PASS']}^accounts={variables['VE_PROF']}^VE_ICQ={variables['VE_ICQ']}^VE_HOMP={variables['VE_HOMP']}^VE_SEX={variables['VE_SEX']}^VE_CNTRY={variables['VE_CNTRY']}^VE_PHON={variables['VE_PHON']}^VE_BIRTH={variables['VE_BIRTH']}\\00|LW_lockall}}{{LW_key&#CANCEL}},0,11,368,\"LOGIN CONFIRMATION\",,26,\"Login\",\"Edit Profile\",\"Cancel\")"
        f"#ebox[%LBX](x:270,y:230,w:500,h:220)"
        f"#pix[%PX1](%LBX[x:2,y:44,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)"
        f"#font(BC14,BC14,BC14)"
        f"#txt[%L_PROF](%LBX[x:4,y:85,w:100%,h:20],{{}},\"Profile ID#\")"
        f"#pan[%P_PROF](%LBX[x:157,y:85,w:318,h:14],1)"
        f"#txt[%E_PROF](%LBX[x:159,y:85,w:300,h:20],{{}},{variables['VE_PROF']})"
        f"#txt[%L_NAME](%LBX[x:4,y:115,w:100%,h:20],{{}},\"Full Name\")"
        f"#pan[%P_NAME](%LBX[x:157,y:115,w:318,h:14],1)"
        f"#txt[%E_NAME](%LBX[x:159,y:115,w:310,h:20],{{}},{variables['VE_NAME']})"
        f"#txt[%L_NICK](%LBX[x:4,y:145,w:100%,h:20],{{}},\"Nickname\")"
        f"#pan[%P_NICK](%LBX[x:157,y:145,w:318,h:14],1)"
        f"#txt[%E_NICK](%LBX[x:159,y:145,w:310,h:20],{{}},\"{variables['VE_NICK']}\") "
        f"#pix[%PX2](%LBX[x:4,y:167,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35) "
        f"#txt[%L_MAIL](%LBX[x:4,y:205,w:100%,h:20],{{}},\"E-Mail Address\")"
        f"#pan[%P_MAIL](%LBX[x:157,y:205,w:318,h:14],1) "
        f"#txt[%E_MAIL](%LBX[x:159,y:205,w:310,h:20],{{}},{variables['VE_MAIL']})"
        f"#txt[%L_PASS](%LBX[x:4,y:235,w:100%,h:20],{{}},\"User Password\")"
        f"#pan[%P_PASS](%LBX[x:157,y:235,w:318,h:14],1)"
        f"#txt[%E_PASS](%LBX[x:159,y:235,w:310,h:24],{{}},\"******************\") "
        f"#txt[%L_GMID](%LBX[x:4,y:265,w:100%,h:20],{{}},\"Game Box #ID\")"
        f"#pan[%P_GMID](%LBX[x:157,y:265,w:318,h:14],1)"
        f"#txt[%E_GMID](%LBX[x:159,y:265,w:310,h:20],{{}},\"****-****-****-****\")"
        f"#pix[%PX3](%LBX[x:4,y:287,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)"
        f"#font(BC14,WC14,BC14)"
        f"#sbtn[%T_CHANGE](%LBX[x:363,y:335,w:180,h:24],{{GW|open&change_account2.dcml\\00&accounts={variables['VE_PROF']}\\00|LW_lockall}},\"Old Profile\")"
        f"#hint(%T_CHANGE,\"Use old profile\")"
        f"#font(R2C12,BC12,BC12)"
        f"#txt[%L_ESRB](%LBX[x:0-10,y:351,w:100%,h:24],{{}},\"ESRB Notice: Game Experience May Change During Online Play\")"
        f"<MESDLG>"
        f"<MESDLG>"
        f"#block(l_games_btn.cml,CAN)"
        f"<MESDLG>"
        f"<MESDLG>"
        f"#end(CAN)"
        f"#hint(%L_NAME,\"Enter your name\")"
        f"#hint(%L_NICK,\"Enter your nickname\")"
        f"#hint(%L_MAIL,\"Enter your e-mail address\")"
        f"#hint(%L_PASS,\"Enter your password\")"
        f"#hint(%L_GMID,\"Enter your GameBox ID#\")"
        f"#hint(%Login,\"Join the server\")"
        f"#hint(%Edit Profile,\"Edit profile\")"
    )


@alexander.route('log_new_form.dcml')
def log_new_form(variables: dict, **kwargs) -> str:
    genders = []
    countries = []
    with alexander.engine.connect() as connection:

        cursor_out = connection.execute(text(f'select name from sexes')).fetchall()
        for row in cursor_out:
            genders.append(f'\"{row[0]}\"')
        genders = ",".join(genders)

        cursor_out = connection.execute(text(f'select name from countries')).fetchall()
        for row in cursor_out:
            countries.append(f'\"{row[0]}\"')
        countries = ",".join(countries)

    if variables['VE_MODE'] in (None, 'edit'):
        return (
            f"#ebox[%EBG](x:0,y:0,w:1024,h:768)"
            f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})"
            f"#block(cancel.cml,l_g):<!goback!>\\00"
            f"#end(l_g)"
            f"#def_dtbl_button_hotkey(13,0,27)"
            f"#table[%TBL](%EBG[x:251,y:247,w:523,h:381],{{}}{{}}{{GW|open&reg_new_user.dcml\\00&cansel=true^VE_PROF={variables['VE_PROF']}^VE_MODE=edit^VE_NAME=<%GV_VE_NAME>^VE_NICK=<%GV_VE_NICK>^VE_MAIL=<%GV_VE_MAIL>^VE_GMID=<%GV_VE_GMID>^VE_PASS=<%GV_VE_PASS>^VE_RASS=<%GV_VE_RASS>^VE_ICQ=<%GV_VE_ICQ>^VE_HOMP=<%GV_VE_HOMP>^VE_SEX=<%GV_VE_SEX>^VE_CNTRY=<%GV_VE_CNTRY>^VE_PHON=<%GV_VE_PHON>^VE_BIRTH=<%GV_VE_BIRTH>^accounts={variables['accounts']}\\00|LW_lockall}}{{GW|open&log_new_form.dcml\\00&logs=1^cansel=true^VE_MODE=creat^accounts={variables['accounts']}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},0,11,368,EDIT PERSONAL PROFILE,,26,Update,\"New account\",\"Cancel\")"
            f"#ebox[%LBX](x:270,y:210,w:500,h:220)"
            f"#font(BC14,RC14,RC14))"
            f"#txt[%L_NAME](%LBX[x:4,y:56,w:100%,h:20],{{}},\"Full Name\")"
            f"#pan[%P_NAME](%LBX[x:159,y:56,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_NAME']}\\00&Cookies/%GV_VE_NAME)"
            f"#edit[%E_NAME](%LBX[x:164,y:53,w:302,h:18],{{%GV_VE_NAME}},0,0,0,1)"
            f"#txt[%L_NICK](%LBX[x:4,y:84,w:100%,h:20],{{}},\"Nickname\")"
            f"#pan[%P_NICK](%LBX[x:159,y:84,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_NICK']}\\00&Cookies/%GV_VE_NICK)"
            f"#edit[%E_NICK](%LBX[x:164,y:81,w:302,h:18],{{%GV_VE_NICK}})"
            f"#txt[%L_MAIL](%LBX[x:4,y:112,w:100%,h:20],{{}},\"E-Mail Address\")"
            f"#pan[%P_MAIL](%LBX[x:159,y:112,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_MAIL']}\\00&Cookies/%GV_VE_MAIL)"
            f"#edit[%E_MAIL](%LBX[x:164,y:109,w:302,h:18],{{%GV_VE_MAIL}})"
            f"#txt[%L_GMID](%LBX[x:4,y:140,w:100%,h:20],{{}},\"Game Box #ID\")"
            f"#pan[%P_GMID](%LBX[x:159,y:140,w:317,h:14],1)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_GMID)"
            f"#edit[%E_GMID](%LBX[x:164,y:137,w:302,h:18],{{%GV_VE_GMID}},0,0,1)"
            f"#txt[%L_PASS](%LBX[x:4,y:168,w:100%,h:20],{{}},\"User Password\")"
            f"#pan[%P_PASS](%LBX[x:159,y:168,w:317,h:14],1)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASS)"
            f"#edit[%E_PASS](%LBX[x:164,y:165,w:302,h:18],{{%GV_VE_PASS}},0,0,1)"
            f"#txt[%L_RASS](%LBX[x:4,y:196,w:100%,h:20],{{}},\"Change password to\")"
            f"#pan[%P_RASS](%LBX[x:159,y:196,w:317,h:14],1)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_RASS)"
            f"#edit[%E_RASS](%LBX[x:164,y:193,w:302,h:18],{{%GV_VE_RASS}},0,0,1)"
            f"#txt[%L_ICQ](%LBX[x:4,y:224,w:100%,h:20],{{}},\"ICQ #ID\")"
            f"#pan[%P_ICQ](%LBX[x:159,y:224,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_ICQ']}\\00&Cookies/%GV_VE_ICQ)"
            f"#edit[%E_ICQ](%LBX[x:164,y:221,w:302,h:18],{{%GV_VE_ICQ}})"
            f"#txt[%L_HOMP](%LBX[x:4,y:252,w:100%,h:20],{{}},\"Internet Homepage\")"
            f"#pan[%P_HOMP](%LBX[x:159,y:252,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_HOMP']}\\00&Cookies/%GV_VE_HOMP)"
            f"#edit[%E_HOMP](%LBX[x:164,y:249,w:302,h:18],{{%GV_VE_HOMP}})"
            f"#txt[%L_SEX](%LBX[x:4,y:280,w:100%,h:20],{{}},\"Gender\")"
            f"#exec(LW_cfile&{int(variables['VE_SEX'])}\\00&Cookies/%GV_VE_SEX)"
            f"#cbb[%E_SEX](%LBX[x:153,y:273,w:329,h:18],{{%GV_VE_SEX}},{genders},0)"
            f"#txt[%L_CNTRY](%LBX[x:4,y:308,w:100%,h:20],{{}},\"Country\")"
            f"#exec(LW_cfile&{int(variables['VE_CNTRY'])}\\00&Cookies/%GV_VE_CNTRY)"
            f"#cbb[%E_CNTRY](%LBX[x:153,y:301,w:329,h:18],{{%GV_VE_CNTRY}},{countries},0)"
            f"#txt[%L_PHON](%LBX[x:4,y:336,w:100%,h:20],{{}},\"Home Phone\")"
            f"#pan[%P_PHON](%LBX[x:159,y:336,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_PHON']}\\00&Cookies/%GV_VE_PHON)"
            f"#edit[%E_PHON](%LBX[x:164,y:333,w:302,h:18],{{%GV_VE_PHON}})"
            f"#txt[%L_BIRTH](%LBX[x:4,y:364,w:100%,h:20],{{}},\"Birthday (D/M/Y)\")"
            f"#pan[%P_BIRTH](%LBX[x:159,y:364,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_BIRTH']}\\00&Cookies/%GV_VE_BIRTH)"
            f"#edit[%E_BIRTH](%LBX[x:164,y:361,w:302,h:18],{{%GV_VE_BIRTH}})"
            f"<MESDLG>"
            f"<MESDLG>"
            f"#block(l_games_btn.cml,CAN)"
            f"<MESDLG>"
            f"<MESDLG>"
            f"#end(CAN)"
            f"#hint(%L_NAME,\"Enter your name\")"
            f"#hint(%L_NICK,\"Enter your nickname\")"
            f"#hint(%L_MAIL,\"Enter your e-mail address\")"
            f"#hint(%L_PASS,\"Enter your password\")"
            f"#hint(%L_RASS,\"Change password to\")"
            f"#hint(%L_GMID,\"Enter your GameBox ID#\")"
            f"#hint(%L_ICQ,\"Enter your ICQ number\")"
            f"#hint(%L_HOMP,\"Enter your homepage\")"
            f"#hint(%L_SEX,\"Select your sex\")"
            f"#hint(%L_CNTRY,\"Select country\")"
            f"#hint(%L_PHON,\"Enter your home phone number\")"
            f"#hint(%L_BIRTH,\"Enter your birth date (DD/MM/YYYY)\")"
            f"#hint(%New account,\"Create a new account\")"
        )

    elif variables['VE_MODE'] == "creat":
        return (
            f"#ebox[%EBG](x:0,y:0,w:1024,h:768)"
            f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})"
            f"#def_dtbl_button_hotkey(13,0,27)"
            f"#table[%TBL](%EBG[x:251,y:247,w:523,h:381],{{}}{{}}{{GW|open&reg_new_user.dcml\\00&cansel=^VE_PROF=^VE_MODE=creat^VE_NAME=<%GV_VE_NAME>^VE_NICK=<%GV_VE_NICK>^VE_MAIL=<%GV_VE_MAIL>^VE_GMID=<%GV_VE_GMID>^VE_PASS=<%GV_VE_PASS>^VE_RASS=<%GV_VE_RASS>^VE_ICQ=<%GV_VE_ICQ>^VE_HOMP=<%GV_VE_HOMP>^VE_SEX=<%GV_VE_SEX>^VE_CNTRY=<%GV_VE_CNTRY>^VE_PHON=<%GV_VE_PHON>^VE_BIRTH=<%GV_VE_BIRTH>^accounts=\\00|LW_lockall}}{{GW|open&change_account2.dcml\\00&cansel=^accounts=\\00|LW_lockall}}{{LW_key&#CANCEL}},0,11,368,CREATE PERSONAL PROFILE,,26,Register,Old Profile,\"Cancel\")"
            f"#ebox[%LBX](x:270,y:210,w:500,h:220)"
            f"#font(BC14,RC14,RC14))"
            f"#txt[%L_NAME](%LBX[x:4,y:56,w:100%,h:20],{{}},\"Full Name\")"
            f"#pan[%P_NAME](%LBX[x:159,y:56,w:317,h:14],1)"
            f"#exec(LW_cfile{variables['VE_NAME']}&\\00&Cookies/%GV_VE_NAME)"
            f"#edit[%E_NAME](%LBX[x:164,y:53,w:302,h:18],{{%GV_VE_NAME}},0,0,0,1)"
            f"#txt[%L_NICK](%LBX[x:4,y:84,w:100%,h:20],{{}},\"Nickname\")"
            f"#pan[%P_NICK](%LBX[x:159,y:84,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_NICK']}\\00&Cookies/%GV_VE_NICK)"
            f"#edit[%E_NICK](%LBX[x:164,y:81,w:302,h:18],{{%GV_VE_NICK}})"
            f"#txt[%L_MAIL](%LBX[x:4,y:112,w:100%,h:20],{{}},\"E-Mail Address\")"
            f"#pan[%P_MAIL](%LBX[x:159,y:112,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_MAIL']}\\00&Cookies/%GV_VE_MAIL)"
            f"#edit[%E_MAIL](%LBX[x:164,y:109,w:302,h:18],{{%GV_VE_MAIL}})"
            f"#txt[%L_GMID](%LBX[x:4,y:140,w:100%,h:20],{{}},\"Game Box #ID\")"
            f"#pan[%P_GMID](%LBX[x:159,y:140,w:317,h:14],1)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_GMID)"
            f"#edit[%E_GMID](%LBX[x:164,y:137,w:302,h:18],{{%GV_VE_GMID}},0,0,1)"
            f"#txt[%L_PASS](%LBX[x:4,y:168,w:100%,h:20],{{}},\"User Password\")"
            f"#pan[%P_PASS](%LBX[x:159,y:168,w:317,h:14],1)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASS)"
            f"#edit[%E_PASS](%LBX[x:164,y:165,w:302,h:18],{{%GV_VE_PASS}},0,0,1)"
            f"#txt[%L_RASS](%LBX[x:4,y:196,w:100%,h:20],{{}},\"Retype Password\")"
            f"#pan[%P_RASS](%LBX[x:159,y:196,w:317,h:14],1)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_RASS)"
            f"#edit[%E_RASS](%LBX[x:164,y:193,w:302,h:18],{{%GV_VE_RASS}},0,0,1)"
            f"#txt[%L_ICQ](%LBX[x:4,y:224,w:100%,h:20],{{}},\"ICQ #ID\")"
            f"#pan[%P_ICQ](%LBX[x:159,y:224,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_ICQ']}\\00&Cookies/%GV_VE_ICQ)"
            f"#edit[%E_ICQ](%LBX[x:164,y:221,w:302,h:18],{{%GV_VE_ICQ}})"
            f"#txt[%L_HOMP](%LBX[x:4,y:252,w:100%,h:20],{{}},\"Internet Homepage\")"
            f"#pan[%P_HOMP](%LBX[x:159,y:252,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_HOMP']}\\00&Cookies/%GV_VE_HOMP)"
            f"#edit[%E_HOMP](%LBX[x:164,y:249,w:302,h:18],{{%GV_VE_HOMP}})"
            f"#txt[%L_SEX](%LBX[x:4,y:280,w:100%,h:20],{{}},\"Gender\")"
            f"#exec(LW_cfile&{variables['VE_SEX']}\\00&Cookies/%GV_VE_SEX)"
            f"#cbb[%E_SEX](%LBX[x:153,y:273,w:329,h:18],{{%GV_VE_SEX}},{genders},0)"
            f"#txt[%L_CNTRY](%LBX[x:4,y:308,w:100%,h:20],{{}},\"Country\")"
            f"#exec(LW_cfile&{variables['VE_CNTRY']}\\00&Cookies/%GV_VE_CNTRY)"
            f"#cbb[%E_CNTRY](%LBX[x:153,y:301,w:329,h:18],{{%GV_VE_CNTRY}},{countries},0)"
            f"#txt[%L_PHON](%LBX[x:4,y:336,w:100%,h:20],{{}},\"Home Phone\")"
            f"#pan[%P_PHON](%LBX[x:159,y:336,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_PHON']}\\00&Cookies/%GV_VE_PHON)"
            f"#edit[%E_PHON](%LBX[x:164,y:333,w:302,h:18],{{%GV_VE_PHON}})"
            f"#txt[%L_BIRTH](%LBX[x:4,y:364,w:100%,h:20],{{}},\"Birthday (D/M/Y)\")"
            f"#pan[%P_BIRTH](%LBX[x:159,y:364,w:317,h:14],1)"
            f"#exec(LW_cfile&{variables['VE_BIRTH']}\\00&Cookies/%GV_VE_BIRTH)"
            f"#edit[%E_BIRTH](%LBX[x:164,y:361,w:302,h:18],{{%GV_VE_BIRTH}})"
            f"<MESDLG>"
            f"<MESDLG>"
            f"#block(l_games_btn.cml,CAN)"
            f"<MESDLG>"
            f"<MESDLG>"
            f"#end(CAN)"
            f"#hint(%L_NAME,\"Enter your name\")"
            f"#hint(%L_NICK,\"Enter your nickname\")"
            f"#hint(%L_MAIL,\"Enter your e-mail address\")"
            f"#hint(%L_PASS,\"Enter your password\")"
            f"#hint(%L_RASS,\"Enter your password\")"
            f"#hint(%L_GMID,\"Enter your GameBox ID#\")"
            f"#hint(%L_ICQ,\"Enter your ICQ number\")"
            f"#hint(%L_HOMP,\"Enter your homepage\")"
            f"#hint(%L_SEX,\"Select your sex\")"
            f"#hint(%L_CNTRY,\"Select country\")"
            f"#hint(%L_PHON,\"Enter your home phone number\")"
            f"#hint(%L_BIRTH,\"Enter your birth date (DD/MM/YYYY)\")"
            f"#hint(%New account,\"Create a new account\")"
        )
    return ""

@alexander.route('log_user.dcml')
def log_user(variables: dict, **kwargs) -> str | None:
    try:
        with alexander.engine.connect() as connection:
            if variables['relogin'] == "true":
                profile = connection.execute(
                    text(f"CALL relogin(\'{variables['VE_NICK']}\',\'{variables['VE_PASS']}\')")).fetchone()
            else:
                profile = connection.execute(text(
                    f"CALL login(\'{variables['VE_NICK']}\',\'{variables['VE_PASS']}\', \'{variables['VE_GMID']}\')")).fetchone()
            connection.commit()
            if profile:
                profile = profile._mapping
                return (
                    f"<MESDLG> "
                    f"#ebox[%MBG](x:0,y:0,w:1024,h:768)"
                    f"#pix[%PX1](%MBG[x:0,y:0,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)" +
                    (f"#exec(LW_cfile&{profile['session_key']}&lgdta.log)" if variables['save_pass'] == '1' else '') +
                    # f"#exec(LW_cfile&{profile['session_key']}&Cookies/%GV_SESSION_KEY)"
                    f"#exec(LW_key&{profile['player_id']})"
                    f"#exec(LW_gvar&"
                    f"%PROF&{profile['player_id']}&"
                    f"%NAME&{profile['nick']}&"
                    f"%NICK&{profile['nick']}&"
                    f"%MAIL&{profile['mail']}&"
                    f"%PASS&{variables['VE_PASS']}&"
                    f"%GMID&{variables['VE_GMID']}&"
                    f"%CHAT&{alexander.irc.address}&"
                    f"%CHNL1&{alexander.irc.ch1}\\00&"
                    f"%CHNL2&{alexander.irc.ch2}\\00)"
                    f"<MESDLG> ")
    except DBAPIError as err:
            if err.orig: 
                return (
                    f"<MESDLG> "
                    f"#ebox[%MBG](x:0,y:0,w:1024,h:768) "
                    f"#def_dtbl_button_hotkey(13,27) "
                    f"#table[%TBL](%MBG[x:287,y:285,w:450,h:200],{{}}{{}}{{LW_file&Internet/Cash/l_games_btn.cml}}{{LW_file&Internet/Cash/l_games_btn.cml}},1,0,11,362,\"ERROR\",\"{mysql_error_messages[err.orig.args[1]]}\",24,\"Edit\",\"Cancel\") "
                    f"<MESDLG> "
                )


@alexander.route('mail_list.dcml')
def mail_list(variables: dict, player_id, **kwargs) -> str | None:
    panel_list = []
    message_list = []
    with alexander.engine.connect() as connection:
        if variables['delete']:
            sender = connection.execute(text(
                f"SELECT id_from, id_to "
                f"FROM mail_messages "
                f"WHERE mail_messages.id = {variables['messageID']}"
            )).fetchone()
            if sender:
                sender = sender._mapping
                connection.execute(text(
                    f"UPDATE mail_messages "
                    f"SET {'removed_by_sender' if sender['id_from'] == int(player_id) else 'removed_by_recipient'} = 1 "
                    f"{',removed_by_recipient = 1' if sender['id_from'] == sender['id_to'] else ''} "
                    f"WHERE id = {variables['messageID']}"
                ))
                connection.commit()
        summary = connection.execute(text(
            f"CALL mail_stats({player_id}) "
        )).fetchone()
        if summary:
            summary = summary._mapping
            if variables['sent'] == 'true':
                mode = "1"
            elif variables['readable'] == '2':
                mode = "2"
            elif variables['readable'] == '3':
                mode = "3"
            else:
                mode = "4"
            messages = connection.execute(text(f"CALL get_mail({mode}, {player_id}) ")).fetchall()
            for idx, entry in enumerate(messages):
                message = entry._mapping
                highlight = "{" if message.status == 1 else ""
                panel_list.append(
                    f"#apan[%APAN{idx}](%SB[x:0,y:{21 * idx}-2,w:100%,h:20],{{GW|open&mail_view.dcml\\00&messageID={message.id}^readable={variables['readable']}^sent={variables['sent']}\\00|LW_lockall}},8)"
                )
                message_list.append(
                    f",21,\"{message.nick}\",\"{highlight}{message.subject}\",\"{message.sent_at}\""
                )
            panel_list = "".join(panel_list)
            message_list = "".join(message_list)
            selection = 0
            if variables['sent'] == 'true':
                selection = 1
            elif variables['readable'] == '2':
                selection = 2
            elif variables['readable'] == '3':
                selection = 3
            return (
                f"#ebox[%TB](x:0,y:0,w:100%,h:100%) "
                f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12) "
                f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13) "
                f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10) "
                f"#font(RG18,RG18,RG18) "
                f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
                f"#font(BG18,BG18,BG18) "
                f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\") "
                f"#font(R2C12,R2C12,R2C12) "
                f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\") "
                f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
                f"#font(RC12,R2C12,RC12) "
                f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
                f"#hint(%BT1,\"News, events, forum and punishment list\")"
                f"#font(RC12,RC12,RC12) "
                f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1) "
                f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},\"Player List\")"
                f"#hint(%BT2,\"Player list, personal mail and clan information\")"
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                f"#font(RC12,R2C12,RC12) "
                f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
                f"#hint(%BT4,\"Play custom games\")"
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                f"#font(RC12,R2C12,RC12) "
                f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
                f"#hint(%BT5,\"Played games and their scores\")"
                f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103) "
                f"<VOTING> "
                f"#exec(GW|open&voting.dcml\\00&question=46\\00) "
                f"<VOTING> "
                f"<MAILBUTTONS> "
                f"#ebox[%MB](x:0,y:0,w:100%,h:100%) "
                f"#font(RC14,GC14,RC14) "
                f"#ctxt[%LIST1](%MB[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\") "
                f"#hint(%LIST1,\"Player list, personal mail and clan information\") "
                f"#font(RC12,GC12,RC12) "
                f"#ctxt[%LIST2](%MB[x:0,y:%LIST1-10,w:146,h:24],{{GW|open&mail_list.dcml\\00|LW_lockall}},\"{{Mail}}\") "
                f"#hint(%LIST2,\"Manage your personal mail\") "
                f"#font(R2C14,R2C14,RC14) "
                f"#ctxt[%LIST3](%MB[x:0,y:%LIST2+7,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\") "
                f"#hint(%LIST3,\"Clans, their members and details\") "
                f"#ebox[%B1](x:154,y:40,w:559,h:45) "
                f"#pan[%P1](%B1[x:0,y:0,w:100%,h:100%],7) "
                f"#font({'G' if selection == 0 else 'B'}C12,BC12,GC12)"
                f"#txt[%TITRE1](%B1[x:4,y:0+8,w:150,h:20],{{}},\"Mail Inbox total: {summary.messages_total}\")"
                f"#apan[%APAN0](%B1[x:4,y:%TITRE1-18,x1:%TITRE1,h:16],{{GW|open&mail_list.dcml\\00|LW_lockall}},15)"
                f"#font({'G' if selection == 1 else 'B'}C12,BC12,GC12)"
                f"#txt[%TITRE2](%B1[x:4,y:18+8,w:150,h:20],{{}},\"Sent: {summary.messages_sent}\")"
                f"#apan[%APAN1](%B1[x:4,y:%TITRE2-18,x1:%TITRE2,h:16],{{GW|open&mail_list.dcml\\00&sent=true\\00|LW_lockall}},15)"
                f"#font({'G' if selection == 2 else 'B'}C12,BC12,GC12)"
                f"#txt[%TITRE3](%B1[x:292,y:0+8,w:150,h:20],{{}},\"Unread: {summary.messages_unread}\")"
                f"#apan[%APAN2](%B1[x:292,y:%TITRE3-18,x1:%TITRE3,h:16],{{GW|open&mail_list.dcml\\00&readable=2\\00|LW_lockall}},15)"
                f"#font({'G' if selection == 3 else 'B'}C12,BC12,GC12)"
                f"#txt[%TITRE4](%B1[x:292,y:18+8,w:150,h:20],{{}},\"Read: {summary.messages_read}\")"
                f"#apan[%APAN3](%B1[x:292,y:%TITRE4-18,x1:%TITRE4,h:16],{{GW|open&mail_list.dcml\\00&readable=3\\00|LW_lockall}},15)"
                f"#pan[%P2](%B1[x:314,y:0-34,w:0,h:100%+68],10) "
                f"<MAILBUTTONS>"
                f"#ebox[%B](x:0,y:0,w:100%,h:100%) "
                f"#ebox[%LB](x:0,y:0,w:100%,h:100%) "
                f"#font(R2C12,R2C12,RC12) "
                f"#stbl[%TIT_TBL](%LB[x:154,y:95,w:523,h:238],{{GW|open&mail_list.dcml\\00&sent=^order=nick^resort=1^readable=\\00|LW_lockall}}{{GW|open&mail_list.dcml\\00&sent=^order=subject^resort=1^readable=\\00|LW_lockall}}{{GW|open&mail_list.dcml\\00&sent=^order=m.send^resort=1^readable=\\00|LW_lockall}},3,7,20,1,40,1,40,1,18,\"{{From\",\"{{Subject\",\"{{Date\") "
                f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-21,27) "
                f"#sbox[%SB](x:150,y:114,w:526+4,h:216) "
                f"{panel_list}"
                f"#font(BC12,RC12,BC12) "
                f"#stbl[%MESS](%SB[x:4,y:0,w:523,h:100%],{{}},3,0,20,1,40,1,40,1{message_list})"
                f"#font(BC14,WC14,BC14) "
                f"#sbtn[%BTXT1](%B[x:641,y:377,w:100,h:305],{{GW|open&mail_new.dcml\\00|LW_lockall}},\"New Mail\") "
                f"<NGDLG> "
                f"<NGDLG> "
                f"#block(cancel.cml,CAN)<NGDLG> "
                f"<NGDLG> "
                f"#end(CAN)"
            )


@alexander.route('mail_new.dcml')
def mail_new(variables: dict, player_id, **kwargs) -> str | None:
    with alexander.engine.connect() as connection:
        summary = connection.execute(text(
            f"CALL mail_stats({player_id}) "
        )).fetchone()
        if summary:
            summary = summary._mapping
            if variables['send']:
                id = connection.execute(text(
                    f"CALL get_player_id_by_nick(\"{variables['send_to']}\")"
                )).fetchone()
                if id:
                    connection.execute(text(
                        "INSERT INTO mail_messages ("
                        "id_from, id_to, subject, content "
                        ") "
                        "VALUES "
                        "( "
                        f"{player_id}, {id._mapping.id}, \"{variables['subject']}\", \"{variables['message']}\""
                        ")"
                    ))
                    connection.commit()
                    return f"#exec(GW|open&mail_list.dcml\\00&sent=true\\00|LW_lockall)"
                else:
                    return (
                        f"<NGDLG>"
                        f"#ebox[%BF](x:0,y:0,w:100%,h:100%)"
                        f"#table[%TBL](%BF[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&mail_new.dcml\\00&subject={variables['subject']}^message={variables['message']}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"The user with the provided nickname does not exist.\",26,\"OK\")"
                        f"<NGDLG>"
                    )
            not_found = False
            return " ".join((
                f"#block(l_games_btn.cml,l_g):<!goback!>\\00",
                f"#end(l_g) ",
                f"#ebox[%TB](x:0,y:0,w:100%,h:100%) ",
                f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12) ",
                f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13) ",
                f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10) ",
                f"#font(RG18,RG18,RG18) ",
                f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")",
                f"#font(BG18,BG18,BG18) ",
                f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\") ",
                f"#font(R2C12,R2C12,R2C12) ",
                f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\") ",
                f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)      ",
                f"#font(RC12,R2C12,RC12) ",
                f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")",
                f"#hint(%BT1,\"News, events, forum and punishment list\")      ",
                f"#font(RC12,RC12,RC12) ",
                f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1) ",
                f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},\"Player List\")",
                f"#hint(%BT2,\"Player list, personal mail and clan information\")",
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)      ",
                f"#font(RC12,R2C12,RC12) ",
                f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")",
                f"#hint(%BT4,\"Play custom games\")",
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)      ",
                f"#font(RC12,R2C12,RC12) ",
                f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
                f"#hint(%BT5,\"Played games and their scores\")     ",
                f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103) ",
                f"<VOTING> ",
                f"#exec(GW|open&voting.dcml\\00&question=46\\00) ",
                f"<VOTING> ",
                f"<MAILBUTTONS> ",
                f"#ebox[%MB](x:0,y:0,w:100%,h:100%) ",
                f"#font(RC14,GC14,RC14) ",
                f"#ctxt[%LIST1](%MB[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\") ",
                f"#hint(%LIST1,\"Player list, personal mail and clan information\") ",
                f"#font(RC12,GC12,RC12) ",
                f"#ctxt[%LIST2](%MB[x:0,y:%LIST1-10,w:146,h:24],{{GW|open&mail_list.dcml\\00|LW_lockall}},\"{{Mail}}\") ",
                f"#hint(%LIST2,\"Manage your personal mail\") ",
                f"#font(R2C14,R2C14,RC14) ",
                f"#ctxt[%LIST3](%MB[x:0,y:%LIST2+7,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\") ",
                f"#hint(%LIST3,\"Clans, their members and details\") ",
                f"#ebox[%B1](x:154,y:40,w:559,h:45) ",
                f"#pan[%P1](%B1[x:0,y:0,w:100%,h:100%],7) ",
                f"#font(BC12,BC12,GC12)"
                f"#txt[%TITRE1](%B1[x:4,y:0+8,w:150,h:20],{{}},\"Mail Inbox total: {summary.messages_total}\")"
                f"#apan[%APAN0](%B1[x:4,y:%TITRE1-18,x1:%TITRE1,h:16],{{GW|open&mail_list.dcml\\00|LW_lockall}},15)"
                f"#font(BC12,BC12,GC12)"
                f"#txt[%TITRE2](%B1[x:4,y:18+8,w:150,h:20],{{}},\"Sent: {summary.messages_sent}\")"
                f"#apan[%APAN1](%B1[x:4,y:%TITRE2-18,x1:%TITRE2,h:16],{{GW|open&mail_list.dcml\\00&sent=true\\00|LW_lockall}},15)"
                f"#font(BC12,BC12,GC12)"
                f"#txt[%TITRE3](%B1[x:292,y:0+8,w:150,h:20],{{}},\"Unread: {summary.messages_unread}\")"
                f"#apan[%APAN2](%B1[x:292,y:%TITRE3-18,x1:%TITRE3,h:16],{{GW|open&mail_list.dcml\\00&readable=2\\00|LW_lockall}},15)"
                f"#font(BC12,BC12,GC12)"
                f"#txt[%TITRE4](%B1[x:292,y:18+8,w:150,h:20],{{}},\"Read: {summary.messages_read}\")"
                f"#apan[%APAN3](%B1[x:292,y:%TITRE4-18,x1:%TITRE4,h:16],{{GW|open&mail_list.dcml\\00&readable=3\\00|LW_lockall}},15)"
                f"#pan[%P2](%B1[x:314,y:0-34,w:0,h:100%+68],10) ",
                f"<MAILBUTTONS>",
                f"#ebox[%B](x:0,y:0,w:100%,h:100%) ",
                f"#exec(LW_cfile&\\00&Cookies/%GV_SEND_TO) " if not variables[
                    'send_to'] else f"#exec(LW_cfile&{variables['send_to']}\\00&Cookies/%GV_SEND_TO) ",
                f"#exec(LW_cfile&{variables['subject'] if variables['subject'] else ''}\\00&Cookies/%GV_SUBJECT) ",
                f"#exec(LW_cfile&{variables['message'] if variables['message'] else ''}\\00&Cookies/%GV_TEXT) ",
                f"#ebox[%B0](x:154,y:95,w:559,h:238) ",
                f"#pan[%P1](%B0[x:0,y:0,w:100%,h:100%],5) ",
                f"#font(R2C12,RC12,RC12) ",
                f"#txt[%T1](%B0[x:4,y:8,w:100,h:20],{{}},\"Send to:\") ",
                f"#font(BC12,RC12,RC12) ",
                f"#pan[%P2](%B0[x:8,y:27,w:543,h:14],1) ",
                f"#edit[%E1](%B0[x:14,y:26,w:538,h:18],{{%GV_SEND_TO}},0,0,0,1) ",
                f"#font(R2C12,RC12,RC12) ",
                f"#txt[%T2](%B0[x:4,y:53,w:100,h:20],{{}},\"Subject:\") ",
                f"#pan[%P3](%B0[x:8,y:72,w:543,h:14],1) ",
                f"#font(BC12,RC12,RC12) ",
                f"#edit[%E2](%B0[x:13,y:71,w:538,h:18],{{%GV_SUBJECT}}) ",
                f"#font(R2C12,RC12,RC12) ",
                f"#txt[%T3](%B0[x:4,y:98,w:100,h:20],{{}},\"Text:\") ",
                f"#pan[%P4](%B0[x:8,y:117,w:543,h:111],1) ",
                f"#font(BC12,RC12,RC12) ",
                f"#edit[%E3](%B0[x:13,y:117,w:534,h:111],{{%GV_TEXT}},1) ",
                f"#font(BC14,WC14,BC14) ",
                f"#sbtn[%Send](%B[x:521,y:377,w:100,h:305],{{GW|open&mail_new.dcml\\00&cansel=true^send=1^send_to=<%GV_SEND_TO>^subject=<%GV_SUBJECT>^message=<%GV_TEXT>\\00|LW_lockall}},\"Send\") ",
                f"#sbtn[%Back](%B[x:641,y:377,w:100,h:305],{{LW_file&Internet/Cash/l_games_btn.cml}},\"Cancel\") ",
                f"<NGDLG> ",
                f"#ebox[%L0](x:0,y:0,w:100%,h:100%)\
                #table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"NOTICE\",\" Players with nicknames \'\'c\'\' not found! \",0,\"OK\")" if not_found else "",
                f"<NGDLG> ",
                f"#block(cancel.cml,CAN)<NGDLG> ",
                f"<NGDLG> ",
                f"#end(CAN)",
            ))


@alexander.route('mail_view.dcml')
def mail_view(variables: dict, player_id, **kwargs) -> str | None:
    with alexander.engine.connect() as connection:
        summary = connection.execute(text(
            f"CALL mail_stats({player_id}) "
        )).fetchone()
        if summary:
            summary = summary._mapping
            message = connection.execute(text(
                f"SELECT "
                f"subject "
                f"content, "
                f"id_from, "
                f"sent_at, "
                f"subject, "
                f"player_id, "
                f"status, "
                f"CONCAT(COALESCE(clans.signature,''), players.nick) AS name "
                f"FROM mail_messages "
                f"INNER JOIN players ON players.player_id = id_to "
                f"LEFT JOIN clans ON clan_id = clans.id "
                f"WHERE mail_messages.id = {variables['messageID']} "
            )).fetchone()
            if message:
                message = message._mapping
                if message['status'] == 1:
                    connection.execute(text(
                        f"UPDATE mail_messages "
                        f"SET status = 2 "
                        f"WHERE id = {variables['messageID']}"
                    ))
                    connection.commit()
                return (
                    f"#ebox[%TB](x:0,y:0,w:100%,h:100%) "
                    f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12) "
                    f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13) "
                    f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10) "
                    f"#font(RG18,RG18,RG18) "
                    f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
                    f"#font(BG18,BG18,BG18) "
                    f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\") "
                    f"#font(R2C12,R2C12,R2C12) "
                    f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\") "
                    f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
                    f"#font(RC12,R2C12,RC12) "
                    f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
                    f"#hint(%BT1,\"News, events, forum and punishment list\")"
                    f"#font(RC12,RC12,RC12) "
                    f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1) "
                    f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},\"Player List\")"
                    f"#hint(%BT2,\"Player list, personal mail and clan information\")"
                    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)     "
                    f"#font(RC12,R2C12,RC12) "
                    f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
                    f"#hint(%BT4,\"Play custom games\")"
                    f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                    f"#font(RC12,R2C12,RC12) "
                    f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
                    f"#hint(%BT5,\"Played games and their scores\")"
                    f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103) "
                    f"<VOTING> "
                    f"#exec(GW|open&voting.dcml\\00&question=46\\00) "
                    f"<VOTING> "
                    f"<MAILBUTTONS> "
                    f"#ebox[%MB](x:0,y:0,w:100%,h:100%) "
                    f"#font(RC14,GC14,RC14) "
                    f"#ctxt[%LIST1](%MB[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\") "
                    f"#hint(%LIST1,\"Player list, personal mail and clan information\") "
                    f"#font(RC12,GC12,RC12) "
                    f"#ctxt[%LIST2](%MB[x:0,y:%LIST1-10,w:146,h:24],{{GW|open&mail_list.dcml\\00|LW_lockall}},\"{{Mail}}\") "
                    f"#hint(%LIST2,\"Manage your personal mail\") "
                    f"#font(R2C14,R2C14,RC14) "
                    f"#ctxt[%LIST3](%MB[x:0,y:%LIST2+7,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\") "
                    f"#hint(%LIST3,\"Clans, their members and details\") "
                    f"#ebox[%B1](x:154,y:40,w:559,h:45) "
                    f"#pan[%P1](%B1[x:0,y:0,w:100%,h:100%],7) "
                    f"#font(BC12,BC12,GC12)"
                    f"#txt[%TITRE1](%B1[x:4,y:0+8,w:150,h:20],{{}},\"Mail Inbox total: {summary.messages_total}\")"
                    f"#apan[%APAN0](%B1[x:4,y:%TITRE1-18,x1:%TITRE1,h:16],{{GW|open&mail_list.dcml\\00|LW_lockall}},15)"
                    f"#font(BC12,BC12,GC12)"
                    f"#txt[%TITRE2](%B1[x:4,y:18+8,w:150,h:20],{{}},\"Sent: {summary.messages_sent}\")"
                    f"#apan[%APAN1](%B1[x:4,y:%TITRE2-18,x1:%TITRE2,h:16],{{GW|open&mail_list.dcml\\00&sent=true\\00|LW_lockall}},15)"
                    f"#font(BC12,BC12,GC12)"
                    f"#txt[%TITRE3](%B1[x:292,y:0+8,w:150,h:20],{{}},\"Unread: {summary.messages_unread}\")"
                    f"#apan[%APAN2](%B1[x:292,y:%TITRE3-18,x1:%TITRE3,h:16],{{GW|open&mail_list.dcml\\00&readable=2\\00|LW_lockall}},15)"
                    f"#font(BC12,BC12,GC12)"
                    f"#txt[%TITRE4](%B1[x:292,y:18+8,w:150,h:20],{{}},\"Read: {summary.messages_read}\")"
                    f"#apan[%APAN3](%B1[x:292,y:%TITRE4-18,x1:%TITRE4,h:16],{{GW|open&mail_list.dcml\\00&readable=3\\00|LW_lockall}},15)"
                    f"#pan[%P2](%B1[x:314,y:0-34,w:0,h:100%+68],10) "
                    f"<MAILBUTTONS>"
                    f"#ebox[%B](x:0,y:0,w:100%,h:100%) "
                    f"#ebox[%B2](x:154,y:95,w:559,h:238) "
                    f"#pan[%P1](%B2[x:0,y:0,w:100%,h:100%],7) "
                    f"#pan[%P1](%B2[x:0-35,y:74,w:100%+71,h:0],9) "
                    f"#font(R2C12,BC12,RC12) "
                    f"#txt[%T1](%B2[x:4,y:6,w:100,h:24],{{}},\"From:\") "
                    f"#font(BC12,BC12,RC12) "
                    f"#txt[%T2](%B2[x:%T1+5,y:6,w:270,h:24],{{GW|open&user_details.dcml\\00&ID={message.player_id}\\00|LW_lockall}},\"{{{message.name}\") "
                    f"#font(R2C12,BC12,BC12) "
                    f"#txt[%T3](%B2[x:4,y:24,w:100,h:24],{{}},\"Subject:\") "
                    f"#font(BC12,BC12,RC12) "
                    f"#txt[%T4](%B2[x:%T3+5,y:24,w:380,h:24],{{}},\"{message.subject}\") "
                    f"#font(BC12,R2C12,R2C12) "
                    f"#txt[%T5](%B2[x:292,y:6,w:250,h:24],{{}},\"{{Date: }}{message.sent_at}\") "
                    f"#txt[%T7](%B2[x:4,y:50,w:100%-20,h:100%-57],{{}},\"{message.content}\") "
                    f"#font(BC14,WC14,BC14) "
                    f"#sbtn[%del](%B[x:401,y:377,w:100,h:305],{{GW|open&mail_list.dcml\\00&messageID={variables['messageID']}^delete=1^readable={variables['readable']}^sent={variables['sent']}\\00|LW_lockall}},\"Delete\") "
                    f"#sbtn[%rep](%B[x:521,y:377,w:100,h:305],{{GW|open&mail_new.dcml\\00&send_to={message.name}^subject=Re: {message.subject}\\00|LW_lockall}},\"Reply\") "
                    f"#sbtn[%for](%B[x:641,y:377,w:100,h:305],{{GW|open&mail_new.dcml\\00&subject={message.subject}^message={message.content}\\00|LW_lockall}},\"Forward\") "
                    f"<NGDLG> "
                    f"<NGDLG> "
                    f"#block(cancel.cml,CAN)<NGDLG> "
                    f"<NGDLG> "
                    f"#end(CAN)"
                )


@alexander.route('map.dcml')
def map_(**kwargs) -> str:
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"RATING GAMES\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)     "
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)     "
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)     "
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)     "
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")    "
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>#exec(GW|open&voting.dcml\\00&question=46\\00)<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#map[%MAP](%B[x:0,y:40,w:535,h:296],{{ROME}}{{GW|open&mclick.dcml\\00&MAP=%s^X=%d^Y=%d\\00|LW_lockall}})"
        # f"//#pix[%FALS](%B[x:0,y:40,w:118,h:25],{{}},Internet/pix/awards,25,25,25,25)"
        f"#pan[%PAN1](%B[x:550,y:42,w:164,h:291],7)"
        f"#font(BC12,BC12,BC12)"
        f"#txt[%BH1](%B[x:555,y:47,w:158,h:20],{{}},\"Click on the area of a chosen nation and then press \'Fight\' button. Other player must do the same. Players cannot play for the same nation. The server will choose an opponent automatically after comparing rating of the players (if there are more than 2 players). After the end of the game the player that lost it looses a segment of his nation-controlled area and the winning player gains control over that area. If time of the game is less than 10 minutes, its results are of no effect on the rating.\")"
        f"#font(BC14,WC14,BC14)"
        f"#sbtn[%BTN1](%B[x:521,y:377,w:100,h:305],{{GW|open&rating_help.dcml\\00|LW_lockall}},\"Rating describe\")"
        f"#font(R0C14,R0C14,R0C14)"
        f"#pix[%BTXT10](%B[x:602,y:353,w:118,h:25],{{}},Internet/pix/i_pri0,54,54,54,54)"
        f"#ctxt[%BTIT10](%B[x:602,y:359,w:118,h:20],{{}},\"Fight\")"
        f"<MCLICK>"
        f"<MCLICK>"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )

# TODO: PLACEHOLDER
@alexander.route('mclick.dcml')
def mclick(variables: dict, **kwargs) -> str:
    # <MCLICK> #ebox[%M](x:550,y:42,w:164,h:291) #font(RG18,WF16,WF16) #pan[%PAN1](%M[x:0,y:0,w:100%,h:100%],
    # 7) #ctxt[%TIT](%M[x:5,y:10,w:100%-10,h:30],{},"Persia") #font(BC12,RC12,RC12) #stbl[%TBL](%M[x:5,y:50,
    # w:100%-10,h:100%],{},2,0,70%,0,30%,1,20,"Total wins","615",20,"Total losses","439",20,"Country area","41246",
    # 20,"Current area","41189") #font(BC14,WC14,BC14) #sbtn[%B_J](%M[x:91,y:335,w:100,h:305],
    # {GW|open&enter_game_dlg.dcml\00&land_id=1\00|LW_lockall},"Fight") <MCLICK>
    return (
        f"<MCLICK>"
        f"<MCLICK>"
    )

# TODO: PLACEHOLDER
@alexander.route('enter_game_dlg.dcml')
def enter_game_dlg(**kwargs) -> str:
    # · ·· ·open· ·   enter_game_dlg.dcml
    # land_id=2 ·   02     35070762
    # HOST
    # <NGDLG>
    ##exec(LW_file&Internet/Cash/cancel.cml|LW_gvar&%GOPT&/NAT3 /OPT00 /OPT10 /OPT20 /OPT30 /OPT60 /PAGE2 /NOCOMP&%CG_GAMEID&2852165&%CG_MAXPL&2&%CG_GAMENAME&"Rating Game"&%COMMAND&CGAME)
    # <NGDLG>

    # CLIENT
    # <NGDLG>
    # #exec(LW_file&Internet/Cash/cancel.cml|LW_gvar&%GOPT&/NAT1&%CG_GAMEID&2852171&%CG_MAXPL&2&%CG_GAMENAME&"Rating Game"&%COMMAND&JGAME&%CG_IP&)
    # <NGDLG>

    # with alexander.engine.connect() as connection:
    #     types = connection.execute(text(f"SELECT name FROM lobby_types")).fetchall()
    return (
        f"<NGDLG>"
        f"#exec(LW_time&3000&l_games_btn.cml\\00)"
        f"#block(l_games_btn.cml,l_g):GW|open&enter_game_dlg.dcml\\00&id_room=2852165^land_id=2^connect=1\\00|LW_lockall"
        f"#end(l_g)"
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)"
        f"#def_dtbl_button_hotkey(27)"
        f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&cancel.dcml\\00|LW_lockall}},2,0,3,13,252,\"ENTER GAME\",,0,\"Cancel\")"
        f"#ebox[%L](x:242,y:100,w:100%,h:100%)"
        f"#font(BC14,RC14,RC14)"
        f"#ctxt[%LIST1](%L[x:0,y:96,w:414,h:24],{{}},\"Please, wait.\")"
        f"#pix[%PX](%L[x:40,y:112,w:100%,h:100%],{{}},Interf3/elements/delimeter,4,4,4,4)"
        f"#ctxt[%LIST2](%L[x:0,y:128,w:414,h:24],{{}},\"searching other players...\")"
        f"<NGDLG>"
    )


@alexander.route('new_game_dlg.dcml')
def new_game_dlg(variables: dict, player_id, **kwargs) -> str:
    if variables['max_players'] and variables['type']:
        gameType = variables.get('type', 0)
        with alexander.engine.connect() as connection:
            output = connection.execute(
                text(f"SELECT allow_designed, allow_ai FROM lobby_types WHERE id = {int(gameType) + 1} LIMIT 1")).fetchone()
            if output:
                allow_designed, allow_ai = output
            else:
                allow_designed, allow_ai = False, False
            result = connection.execute(text(f'INSERT INTO lobbies (title, host_id, type, max_players, password)\
                    VALUES ("{variables["title"]}", "{player_id}", "{int(gameType) + 1}", "{int(variables["max_players"])+2}", "{variables["password"]}")\
                    ON DUPLICATE KEY UPDATE title = "{variables["title"]}", type = "{int(gameType) + 1}", max_players = "{int(variables["max_players"])+2}", password = "{variables["password"]}"'))
            connection.commit()
            gameID = result.lastrowid
            return (
                f'<NGDLG>'
                f'#ebox[%L0](x:0,y:0,w:100%,h:100%)'
                f'#exec(LW_file&Internet/Cash/cancel.cml|LW_gvar&'
                f'%GOPT&'
                f'{" /OPT00 /OPT10 /OPT20 /OPT30 /OPT60 " if allow_designed == 0 and allow_ai == 0 else " "} '
                f'/PAGE{"0" if allow_designed == 1 else "2"} /{"" if allow_ai == 1 else "NO"}COMP&'
                f'%CG_GAMEID&{gameID}&'
                f'%CG_MAXPL&{int(variables["max_players"])+2}&'
                f'%CG_GAMENAME&\"{variables["title"]}\"&'
                f'%COMMAND&'
                f'CGAME)'
                f'<NGDLG>'
            )
    else:
        title = "Lobby"
        with alexander.engine.connect() as connection:
            types = connection.execute(text(f"SELECT name FROM lobby_types")).fetchall()
            player = connection.execute(text(f"SELECT get_display_nick({player_id}) AS nick")).fetchone()
            if player: 
                title = player._mapping['nick']
        return (
            f"<NGDLG>"
            f"#ebox[%L0](x:0,y:0,w:100%,h:100%)"
            f"#exec(LW_cfile&{title}\\00&Cookies/%GV_VE_TITLE)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASSWD)"
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_MAX_PL)"
            f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&new_game_dlg.dcml\\00&max_players=<%GV_VE_MAX_PL>^type=<%GV_VE_TYPE>^password=<%GV_VE_PASSWD>^title=<%GV_VE_TITLE>\\00|LW_lockall}}{{GW|open&cancel.dcml\\00|LW_lockall}},1,0,13,252,\"CREATE NEW GAME\",,26,\"Create\",\"Cancel\")"
            f"#ebox[%L](x:245,y:100,w:450,h:210)"
            f"#font(BC12,RC12,RC12)"
            f"#txt[%L_NAME](%L[x:11,y:48,w:160,h:20],{{}},\"Game Title:\")"
            f"#pan[%P_NAME](%L[x:15,y:68,w:382,h:14],1)"
            f"#font(BC12,GC12,GC12)"
            f"#edit[%E_NAME](%L[x:19,y:67,w:377,h:18],{{%GV_VE_TITLE}},0,0,0,1)"
            f"#font(BC12,RC12,RC12)"
            f"#txt[%L_PASS](%L[x:11,y:95,w:160,h:20],{{}},\"Password:\")"
            f"#pan[%P_PASS](%L[x:15,y:114,w:382,h:14],1)"
            f"#font(BC12,GC12,GC12)"
            f"#edit[%E_PASS](%L[x:19,y:113,w:377,h:18],{{%GV_VE_PASSWD}},0,0,1)"
            f"#font(BC14,RC14,RC14)"
            f"#txt[%L_MAXPL](%L[x:11,y:145,w:150,h:24],{{}},\"Max Players:\")"
            f"#cbb[%E_MAXPL](%L[x:130,y:139,w:273,h:24],{{%GV_VE_MAX_PL}},2,3,4,5,6,7,0)"
            f"#font(BC14,RC14,RC14)"
            f"#txt[%L_MAXPL](%L[x:11,y:175,w:151,h:24],{{}},\"Type:\")"
            f"#cbb[%E_TYPE](%L[x:130,y:169,w:273,h:24],{{%GV_VE_TYPE}},{''.join([f'{type[0]},' for type in types])})"
            f"<NGDLG>"
        )


@alexander.route('news.dcml')
def news(**kwargs) -> str:
    with alexander.engine.connect() as connection:
        news = connection.execute(text(f"SELECT posted_at, content FROM news ORDER BY id DESC")).fetchall()
    news_board = []
    if news:
        news_board.append(f"\
                    #font(BC12,BC12,RC12)\
                    #txt[%TEXT0](%SB[x:85,y:8,w:100%-90,h:24],{{}},\"{news[0][1]}\")\
                    #font(BC14,BC14,RC14)\
                    #ctxt[%DATE0](%SB[x:0,y:8,w:78,h:24],{{}},\
                    {' - ' if not isinstance(news[0][0], datetime) else news[0][0].strftime('%d/%m/%Y')})")  # type: ignore
        if len(news) > 1:
            for idx, n in enumerate(news[1:]):
                news_board.append(f"\
                    #font(BC12,BC12,RC12)\
                    #txt[%TEXT{idx + 1}](%SB[x:85,y:%TEXT{idx}+27,w:100%-90,h:24],{{}},\"{n[1]}\")\
                    #font(BC14,BC14,RC14)\
                    #ctxt[%DATE{idx + 1}](%SB[x:0,y:%TEXT{idx}+27,w:78,h:24],{{}},\
                    {' - ' if not isinstance(news[0][0], datetime) else n[0].strftime('%d/%m/%Y')})")  # type: ignore
    news_board = "".join(news_board)
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")\""
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")"
        f"#font(R2C14,R2C14,RC14)"
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")"
        f"#hint(%LIST2,\"List of punished players\")"
        f"#edit[%E_FT](%B[x:0,y:0,w:0,h:0],{{%GV_FORUM_LAST_TIME}})"
        f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=<%GV_FORUM_LAST_TIME>\\00|LW_lockall}},\"{{Forum}}\")"
        f"#hint(%LIST3,\"Read and write forum messages\")"
        f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)"
        f"#sbox[%SB](x:150,y:46,w:526+4,h:291-8)" +
        (news_board if news_board else (
            f"#font(RG18,RG18,RG18)"
            f"#ctxt[%T0](%B[x:154,y:179,w:559,h:20],{{}},\"No search results\")"
        ))+
        f"#ebox[%B1](x:0,y:0,w:100%,h:100%)"
        f"#pan[%PANV](%B1[x:260,y:8,w:0,h:359],10)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('punishments.dcml')
def punishments(**kwargs) -> str:
    with alexander.engine.connect() as connection:
        punishment_list = []
        punishments = connection.execute(text(
            "CALL get_punishments()"
        )).fetchall()
        for idx, entry in enumerate(punishments):
            punishment = entry._mapping
            punishment_list.append(
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%MSG{idx + 1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'},w:570,h:20],{{}},\"Cancelled game {punishment.game_id} (#).\")"
                f"#font(R2C12,BC12,BC12)"
                f"#txt[%DAT{idx + 1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:90,h:20],{{}},\"Date:\")"
                f"#font(BC12,BC12,BC12)"
                f"#txt[%DATE{idx + 1}](%SB[x:%DAT{idx + 1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:200,h:20],{{}},\"{punishment.published_at}\")"
                f"#font(R2C12,BC12,BC12)"
                f"#txt[%MD{idx + 1}](%SB[x:8,y:{'4' if idx == 0 else f'%P{idx}-21'}+43,w:90,h:20],{{}},\"Moderator:\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%MDR{idx + 1}](%SB[x:%MD{idx + 1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+43,w:200,h:20],{{GW|open&user_details.dcml\\00&ID={punishment.moderator_id}\\00|LW_lockall}},\"{{{punishment.nick}}}\")"
                f"#font(R2C12,BC12,BC12)"
                f"#txt[%CM{idx + 1}](%SB[x:210,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:100,h:20],{{}},\"Comments:\")"
                f"#font(BC12,BC12,BC12)"
                f"#txt[%CMT{idx + 1}](%SB[x:%CM{idx + 1}+5,y:{'4' if idx == 0 else f'%P{idx}-21'}+29,w:256,h:20],{{}},\"{punishment.comment}\")"
                f"#pan[%P{idx + 1}](%SB[x:0-32,y:%MDR{idx + 1}>%CMT{idx + 1}+38,w:100%+65,h:0],9)"
            )
    punishment_list = "".join(punishment_list)
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(RC14,R2C14,RC14)"
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")"
        f"#hint(%LIST2,\"List of punished players\")"
        f"#font(R2C14,R2C14,RC14)"
        f"#edit[%E_FT](%B[x:0,y:0,w:0,h:0],{{%GV_FORUM_LAST_TIME}})"
        f"#ctxt[%LIST3](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=<%GV_FORUM_LAST_TIME>\\00|LW_lockall}},\"{{Forum}}\")"
        f"#hint(%LIST3,\"Read and write forum messages\")"
        f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)"
        f"#sbox[%SB](x:150,y:46,w:526+4,h:291-8)"+
        (punishment_list if punishment_list else (
            f"#font(RG18,RG18,RG18)"
            f"#ctxt[%T0](%B[x:154,y:179,w:559,h:20],{{}},\"No search results\")"
        ))+
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('rating_calculator.dcml')
def rating_calculator(variables: dict, **kwargs) -> str:
    error = False
    if (variables['score1'] and variables['score2']) and (
            variables['score1'].isdigit() and variables['score2'].isdigit()):
        you, opponent = int(clip_string(variables['score1'], 9)), int(clip_string(variables['score2'], 9))
        win = abs(floor(clip(you + 10 * 1 * (opponent + 100) / (you + 100) - you, 1, 100)))
        loss = abs(ceil(clip(you + 10 * -1 * (you + 100) / (opponent + 100) - you, -100, -1)))
    else:
        error = True
        win, loss, you, opponent = 0, 0, 0, 0
    return (
        f"<RGDLG>"
        f"#ebox[%B2](x:427,y:266,w:288,h:72)"
        f"#def_panel(9,Internet/pix/i_pri0,-1,-1,-1,-1,-1,-1,30,-1,-1,-1)"
        f"#pan[%P4](%B2[x:31,y:0-32,w:0,h:137],10)"
        f"#pan[%P5](%B2[x:127,y:0-32,w:0,h:137],10)"
        f"#pan[%P6](%B2[x:223,y:0-32,w:0,h:137],10)"
        f"#font(R2C12,BC12,BC12)"
        f"#ctxt[%I1](%B2[x:96,y:1,w:96,h:20],{{}},\"You\")"
        f"#ctxt[%I2](%B2[x:192,y:1,w:96,h:20],{{}},\"Enemy\")" +
        ("#pan[%P1](%B2[x:64,y:49,w:257,h:0],9)" if not win or not loss else "") +
        f"#pan[%P2](%B2[x:0-32,y:67,w:353,h:0],9)"
        f"#pan[%P3](%B2[x:0-32,y:85,w:353,h:0],9)"
        f"#font(R2C14,R2C14,R2C14)"
        f"#ctxt[%I3](%B2[x:0,y:11,w:96,h:20],{{}},\"Score\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#ctxt[%I3](%B2[x:0,y:36,w:96,h:20],{{}},\"You win\")"
        f"#ctxt[%I3](%B2[x:0,y:54,w:96,h:20],{{}},\"You lose\")"
        f"#font(BC12,R2C12,R2C12)" +
        (f'#stbl[%TBL](%B2[x:96,y:36,w:192,h:36],{{}},2,0,50,1,50,1,17,\"+{win} pt\",\"-{win} pt\",17,\"-{loss} pt\",\"+{loss} pt\")' if not error else '') +
        f"#pan[%P1](%B2[x:104,y:18,w:80,h:10],1)"
        f"#font(BC12,RC12,RC12)"
        f"#edit[%E1](%B2[x:104,y:15,w:80,h:17],{{%GV_SCORE1}},0,1)"
        f"#pan[%P2](%B2[x:200,y:18,w:80,h:10],1)"
        f"#edit[%E2](%B2[x:200,y:15,w:80,h:17],{{%GV_SCORE2}},0,1,0,1)"
        f"#exec(LW_cfile&{variables['score1']}\\00&Cookies/%GV_SCORE1)" +
        (f"#exec(LW_cfile&{variables['score2']}\\00&Cookies/%GV_SCORE2)" if not error else '') +
        f"#exec(LW_cfile&0\\00&Cookies/%GV_SCORE1)"
        f"#exec(LW_cfile&0\\00&Cookies/%GV_SCORE2)"
        f"#font(BC14,WC14,BC14)"
        f"#sbtn[%BT](%B2[x:242,y:110,w:45,h:205],"
        f"{{GW|open&rating_calculator.dcml\\00&score1=<%GV_SCORE1>^score2=<%GV_SCORE2>\\00|LW_lockall}},\"Calculate\")"
        f"<RGDLG>"
    )


@alexander.route('rating_help.dcml')
def rating_help(**kwargs) -> str:
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"RATING GAMES\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(R2C14,R2C14,RC14)"
        
        # f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&rating_help.dcml\\00|LW_lockall}},\"{{Rating Games}}\")"
        # # f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&map.dcml\\00|LW_lockall}},\"{{Rating Games}}\")"
        # f"#hint(%LIST1,\"Play rating games\")"
        # f"#font(RC14,GC14,RC14)"
        # f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&rating_help.dcml\\00|LW_lockall}},\"{{Rating describe}}\")"
        
        f"#ctxt[%TIT1](%B[x:0,y:106,w:146,h:24],{{GW|open&games.dcml\\00|LW_lockall}},\"{{Custom Games}}\")"
        f"#hint(%TIT1,\"Play custom games\")"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%LIST33](%B[x:0,y:%TIT1-9,w:146,h:24],{{GW|open&rating_help.dcml\\00|LW_lockall}},\"{{Rating Describe}}\")"
        
        f"#ebox[%B1](x:154,y:42,w:559,h:291)"
        f"#def_panel(9,Internet/pix/i_pri0,-1,-1,-1,-1,-1,-1,30,-1,-1,-1)"
        f"#pan[%P](%B1[x:0,y:0,w:100%,h:100%],5)"
        f"#pan[%P1](%B1[x:0-32,y:87,w:630,h:0],9)"
        f"#pan[%P2](%B1[x:0-32,y:255,w:630,h:0],9)"
        f"#pan[%P3](%B1[x:131,y:24,w:0,h:232],10)"
        f"#font(R2C14,R2C14,RC14)"
        f"#txt[%I1](%B1[x:8,y:8,w:400,h:20],{{}},\"In rating games, the score is calculated with the formula::\")"
        f"#font(BC14,BC14,RC14)"
        f"#txt[%I2](%B1[x:115,y:28,w:400,h:20],{{}},\"new_score = old_score + 10 * coeff_result * coeff_differ\")"
        f"#font(R2C12,R2C12,RC12)"
        f"#txt[%I3](%B1[x:8,y:65,w:400,h:20],{{}},\"where\")"
        f"#font(BC12,BC12,RC12)"
        f"#txt[%I4](%B1[x:115,y:65,w:400,h:20],{{}},\"old_score - Your score before starting game,\")"
        f"#txt[%I5](%B1[x:115,y:80,w:400,h:20],{{}},\"new_score - Your score after finishing game,\")"
        f"#font(R2C12,R2C12,RC12)"
        f"#txt[%I6](%B1[x:8,y:108,w:400,h:20],{{}},\"if you win:\")"
        f"#font(BC12,BC12,RC12)"
        f"#txt[%I7](%B1[x:115,y:108,w:400,h:20],{{}},\"coeff_result equil 1,\")"
        f"#txt[%I8](%B1[x:115,y:123,w:400,h:20],{{}},\"coeff_differ = (enemy_score + 100) / (old_score + 100),\")"
        f"#font(R2C12,R2C12,RC12)"
        f"#txt[%I9](%B1[x:8,y:150,w:400,h:20],{{}},\"in case you lose:\")"
        f"#font(BC12,BC12,RC12)"
        f"#txt[%I10](%B1[x:115,y:150,w:400,h:20],{{}},\"coeff_result equil -1,\")"
        f"#txt[%I11](%B1[x:115,y:165,w:400,h:20],{{}},\"coeff_differ = (old_score + 100) / (enemy_score + 100),\")"
        f"#font(R2C12,R2C12,RC12)"
        f"#txt[%I12](%B1[x:8,y:192,w:400,h:20],{{}},\"where\")"
        f"#font(BC12,BC12,RC12)"
        f"#txt[%I23](%B1[x:115,y:192,w:400,h:20],{{}},\"enemy_score - opponents score before starting game\")"
        f"#font(R2C14,R2C14,RC14)"
        f"#txt[%I14](%B1[x:8,y:228,w:250,h:20],{{}},\"For testing enter your opponents score and press calculate.\")"
        f"<RGDLG>"
        f"#exec(GW|open&rating_calculator.dcml\\00|LW_lockall)"
        f"<RGDLG>"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('reg_new_user.dcml')
def reg_new_user(variables: dict, **kwargs) -> str | None:
    try:
        with alexander.engine.connect() as connection:
            connection.execute(text(
                f"CALL reg_new_user("
                f"'{variables['VE_MODE']}','{variables['VE_NICK']}','{variables['VE_NAME']}','{variables['VE_MAIL']}',"
                f"'{variables['VE_ICQ']}','{variables['VE_HOMP']}',{variables['VE_SEX']},{variables['VE_CNTRY']},"
                f"'{variables['VE_PHON']}','{variables['VE_BIRTH']}','{variables['VE_GMID']}','{variables['VE_PASS']}',"
                f"'{variables['VE_RASS']}')"))
            connection.commit()

        if variables['VE_MODE'] == 'edit':
            new_password = (f"Your new password is: {variables['VE_RASS']}\\Please keep it in safety and make sure it "
                            f"does not get lost.\\") if \
                variables['VE_PASS'] != variables['VE_RASS'] else ''
            return (
                f"<MESDLG>"
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768)"
                f"#edit[%E_AC](%MBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})"
                f"#exec(LW_cfile&{variables['VE_NICK']}\\00&Cookies/%GV_VE_NICK)"
                f"#exec(LW_cfile&{variables['VE_RASS']}\\00&Cookies/%GV_VE_PASS)"
                f"#exec(LW_cfile&{variables['VE_GMID']}\\00&Cookies/%GV_VE_GMID)"
                f"#def_dtbl_button_hotkey(13,27)"
                f"#def_dtbl_button_hotkey(13,27)"
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_user.dcml\\00&"
                f"VE_PROF={variables['VE_PROF']}^"
                f"save_pass={variables['save_pass']}^"
                f"VE_MODE={variables['VE_MODE']}^"
                f"VE_NAME={variables['VE_NAME']}^"
                f"VE_NICK={variables['VE_NICK']}^"
                f"VE_MAIL={variables['VE_MAIL']}^"
                f"VE_PASS={variables['VE_RASS']}^"
                f"VE_RASS={variables['VE_RASS']}^"
                f"VE_ICQ={variables['VE_ICQ']}^"
                f"VE_HOMP={variables['VE_HOMP']}^"
                f"VE_SEX={variables['VE_SEX']}^"
                f"VE_CNTRY={variables['VE_CNTRY']}^"
                f"VE_PHON={variables['VE_PHON']}^"
                f"VE_BIRTH={variables['VE_BIRTH']}^"
                f"VE_GMID={variables['VE_GMID']}"
                f"\\00|LW_lockall}}{{GW|open&log_user.dcml\\00&"
                f"VE_PROF={variables['VE_PROF']}^"
                f"cansel={variables['cansel']}^"
                f"VE_MODE={variables['VE_MODE']}^"
                f"VE_NAME={variables['VE_NAME']}^"
                f"VE_NICK={variables['VE_NICK']}^"
                f"VE_MAIL={variables['VE_MAIL']}^"
                f"VE_PASS={variables['VE_RASS']}^"
                f"VE_RASS={variables['VE_RASS']}^"
                f"VE_ICQ={variables['VE_ICQ']}^"
                f"VE_HOMP={variables['VE_HOMP']}^"
                f"VE_SEX={variables['VE_SEX']}^"
                f"VE_CNTRY={variables['VE_CNTRY']}^"
                f"VE_PHON={variables['VE_PHON']}^"
                f"VE_BIRTH={variables['VE_BIRTH']}^"
                f"VE_GMID={variables['VE_GMID']}"
                f"\\00|LW_lockall}},2,0,3,13,252,"
                f"\"INFORMATION\",\"Your personal profile data has been successfully updated!\\"
                f"{new_password}"
                f"Press OK button to save password, in other case press Cancel.\\This option saves your password and "
                f"Game Box #ID. Don't use it, if you play from computer accessible for other people.\",26,\"OK\","
                f"\"Cancel\")"
                f"<MESDLG>")

        elif variables['VE_MODE'] == 'creat':
            return (
                f"<MESDLG>"
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768)"
                f"#edit[%E_AC](%MBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})"
                f"#exec(LW_cfile&{variables['VE_NICK']}\\00&Cookies/%GV_VE_PASS)"
                f"#exec(LW_cfile&{variables['VE_RASS']}\\00&Cookies/%GV_VE_RASS)"
                f"#exec(LW_cfile&{variables['VE_GMID']}\\00&Cookies/%GV_VE_GMID)"
                f"#def_dtbl_button_hotkey(13,27)"
                f"#def_dtbl_button_hotkey(13,27)"
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_user.dcml\\00&"
                f"VE_PROF={variables['VE_PROF']}^"
                f"save_pass={variables['save_pass']}^"
                f"VE_MODE={variables['VE_MODE']}^"
                f"VE_NAME={variables['VE_NAME']}^"
                f"VE_NICK={variables['VE_NICK']}^"
                f"VE_MAIL={variables['VE_MAIL']}^"
                f"VE_PASS={variables['VE_PASS']}^"
                f"VE_RASS={variables['VE_RASS']}^"
                f"VE_ICQ={variables['VE_ICQ']}^"
                f"VE_HOMP={variables['VE_HOMP']}^"
                f"VE_SEX={variables['VE_SEX']}^"
                f"VE_CNTRY={variables['VE_CNTRY']}^"
                f"VE_PHON={variables['VE_PHON']}^"
                f"VE_BIRTH={variables['VE_BIRTH']}^"
                f"VE_GMID={variables['VE_GMID']}"
                f"\\00|LW_lockall}}{{GW|open&log_user.dcml\\00&"
                f"VE_PROF={variables['VE_PROF']}^"
                f"cansel={variables['cansel']}^"
                f"VE_MODE={variables['VE_MODE']}^"
                f"VE_NAME={variables['VE_NAME']}^"
                f"VE_NICK={variables['VE_NICK']}^"
                f"VE_MAIL={variables['VE_MAIL']}^"
                f"VE_PASS={variables['VE_PASS']}^"
                f"VE_RASS={variables['VE_RASS']}^"
                f"VE_ICQ={variables['VE_ICQ']}^"
                f"VE_HOMP={variables['VE_HOMP']}^"
                f"VE_SEX={variables['VE_SEX']}^"
                f"VE_CNTRY={variables['VE_CNTRY']}^"
                f"VE_PHON={variables['VE_PHON']}^"
                f"VE_BIRTH={variables['VE_BIRTH']}^"
                f"VE_GMID={variables['VE_GMID']}"
                f"\\00|LW_lockall}},2,0,3,13,252,"
                f"\"INFORMATION\",\"Your personal profile data has been successfully created!\\Press OK button to "
                f"save password, in other case press Cancel.\\This option saves your password and Game Box #ID. Don't "
                f"use it, if you play from computer accessible for other people.\",26,\"OK\",\"Cancel\")"
                f"<MESDLG>")


    except DBAPIError as err:
        error_message = None
        if err.orig:
            error_message = mysql_error_messages[err.orig.args[1]]
            return (
                f"<MESDLG>"
                f"#ebox[%MBG](x:0,y:0,w:1024,h:768) "
                f"#def_dtbl_button_hotkey(13,27) "
                f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&log_new_form.dcml\\00&logs={variables['logs']}^cansel={variables['cansel']}^VE_MODE={variables['VE_MODE']}^VE_NAME={variables['VE_NAME']}^VE_NICK={variables['VE_NICK']}^VE_MAIL={variables['VE_MAIL']}^VE_ICQ={variables['VE_ICQ']}^VE_HOMP={variables['VE_HOMP']}^VE_SEX={variables['VE_SEX']}^VE_CNTRY={variables['VE_CNTRY']}^VE_PHON={variables['VE_PHON']}^VE_BIRTH={variables['VE_BIRTH']}^accounts={variables['accounts']}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"ERROR\",\"{error_message}\",26,\"Edit\",\"Cancel\")"
                f"<MESDLG>"
            )





# TODO: PLACEHOLDER
@alexander.route('scored_games.dcml')
def scored_games(variables: defaultdict, **kwargs) -> str:
    thread_strings = ""
    thread_list = []
    with alexander.engine.connect() as connection:
        threads = connection.execute(text(
            f"CALL get_scored_games({int(variables['next_message']) if variables['next_message'] else 0})")).fetchall()
        if threads:
            return (
            f'#ebox[%TB](x:0,y:0,w:100%,h:100%)'
            f'#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)'
            f'#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)'
            f'#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)'
            f'#font(RG18,RG18,RG18)'
            f'#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},"Players")"'
            f'#font(BG18,BG18,BG18)'
            f'#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},"SCORED GAMES")'
            f'#font(R2C12,R2C12,R2C12)'
            f'#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},"Message:")'
            f'#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)'
            f'#font(RC12,R2C12,RC12)'
            f'#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},"News & Events")'
            f'#hint(%BT1,"News, events, forum and punishment list")'
            f'#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)'
            f'#font(RC12,R2C12,RC12)'
            f'#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},"Player List")'
            f'#hint(%BT2,"Player list, personal mail and clan information")'
            f'#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)'
            f'#font(RC12,R2C12,RC12)'
            f'#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},"Custom Games")'
            f'#hint(%BT4,"Play custom games")'
            f'#font(RC12,RC12,RC12)'
            f'#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)'
            f'#gpbtn[%BT5](%TB[x:440,y:22,w:-22,h:-18],{{}},"Scored Games")#hint(%BT5,"Played games and their scores")'
            f'#ebox[%B_VOTE](x:5,y:396,w:140,h:103)'
            f'<VOTING>'
            f'#exec(GW|open&voting.dcml\\00&question=46\\00)'
            f'<VOTING>'
            f'#ebox[%B](x:0,y:0,w:100%,h:100%)'
            f'#font(RC14,GC14,RC14)'
            f'#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&scored_games.dcml\\00|LW_lockall}},"{{Scored Games}}")'
            f'#hint(%LIST1,"Played games and their scores")'
            # f'#font(RC14,R2C14,RC14)'
            # f'#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&scored_games2x2.dcml\\00|LW_lockall}},"{{Scored Games 2x2}}")'
            # f'#hint(%LIST2,"Played games and their scores 2x2")'
            f'#font(BC14,WC14,BC14)'
            f'#sbtn[%BTXT2](%B[x:401,y:377,w:100,h:305],{{GW|open&scored_games.dcml\\00&player_id=0^player_nick=\\00|LW_lockall}},"First Page")'
            f'#sbtn[%BTXT3](%B[x:521,y:377,w:100,h:305],{{<!goback!>}},"Back")'
            f'#font(R0C14,R0C14,R0C14)'
            f'#pix[%BTXT10](%B[x:601,y:352,w:118,h:25],{{}},Internet/pix/i_pri0,54,54,54,54)'
            f'#ctxt[%BTIT10](%B[x:601,y:358,w:115,h:20],{{}},"Next")'
            f'#font(R2C12,RC12,RC12)'
            f'#ebox[%BB](x:0,y:0,w:100%,h:100%)'
            f'#stbl[%TBL0](%BB[x:154,y:42,w:559,h:291],{{}},5,7,34,1,26,1,15,1,15,1,10,1,20,"Game / Start time","Player","Result","Nation","Scores")'
            f'#font(BC12,RC12,RC12)'
            f'#stbl[%TBL1](%BB[x:154,y:42+20,w:559,h:291-20],{{}},5,0,34,1,26,1,15,1,15,1,10,1,5,,,,,,16," (#)","","","","",16,"","","","","",13,,,,,,16," (#)","","","","",16,"","","","","",13,,,,,,16," (#)","","","","",16,"","","","","",13,,,,,,16," (#)","","","","",16,"","","","","",13,,,,,,16," (#)","","","","",16,"","","","","",13,,,,,,16," (#)","","","","",16,"","","","","",13,,,,,)'+
            (f'')+
            f'#font(BC14,WC14,BC14)'
            f'#sbtn[%BTXT1](%B[x:641,y:377,w:100,h:305],{{GW|open&scored_games.dcml\\00&player_id=0^player_nick=^next_game=12^games_total=923\\00|LW_lockall}},"Next")'
            f'<NGDLG>'
            f'<NGDLG>'
            f'#block(cancel.cml,CAN)<NGDLG>'
            f'<NGDLG>'
            f'#end(CAN)'
            )
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"SCORED GAMES\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT5](%TB[x:440,y:22,w:-22,h:-18],{{}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&scored_games.dcml\\00|LW_lockall}},\"{{Scored Games}}\")"
        f"#hint(%LIST1,\"Played games and their scores\")"
        # f"#font(RC14,R2C14,RC14)"
        # f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&scored_games2x2.dcml\\00|LW_lockall}},\"{{Scored "
        # f"Games 2x2}}\")"
        # f"#hint(%LIST2,\"Played games and their scores 2x2\")"
        f"#pan[%PAN](%B[x:154,y:42,w:559,h:291],7)"
        f"#font(RG18,RG18,RG18)"
        f"#ctxt[%T0](%B[x:154,y:179,w:559,h:20],{{}},\"No search results\")"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('scored_games2x2.dcml')
def scored_games2x2(**kwargs) -> str:
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"SCORED GAMES\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT5](%TB[x:440,y:22,w:-22,h:-18],{{}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(RC14,R2C14,RC14)"
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&scored_games.dcml\\00|LW_lockall}},\"{{Scored Games}}\")"
        f"#hint(%LIST1,\"Played games and their scores\")"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&scored_games2x2.dcml\\00|LW_lockall}},\"{{Scored Games 2x2}}\")"
        f"#hint(%LIST2,\"Played games and their scores 2x2\")"
        f"#pan[%PAN](%B[x:154,y:42,w:559,h:291],7)"
        f"#font(RG18,RG18,RG18)"
        f"#ctxt[%T0](%B[x:154,y:179,w:559,h:20],{{}},\"No search results\")"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('startup.dcml')
def startup(**kwargs) -> str:
    return (
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
        f"#font(RG18,RG18,RG18)"
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
        f"#font(BG18,BG18,BG18)"
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"CUSTOM GAMES\")"
        f"#font(R2C12,R2C12,R2C12)"
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"Lobbies\")"
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
        f"#hint(%BT1,\"News, events, forum and punishment list\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")"
        f"#hint(%BT2,\"Player list, personal mail and clan information\")"
        f"#font(RC12,RC12,RC12)"
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
        f"#gpbtn[%BT4](%TB[x:318,y:22,w:-22,h:-18],{{}},\"Custom Games\")"
        f"#hint(%BT4,\"Play custom games\")"
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
        f"#font(RC12,R2C12,RC12)"
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
        f"#hint(%BT5,\"Played games and their scores\")"
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
        f"<VOTING>"
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
        f"<VOTING>"
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
        f"#font(RC14,GC14,RC14)"
        f"#ctxt[%TIT1](%B[x:0,y:106,w:146,h:24],{{GW|open&games.dcml\\00|LW_lockall}},\"{{Custom Games}}\")"
        f"#hint(%TIT1,\"Play custom games\")"
        f"#ctxt[%LIST33](%B[x:0,y:%TIT1-9,w:146,h:24],{{GW|open&rating_help.dcml\\00|LW_lockall}},\"{{Rating Describe}}\")"
        f"#pan[%PAN](%B[x:154,y:42,w:523,h:291],7)"
        f"#font(BC14,WC14,BC14)"
        f"#sbtn[%B_R](%B[x:521,y:377,w:100,h:305],{{GW|open&random_game_dlg.dcml\\00|LW_lockall}},\"Fight\")"
        f"#sbtn[%B_C](%B[x:641,y:377,w:100,h:305],{{GW|open&new_game_dlg.dcml\\00&delete_old=true\\00|LW_lockall}},\"Create\")"
        f"<DBTBL>"
        f"#exec(GW|open&dbtbl.dcml\\00)"
        f"<DBTBL>"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#block(cancel.cml,CAN)"
        f"<NGDLG>"
        f"<NGDLG>"
        f"#end(CAN)"
    )


@alexander.route('user_details.dcml')
def user_details(variables: dict, player_id, **kwargs) -> str | None:
    with alexander.engine.connect() as connection:
        profile = connection.execute(text(
            f"CALL get_user_details({variables['ID']})"
        )).fetchone()
        if profile:
            profile = profile._mapping
            can_be_excluded = connection.execute(text(
                f"CALL can_be_excluded({variables['ID']}, {player_id})"
            )).fetchone()
            exclude_button = ""
            if can_be_excluded == 'true':
                can_be_excluded = can_be_excluded._mapping
                exclude_button = \
                    "#sbtn[%BTXT3](%B[x:521,y:377,w:100,h:305],{GW|open&clan_users.dcml\\00&clanID=6854^exclude_from_clan=81917\\00|LW_lockall},\"Exclude from clan\")" \
                        if can_be_excluded.result else ""
            clan_str = f"{{GW|open&clan_users.dcml\\00&clanID={profile.clan_id}\\00|LW_lockall}},\"{{{profile.signature}\")" if profile.clan_id else "{},\"\")"
            return (
                f"#ebox[%TB](x:0,y:0,w:100%,h:100%)"
                f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)"
                f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)"
                f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)"
                f"#font(RG18,RG18,RG18)"
                f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")"
                f"#font(BG18,BG18,BG18)"
                f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\")"
                f"#font(R2C12,R2C12,R2C12)"
                f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")"
                f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)"
                f"#font(RC12,R2C12,RC12)"
                f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")"
                f"#hint(%BT1,\"News, events, forum and punishment list\")"
                f"#font(RC12,RC12,RC12)"
                f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)"
                f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{GW|open&users_list.dcml\\00&language=\\00|LW_lockall}},\"Player List\")"
                f"#hint(%BT2,\"Player list, personal mail and clan information\")"
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                f"#font(RC12,R2C12,RC12)"
                f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")"
                f"#hint(%BT4,\"Play custom games\")"
                f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)"
                f"#font(RC12,R2C12,RC12)"
                f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")"
                f"#hint(%BT5,\"Played games and their scores\")"
                f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)"
                f"<VOTING>"
                f"#exec(GW|open&voting.dcml\\00&question=46\\00)"
                f"<VOTING>"
                f"#ebox[%B](x:0,y:0,w:100%,h:100%)"
                f"#font(RC14,GC14,RC14)"
                f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\")"
                f"#hint(%LIST1,\"Player list, personal mail and clan information\")"
                f"#font(RC12,BC12,BC12)"
                f"#stbl[%TBL0](%B[x:154,y:42,w:559,h:291],{{}},1,7,100,0,20,\"Player {profile.nick}\")"
                f"#ebox[%BG](x:431,y:40,w:177,h:118)"
                f"#pix[%PXGB](%BG[x:0,y:0,w:100%,h:100%],{{}},Internet/pix/awards,24,24,24,24)"
                f"#pix[%PXG](%BG[x:0,y:0,w:100%,h:100%],{{}},Internet/pix/awards{(','+str(clip(profile.player_rank-1, 0, 23)))*4})"
                f"#ebox[%B1](x:154,y:42,w:559,h:291)"
                f"#pan[%PAN2](%B1[x:277+32,y:0-34,w:0,h:100%+68],10)"
                f"#pan[%PAN3](%B1[x:159,y:0-14,w:0,h:100%+48],10)"
                f"#ebox[%B2](x:154,y:42,w:559,h:291)"
                f"#font(R2C12,BC12,BC12)"
                f"#txt[%RANK_TIT](%B2[x:294,y:12,w:100,h:24],{{}},\"Current Rank\")"
                f"#font(RC14,BC14,BC14)"
                f"#txt[%RANK](%B2[x:294,y:28,w:250,h:24],{{}},\"{profile.rank_name}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN0](%B1[x:8,y:25,w:140,h:20],{{}},\"Full Name\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL0](%B1[x:138,y:25,w:135,h:20],{{}},\"{profile.name}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN1](%B1[x:8,y:%VAL0+4,w:140,h:20],{{}},\"Nickname\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL1](%B1[x:138,y:%VAL0+4,w:135,h:20],{{}},\"{profile.nick}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN2](%B1[x:8,y:%VAL1+4,w:140,h:20],{{}},\"Clan\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL2](%B1[x:138,y:%VAL1+4,w:135,h:20],"
                f"{clan_str}"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN3](%B1[x:8,y:%VAL2+4,w:140,h:20],{{}},\"E-Mail Address\")"
                f"#font(RC12,BC12,RC12)"
                f"#txt[%VAL3](%B1[x:138,y:%VAL2+4,w:135,h:20],{{GW|open&url_open.dcml\\00&URL=mailto:{profile.mail}\\00|LW_lockall}},\"{{{profile.mail}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN4](%B1[x:8,y:%VAL3+4,w:140,h:20],{{}},\"ICQ #ID\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL4](%B1[x:138,y:%VAL3+4,w:135,h:20],{{}},\"{profile.icq}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN5](%B1[x:8,y:%VAL4+4,w:140,h:20],{{}},\"Internet Homepage\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL5](%B1[x:138,y:%VAL4+4,w:135,h:20],{{}},\"{profile.site}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN6](%B1[x:8,y:%VAL5+4,w:140,h:20],{{}},\"Gender\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL6](%B1[x:138,y:%VAL5+4,w:135,h:20],{{}},\"{profile.sex}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN7](%B1[x:8,y:%VAL6+4,w:140,h:20],{{}},\"Country\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL7](%B1[x:138,y:%VAL6+4,w:135,h:20],{{}},\"{profile.country}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN8](%B1[x:8,y:%VAL7+4,w:140,h:20],{{}},\"Phone\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL8](%B1[x:138,y:%VAL7+4,w:135,h:20],{{}},\"{profile.phone}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN9](%B1[x:8,y:%VAL8+4,w:140,h:20],{{}},\"Birthday (D/M/Y)\")"
                f"#font(BC12,BC12,RC12)"
                f"#txt[%VAL9](%B1[x:138,y:%VAL8+4,w:135,h:20],{{}},\"{profile.birthday}\")"
                f"#font(R2C12,BC12,RC12)"
                f"#txt[%SIGN10](%B1[x:8,y:%VAL9+4,w:140,h:20],{{}},\"Score\")"
                f"#font(RC12,BC12,RC12)"
                f"#txt[%VAL10](%B1[x:138,y:%VAL9+4,w:135,h:20],{{}},\"{profile.score}\")"
                f"#font(BC14,WC14,BC14)"
                f"#sbtn[%BTXT1](%B[x:641,y:377,w:100,h:305],{{<!goback!>}},\"Back\")"
                f"#font(R2C12,BC12,RC12)"
                f"#def_tbl_top(Internet/pix/i_pri0,30,30,30,2,-2,-4)"
                f"#stbl[%TBL20](%B1[x:276,y:136,w:289,h:155],{{}},3,0,40%,1,30%,1,30%,1,20,\"Nation\",\"Games\",\"Wins\")"
                f"#font(BC12,RC12,RC12)"
                f"#pan[%PAN6](%B1[x:245,y:165,w:350,h:0],9)"
                f"#pan[%PAN7](%B1[x:245,y:185,w:350,h:0],9)"
                f"#stbl[%TBL2](%B1[x:276,y:155,w:289,h:136],{{}},3,0,40%,1,30%,1,30%,1,21,\"Total\",\"0\",\"0\")"
                f"#font(R2C12,R2C12,RC12)"
                f"#ctxt[%LIST2](%B[x:0,y:%LIST1-10,w:146,h:24],{{GW|open&mail_new.dcml\\00&send_to={profile.player_id}\\00|LW_lockall}},\"{{Send mail}}\")"
                f"#hint(%LIST2,\"Write new mail to current user\")"
                f"#font(R2C14,R2C14,RC14)"
                f"#ctxt[%LIST4](%B[x:0,y:%LIST2+7,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\")"
                f"#hint(%LIST4,\"Clans, their members and details\")"
                f"#font(BC14,WC14,BC14)"
                f"{exclude_button}"
                # sbtn[%BTXT2](%B[x:401,y:377,w:100,h:305],{GW|open&clan_users.dcml\\00&clanID=6854^include_to_clan=81917\\00|LW_lockall},"Include in clan")
                f"<OPENURL>"
                f"<OPENURL>"
                f"<NGDLG>"
                f"<NGDLG>"
                f"#block(cancel.cml,CAN)"
                f"<NGDLG>"
                f"<NGDLG>"
                f"#end(CAN)"
            )


@alexander.route('url_open.dcml')
def url_open(variables: dict, **kwargs) -> str:
    return (
        f"<OPENURL>"
        f"#time(1,open:{variables['URL']})"
        f"<OPENURL>"
    )


@alexander.route('users_list.dcml')
def users_list(variables: dict, **kwargs) -> str:
    user_list = []
    user_buttons = []
    page = variables.get("next_user", 0)
    resort = variables.get("resort", "1")
    order = variables.get("order", "score")
    if order == 'nick':
        order_by = 'players.nick'
    elif order == 'name':
        order_by = 'players.name'
    elif order == 'id':
        order_by = 'players.player_id'
    elif order == 'country':
        order_by = 'players.country'
    else:
        order_by = 'players.score'
    order = 'DESC' if resort == '1' else 'ASC'
    players = None
    with alexander.engine.connect() as connection:
        players = connection.execute(text(
            f"SELECT get_display_nick(player_id), players.name, players.player_id, countries.name, players.score, ranks.name, row_number()\
                        OVER ( order by {order_by} {order} ) AS 'pos'\
                        FROM players\
                        INNER JOIN ranks ON players.clan_rank = ranks.id\
                        LEFT JOIN countries ON players.country = countries.id\
                        ORDER BY {order_by} {order} LIMIT 14 OFFSET {13 * page};")).fetchall()
    user_buttons = "".join([
        f"#apan[%APAN0](%BB[x:150,y:{60 + (21 * idx)}-1,w:100%-161,h:20],{{GW|open&user_details.dcml\\00&ID={player[2]}\\00|LW_lockall}},8)"
        for idx, player in enumerate(players[:13])])
    user_list = "".join([
        f"21,\"{player[6]}\",\"{player[0]}\",\"{player[1]}\",\"{player[2]}\",\"{player[3]}\",\"{player[4]}\",\"{player[5]}\","
        for idx, player in enumerate(players[:13])])
    return "".join((
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
        f"#font(RG18,RG18,RG18)",
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")\"",
        f"#font(BG18,BG18,BG18)",
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"PLAYER LIST\")",
        f"#font(R2C12,R2C12,R2C12)",
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")",
        f"#hint(%BT1,\"News, events, forum and punishment list\")",
        f"#font(RC12,RC12,RC12)",
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
        f"#gpbtn[%BT2](%TB[x:196,y:22,w:-22,h:-18],{{}},\"Player List\")",
        f"#hint(%BT2,\"Player list, personal mail and clan information\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")",
        f"#hint(%BT4,\"Play custom games\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
        f"#hint(%BT5,\"Played games and their scores\")",
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)",
        f"<VOTING>",
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)",
        f"<VOTING>",
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
        f"#font(RC14,GC14,RC14)",
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&users_list.dcml\\00|LW_lockall}},\"{{Player List}}\")",
        f"#font(R2C12,R2C12,RC12)",
        f"#ctxt[%LIST10](%B[x:0,y:%LIST1-10,w:146,h:24],{{GW|open&mail_list.dcml\\00|LW_lockall}},\"{{Mail}}\")",
        f"#hint(%LIST10,\"Manage your personal mail\")",
        f"#font(RC14,R2C14,RC14)",
        f"#ctxt[%LIST2](%B[x:0,y:%LIST10+7,w:146,h:24],{{GW|open&clans_list.dcml\\00|LW_lockall}},\"{{Clan List}}\")",
        f"#hint(%LIST2,\"Clans, their members and details\")",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%BT](%B[x:401,y:377,w:100,h:305],{{GW|open&users_list.dcml\\00&page=0^order=score^resort=1\\00|LW_lockall}},\"First Page\")" if page != 0 else "",
        f"#sbtn[%BT](%B[x:521,y:377,w:100,h:305],{{<!goback!>}},\"Back\")" if page != 0 else "",
        f"#font(R0C14,R0C14,R0C14)",
        f"#pix[%BTXT10](%B[x:602,y:353,w:118,h:25],{{}},Internet/pix/i_pri0,54,54,54,54)",
        f"#ctxt[%BTIT10](%B[x:602,y:359,w:118,h:20],{{}},\"Next\")",
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%)",
        f"#font(RC12,R2C12,RC12)",
        f"#stbl[%TIT](%BB[x:154,y:42,w:559,h:291],",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=score^resort={'1' if order_by == 'players.score' and resort == '0' else '0'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=nick^resort={'1' if order_by == 'players.nick' and resort == '0' else '0'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=name^resort={'1' if order_by == 'players.name' and resort == '0' else '0'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=id^resort={'1' if order_by == 'players.player_id' and resort == '0' else '0'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=country^resort={'1' if order_by == 'players.country' and resort == '0' else '0'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=score^resort={'1' if order_by == 'players.score' and resort == '0' else '0'}\\00|LW_lockall}}",
        f"{{GW|open&users_list.dcml\\00&users_total=^order=score^resort={'1' if order_by == 'players.score' and resort == '0' else '0'}\\00|LW_lockall}},7,7,7,1,21,1,25,1,6,1,15,1,7,1,19,1,20,\"{{Pos\",\"{{Nickname\",\"{{Full Name\",\"{{#\",\"{{Country\",\"{{Scores\",\"{{Rank\")",
        f"{user_buttons}",
        f"#font(BC12,BC12,BC12)",
        f"#stbl[%TBL](%BB[x:154,y:42+18,w:559,h:270],{{}},7,0,7,1,21,1,25,1,6,1,15,1,7,1,19,1,",
        f"{user_list}",
        f")",
        f"#font(RC12,R2C12,RC12)",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%BT](%BB[x:641,y:377,w:100,h:305],{{GW|open&users_list.dcml\\00&page={page + 1}^order={order}^resort=\\00|LW_lockall}},\"Next\")" if len(
            players) > 13 else '',
        f"<NGDLG>",
        f"<NGDLG>",
        f"#block(cancel.cml,CAN)<NGDLG>",
        f"<NGDLG>",
        f"#end(CAN)"
    ))


@alexander.route('voting_view.dcml')
def voting_view(**kwargs) -> str:
    output = []
    with alexander.engine.connect() as connection:
        votings = connection.execute(text(f"SELECT id, subject, published_at FROM votes;")).fetchall()
        n = None
        for idx, voting in enumerate(votings):
            output.append(
                f'#font(R2C12,R2C12,RC12)\
                #rtxt[%DATE{idx}](%SB[x:100%-210,y:{25 - 20 if not output else f"%ANS{idx - 1}_{n}+40-20"},w:200,h:20],{{}},"Published {voting[2].strftime("%m.%d.%Y") if type(voting[2]) == datetime else voting[2]}")\
                #font(GC14,R2C14,RC14)\
                #ctxt[%ANS{idx}_0](%SB[x:5,y:{25 - 3 if not output else f"%ANS{idx - 1}_{n}+40-3"},w:100%-10,h:20],{{}},"{voting[1]}")\
                #font(BC12,R2C12,RC12)')
            n = 0
            answers = connection.execute(
                text(f"SELECT text, votes FROM vote_answers WHERE vote_id = {voting[0]} LIMIT 4;")).fetchall()
            for idy, answer in enumerate(answers):
                n = idy + 1
                output.append(
                    f'#txt[%ANS{idx}_{idy + 1}](%SB[x:10,y:%ANS{idx}_{idy},w:100%-30,h:20],{{}},"- {answer[0]}")\
                    #rtxt[%RES{idx}_{idy + 1}](%SB[x:100%-110,y:%ANS{idx}_{idy},w:100,h:20],{{}},"{answer[1]}")')
            output.append(f'#pan[%HPAN{idx}](%SB[x:0-32,y:%ANS{idx}_{n}+40,w:100%+65,h:0],9)')
    output = "".join(output)
    return " ".join((
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
        f"#font(RG18,RG18,RG18)",
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")",
        f"#font(BG18,BG18,BG18)",
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")",
        f"#font(R2C12,R2C12,R2C12)",
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
        f"#font(RC12,RC12,RC12)",
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
        f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")",
        f"#hint(%BT1,\"News, events, forum and punishment list\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
        f"#hint(%BT2,\"Player list, personal mail and clan information\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")",
        f"#hint(%BT4,\"Play custom games\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
        f"#hint(%BT5,\"Played games and their scores\")",
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)",
        f"<VOTING>",
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)",
        f"<VOTING>",
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
        f"#font(RC14,R2C14,RC14)",
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")",
        f"#font(RC14,GC14,RC14)",
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&voting_view.dcml\\00|LW_lockall}},\"{{View votes}}\")",
        f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)",
        f"#sbox[%SB](x:150,y:42+4,w:526+4,h:291-8)",
        f"{output}",
        f"#font(R2C14,R2C14,RC14)",
        f"#ctxt[%LIST5](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")",
        f"#hint(%LIST5,\"List of punished players\")",
        f"#edit[%E_FT](%B[x:0,y:0,w:0,h:0],{{%GV_FORUM_LAST_TIME}})",
        f"#ctxt[%LIST6](%B[x:0,y:%LIST5-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=<%GV_FORUM_LAST_TIME>\\00|LW_lockall}},\"{{Forum}}\")",
        f"#hint(%LIST6,\"Read and write forum messages\")",
        f"<NGDLG>",
        f"<NGDLG>",
        f"#block(cancel.cml,CAN)<NGDLG>",
        f"<NGDLG>",
        f"#end(CAN)"))


# TODO: HANDLE THE ACTUAL VOTING
@alexander.route('voting.dcml')
def voting(variables: dict, **kwargs) -> str:
    with alexander.engine.connect() as connection:
        question = variables.get("question")
        answer = variables.get("answer")
        latest_vote = connection.execute(text("SELECT votes.id, votes.subject\
                        FROM votes ORDER BY id DESC LIMIT 1")).fetchone()
        if latest_vote:
            answers = connection.execute(text(f"SELECT vote_answers.id, vote_answers.text, vote_answers.votes\
                            FROM vote_answers WHERE vote_answers.vote_id = '{latest_vote[0]}' LIMIT 4")).fetchall()
            return " ".join((
                f"<VOTING>",
                f"#font(GC12,R2C12,RC12)",
                f"#txt[%ANS0](%B_VOTE[x:5,y:3,w:100%-10,h:14],{{}},\"{latest_vote[1]}\")",
                "".join([
                    f'#apan[%PAN{idx + 1}](%B_VOTE[x:0-3,y:%ANS0+{idx * 14},w:100%-4,h:13],{{GW|open&voting.dcml\\00&question={latest_vote[0]}^answer={answer[0]}\\00|LW_lockall}},14,\"\")\
                #font(R2C12,R2C12,RC12)\
                #txt[%ANS{idx + 1}](%B_VOTE[x:0,y:%ANS0+{idx * 14}+1,w:100%,h:20],{{}},\"{idx + 1}. {answer[1]} \")\
                #ctxt[%RES{idx + 1}](%B_VOTE[x:105,y:%ANS0+{idx * 14}+1,w:40,h:20],{{}},\"{answer[2]}\")'
                    for idx, answer in enumerate(answers)]),
                "#font(RC12,R2C12,RC12)",
                "#txt[%VIEW](%B_VOTE[x:5,y:100%-17,w:100%,h:20],{GW|open&voting_view.dcml\\00|LW_lockall},\"{View all votes}\")",
                f"<VOTING>"
            ))
        else:
            return (
                f"<VOTING>"
                f"#font(RG18,RG18,RG18)"
                f"#ctxt[%T0](%B_VOTE[x:5,y:20,w:100%-10,h:20],{{}},\"No search results\")"
                f"#font(R2C12,R2C12,RC12)"
                f"#ctxt[%VIEW](%B_VOTE[x:4,y:100%-19,w:100%-5,h:20],{{GW|open&voting_view.dcml\\00|LW_lockall}},\"{{View all votes}}\") "
                f"<VOTING>"
            )


def LW_time(time: str | int, url: str) -> list:
    return ['LW_time', time, f'open:{url}']


def LW_show(content: str) -> list:
    return ['LW_show', content]


def command_open(parameters: list[bytes], player_id: str | int) -> str:
    filename = parameters[0].decode()
    variables = defaultdict(lambda: '')
    if len(parameters) > 1:
        variable_string = parameters[1].decode()
        extract_variables(variables, variable_string)
    return alexander.route_map.get(filename, cancel)(variables=variables, player_id=player_id)


def command_login(parameters: list[bytes], database: Engine) -> str:
    lgd = parameters[0].decode()
    if lgd:
        with alexander.engine.connect() as connection:
            profileid = connection.execute(text(f"SELECT player_id "
                                                f"FROM sessions "
                                                f"WHERE session_key = '{lgd}' "
                                                f"LIMIT 1")).fetchone()
            if profileid:
                profileid = profileid._mapping
                profile = connection.execute(text(
                    f"CALL get_profile({profileid.player_id})"
                )).fetchone()
                if profile:
                    return (
                        f"#ebox[%EBG](x:0,y:0,w:1024,h:768)"
                        f"#edit[%E_AC](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_ACCOUNTS}})"
                        f"#edit[%E_CUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_CLANS_LAST_UPDATE}})"
                        f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})"
                        f"#edit[%E_AC2](%EBG[x:0,y:0,w:0,h:0],{{%GV_VE_AC}})"
                        f"#edit[%E_AC2](%EBG[x:0,y:0,w:0,h:0],{{%GV_LGD}})"
                        f"#exec(LW_cfile&&Cookies/%GV_VE_AC)"
                        f"#exec(LW_time&10&l_games_btn.cml\\00)"
                        f"#block(l_games_btn.cml,l_g):GW|open&log_conf_dlg.dcml\\00&logs=true^last_update"
                        f"=<%GV_LAST_UPDATE>"
                        f"^accounts=<%GV_VE_ACCOUNTS>"
                        f"^VE_PROF={profile.player_id}"
                        f"^VE_NAME={profile.name}"
                        f"^VE_NICK={profile.nick}"
                        f"^VE_MAIL={profile.mail}"
                        f"^VE_PASS={profile.password}"
                        f"^VE_ICQ={profile.icq}"
                        f"^VE_HOMP={profile.site}"
                        f"^VE_SEX={profile.sex}"
                        f"^VE_CNTRY={profile.country}"
                        f"^VE_PHON={profile.phone}"
                        f"^VE_BIRTH={profile.birthday}\\00|LW_lockall"
                        f"#end(l_g)"
                    )
    return (
        f"#ebox[%EBG](x:0,y:0,w:1024,h:768)"
        f"#edit[%E_LUP](%EBG[x:0,y:0,w:0,h:0],{{%GV_LAST_UPDATE}})"
        f"#exec(LW_time&10&l_games_btn.cml\\00)"
        f"#block(l_games_btn.cml,l_g):GW|open&log_new_form.dcml\\00&logs=2^VE_MODE=creat^last_update=<%GV_LAST_UPDATE"
        f">\\00|LW_lockall"
        f"#end(l_g)"
    )


def command_url(parameters: list[bytes]) -> str:
    return parameters[0].decode()


def command_alive(parameters: list[bytes], database: Engine) -> None:
    data = bytearray(parameters[0])
    data.extend(b'\x00' * (4 - len(data) % 4))
    values = []
    for n in range(0, len(data) // 4):
        src = data[n * 4:n * 4 + 4]
        values.append(unpack('<I', src)[0])
    reported_player_count, host_id = values[0], values[1]
    with alexander.engine.connect() as connection:
        connection.execute(text(
            f"UPDATE lobbies SET players = '{reported_player_count}' WHERE host_id = {host_id}"
        ))
        connection.commit()


def command_leave(player_id: str | int) -> None:
    with alexander.engine.connect() as connection:
        connection.execute(text(f"DELETE FROM lobbies WHERE host_id={player_id};"))
        connection.commit()


def command_setipaddr(lobby_id: str, address: str) -> None:
    with alexander.engine.connect() as connection:
        connection.execute(text(f"UPDATE lobbies SET ip = '{address}' WHERE id = {lobby_id}"))
        connection.commit()


def view_message(button_1: str = "LW_file&Internet/Cash/l_games_btn.cml", button_2: str = "LW_file&Internet/Cash/l_games_btn.cml", title: str = "ERROR", message: str = "INTERNAL SERVER ERROR") -> str:
    return (
            f"<MESDLG>"
            f"#ebox[%MBG](x:0,y:0,w:1024,h:768)"
            f"#def_dtbl_button_hotkey(13,27)"
            f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{button_1}{button_2},2,0,3,13,252,\"{title}\",\"{mysql_error_messages[message]}\",26,\"Edit\",\"Cancel\")"
            f"<MESDLG>"
            )


def process_request(request, **kwargs) -> list:
    print(request)
    command, parameters, player_id = request[0], request[1:-2], request[-1].decode()
    response = []

    if command == "setipaddr":
        command_setipaddr(request[1].decode(), request[2].decode().split(':')[0])

    elif command == "leave":
        command_leave(player_id)

    elif command == "start":
        pass

    elif command == "url":
        response.append(LW_time(0, command_url(parameters)))

    elif command == "gmalive":
        pass

    elif command == "stats":
        pass

    elif command == "setclan":
        print("SIGNATURE ", parameters)
        # signature = parameters[]
        pass

    elif command == "endgame":
        pass

    elif command == "alive":
        command_alive(parameters, alexander.engine)

    elif command == "login":
        response.append(LW_show(command_login(parameters, alexander.engine)))

    elif command == "open":
        try:
            result = command_open(parameters, player_id)
            response.append(LW_show(result))

        except Exception as exception:
            print(exception)
            response.append(LW_show(
                    f'<MESDLG> '
                    f'#ebox[%D](x:0,y:0,w:1024,h:768) '
                    f'#def_dtbl_button_hotkey(13,27) '
                    f'#table[%TBL](%D[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&{parameters[0].decode()}\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,"CRITICAL ERROR","Server error occurred while processing your request! Press Try Again button to attempt process request again. Press Cancel to exit",26,"Try Again","Cancel") '
                    f'<MESDLG> '
                ))

    return response
