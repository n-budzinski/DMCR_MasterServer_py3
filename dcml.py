from __future__ import annotations
import config
import classes
import common
from datetime import datetime

def _ebox(id, posX, posY, width, height) -> str:
    return f"#ebox[%{id}](x:{posX},y:{posY},w:{width},h:{height})"


def _pix(id, parentID, posX, posY, width, height, element, a, b, c, d) -> str:
    return f"#pix[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{}},{element},{a},{b},{c},{d})"


def _exec(cmd, execs: dict) -> str:
    e = [cmd]
    for key, value in execs.items():
        e.append(f"{str(key)+'&'+str(value) if(value is not None) else key}")
    return f"#exec({'&'.join(e)})"


def _font(a, b, c):
    return f"#font({a},{b},{c})"


def _def_panel(a, element, b, c, d, e, f, g, h, i, j, k):
    return f"#def_panel({a},{element},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k})"


def _pan(id, parentID, x, y, width, height, a):
    return f"#pan[%{id}](%{parentID}[x:{x},y:{y},w:{width},h:{height}],{a})"


def _apan(id, parentID, x, y, width, height, command, a, text):
    return f"#apan[%{id}](%{parentID}[x:{x},y:{y},w:{width},h:{height}],{{{command}}},{a},\"{text}\")"


def _ctxt(id, parentID, posX, posY, width, height, command, text):
    return f"#ctxt[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{{command}}},\"{text}\")"


def _def_gp_btn(element, a, b, c, d):
    return f"#def_gp_btn({element},{a},{b},{c},{d})"


def _gpbtn(id, parentID, posX, posY, width, height, command, text):
    return f"#gpbtn[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{{command}}},\"{text}\")"


def _txt(id, parentID, posX, posY, width, height, command, text):
    return f"#txt[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{{command}}},\"{text}\")"


def _edit(id, parentID, posX, posY, width, height, command, text):
    return f"#edit[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{{command}}},\"{text}\")"


def _block(a, b):
    return f"#block({a},{b})"


def _end(a) -> str:
    return f"#end({a})"


def _hint(parentID, text):
    return f"#hint(%{parentID},\"{text}\")"


def _voting() -> str:
    return "<VOTING>"


def _ngdlg() -> str:
    return "<NGDLG>"


class Table:
    @staticmethod
    def single(id,
               parentID,
               posX,
               posY,
               width,
               height,
               onTitleClick,
               onBodyClick,
               onLeftButton,
               windowID,
               b,
               ornamentID,
               backgroundID,
               titleWidth,
               title,
               body,
               buttonSpacing,
               leftButtonText,
               ) -> str:

        return f"#table[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{{onTitleClick}}}{{{onBodyClick}}}{{{onLeftButton}}},{windowID},{b},{ornamentID},{backgroundID},{titleWidth},\"{title}\",\"{body}\",{buttonSpacing},\"{leftButtonText}\")"

    @staticmethod
    def double(id,
               parentID,
               posX,
               posY,
               width,
               height,
               onTitleClick,
               onBodyClick,
               onLeftButton,
               onRightButton,
               windowID,
               b,
               ornamentID,
               backgroundID,
               titleWidth,
               title,
               body,
               buttonSpacing,
               leftButtonText,
               rightButtonText) -> str:

        return f"#table[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{{onTitleClick}}}{{{onBodyClick}}}{{{onLeftButton}}}{{{onRightButton}}},{windowID},{b},{ornamentID},{backgroundID},{titleWidth},\"{title}\",\"{body}\",{buttonSpacing},\"{leftButtonText}\",\"{rightButtonText}\")"


def _table(id, parentID, posX, posY, width, height, onTitleClick, onBodyClick, onLeftButton, onRightButton, type, b, ornamentID, backgroundID, titleWidth, title, body, buttonSpacing, leftButtonText, rightButtonText) -> str:
    return f"#table[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{{onTitleClick}}}{{{onBodyClick}}}{{{onLeftButton}}}{{{onRightButton}}},{type},{b},{ornamentID},{backgroundID},{titleWidth},\"{title}\",\"{body}\",{buttonSpacing},\"{leftButtonText}\",\"{rightButtonText}\")"


def _mesdlg() -> str:
    return "<MESDLG>"


def logUser(gameManager, options, player) -> str:
    from common import checkAlpha
    gameManager.leaveLobby(player)
    player.nickname = options.get("VE_NICK")
    if len(player.nickname) >= 3:
        return "\n".join((
            f"<MESDLG>",
            f"#ebox[%MBG](x:0,y:0,w:1024,h:768)",
            f"#pix[%PX1](%MBG[x:0,y:0,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
            f"#exec(LW_key&{player.sessionID})",
            f"#exec(LW_gvar&"\
            f"%PROF&{player.sessionID}&"\
            f"%NAME&n/a&"\
            f"%NICK&{player.nickname}&"\
            f"%MAIL&n/a&"\
            f"%PASS&DEMO&"\
            f"%GMID&XXXX-XXXX-XXXX-DEMO&"\
            f"%CHAT&{config.IRCADDRESS}&"\
            f"%CHNL1&{config.IRCCH1}\\00&"\
            f"%CHNL2&{config.IRCCH2}\\00)",
            f"<MESDLG>",
        ))

    else:
        return mesError("ERROR", "Your nickname has to be longer than 3 characters!")

# player, options, gamemanager


def login() -> str:
    return "\n".join((
        f"#ebox[%TB](x:0,y:0,w:1024,h:768)",
        f"#exec(LW_enbbox&0&%L0)",
        f"#exec(LW_enbbox&0&%B)",
        f"#exec(LW_enbbox&0&%FLBOX)",
        f"#exec(LW_enbbox&0&%BP)",
        f"#exec(LW_enbbox&0&%L)",
        f"#exec(LW_enbbox&0&%BB)",
        f"#exec(LW_enbbox&0&%B1)",
        f"#exec(LW_enbbox&0&%BG)",
        f"#exec(LW_enbbox&0&%B2)",
        f"#exec(LW_enbbox&0&%BPANEL)",
        f"#exec(LW_enbbox&0&%BPANEL2)",
        f"#exec(LW_enbbox&0&%TB)",
        f"#exec(LW_enbbox&0&%B_VOTE)",
        f"#exec(LW_enbbox&0&%MBG)",
        f"#exec(LW_enbbox&0&%B0)",
        f"#exec(LW_enbbox&0&%M)",
        f"#exec(LW_enbbox&0&%LB)",
        f"#exec(LW_enbbox&0&%MB)",
        f"#exec(LW_enbbox&0&%EBG)",
        f"#exec(LW_enbbox&0&%LBX)",
        f"#exec(LW_enbbox&0&%BARDLD)",
        f"#exec(LW_enbbox&0&%BF2)",
        f"#exec(LW_enbbox&0&%B01)",
        f"#exec(LW_enbbox&0&%BF)",
        f"#exec(LW_enbbox&0&%BTABLE2)",
        f"#exec(LW_enbbox&0&%SB)",
        f"#ebox[%BTABLE](x:0,y:0,w:100%,h:100%)",
        f"#font(BC12,BC12,BC12)",
        f"#def_panel(11,Interf3/elements/b02,-1,-1,-1,-1,-1,-1,-1,-1,8,8)",
        f"#pan[%MPNT](%BTABLE[x:251,y:308,w:523,h:240],11)",
        f"#def_panel(11,Interf3/elements/b02,-1,-1,14,15,4,5,11,16,-1,-1)",
        f"#pan[%MPN](%BTABLE[x:251,y:308+4,w:523,h:240-4],11)",
        f"#pix[%PXT1](%BTABLE[x:251-208,y:308-189,w:50,h:70],{{}},Interf3/elements/b02,18,18,18,18)",
        f"#pix[%PXT2](%BTABLE[x:566,y:308-189,w:50,h:70],{{}},Interf3/elements/b02,19,19,19,19)",
        f"#pix[%PX2](%BTABLE[x:617+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX3](%BTABLE[x:347+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX4](%BTABLE[x:397+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX5](%BTABLE[x:447+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX6](%BTABLE[x:497+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX7](%BTABLE[x:547+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX8](%BTABLE[x:597+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX0](%BTABLE[x:342,y:308-5,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)",
        f"#pix[%PX1](%BTABLE[x:672,y:308-5,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)",
        f"#font(BG18,BG18,RG18)",
        f"#ctxt[%TTEXT](%BTABLE[x:251+2,y:308+4,w:523,h:20],{{0}},\"{config.SERVERNAME}\")",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#font(WG14,BG14,WG14)",
        f"#gpbtn[%PXBT](%BTABLE[x:348-433,y:517-16,w:100%,h:70],{{GW|open&log_user.dcml\\00&VE_NICK=<%GV_VE_NICK>\\00|LW_lockall}},\"Login\")",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#font(WG14,BG14,WG14)",
        f"#gpbtn[%PXBT](%BTABLE[x:519-433,y:517-16,w:100%,h:70],{{LW_key&#CANCEL}},\"Cancel\")",
        f"#ebox[%LBX](x:270,y:310,w:500,h:220)",
        f"#pix[%PX1](%LBX[x:2,y:54,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)",
        f"#font(BC14,BC14,BC14)",
        f"#txt[%L_NICK](%LBX[x:74,y:115,w:100%,h:20],{{}},\"Nickname\")",
        f"#pan[%P_NICK](%LBX[x:167,y:115,w:238,h:14],1)",
        f"#edit[%E_NICK](%LBX[x:172,y:112,w:232,h:18],{{%GV_VE_NICK}},\"Player\")",
        f"#pix[%PX2](%LBX[x:4,y:157,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)",
        f"<NEWDLG>",
        f"<NEWDLG>",
        f"<MESDLG>",
        f"<MESDLG>",
        f"#block(newdlg.cml,CAN)",
        f"<MESDLG>",
        f"<MESDLG>",
        f"<NEWDLG>",
        f"<NEWDLG>",
        f"#end(CAN)",
        f"#hint(%L_NICK,\"Enter your nickname\")",
        f"#hint(%Login,\"Join the server\")",
    ))


def voting(options: dict):
    question = options.get("question")
    answer = options.get("answer")
    return "".join((
        f"<VOTING>",
        f"#font(GC12,R2C12,RC12)",
        f"#txt[%ANS0](%B_VOTE[x:5,y:3,w:100%-10,h:14],{{}},\"Top donations: \")",
        f"#apan[%PAN1](%B_VOTE[x:0-3,y:%ANS0+0+10,w:100%-4,h:13],{{GW|open&voting.dcml\\00&question=32^answer=65\\00|LW_lockall}},14,\"\")",
        f"#font(R2C12,R2C12,RC12)",
        f"#txt[%ANS1](%B_VOTE[x:0,y:%ANS0+0+11,w:100%,h:20],{{}},\"1. - \")",
        f"#ctxt[%RES1](%B_VOTE[x:105,y:%ANS0+0+11,w:40,h:20],{{}},\"0\")",
        f"#apan[%PAN2](%B_VOTE[x:0-3,y:%ANS0+14+10,w:100%-4,h:13],{{GW|open&voting.dcml\\00&question=32^answer=62\\00|LW_lockall}},14,\"\")",
        f"#font(R2C12,R2C12,RC12)",
        f"#txt[%ANS2](%B_VOTE[x:0,y:%ANS0+14+11,w:100%,h:20],{{}},\"2. - \")",
        f"#ctxt[%RES2](%B_VOTE[x:105,y:%ANS0+14+11,w:40,h:20],{{}},\"0\")",
        f"#apan[%PAN3](%B_VOTE[x:0-3,y:%ANS0+28+10,w:100%-4,h:13],{{GW|open&voting.dcml\\00&question=32^answer=63\\00|LW_lockall}},14,\"\")",
        f"#font(R2C12,R2C12,RC12)",
        f"#txt[%ANS3](%B_VOTE[x:0,y:%ANS0+28+11,w:100%,h:20],{{}},\"3. - \")",
        f"#ctxt[%RES3](%B_VOTE[x:105,y:%ANS0+28+11,w:40,h:20],{{}},\"0\")",
        f"#apan[%PAN4](%B_VOTE[x:0-3,y:%ANS0+42+10,w:100%-4,h:13],{{GW|open&voting.dcml\\00&question=32^answer=64\\00|LW_lockall}},14,\"\")",
        f"#font(R2C12,R2C12,RC12)",
        f"#txt[%ANS4](%B_VOTE[x:0,y:%ANS0+42+11,w:100%,h:20],{{}},\"4. - \")",
        f"#ctxt[%RES4](%B_VOTE[x:105,y:%ANS0+42+11,w:40,h:20],{{}},\"0\")",
        f"<VOTING>",
    ))

def mesError(title: str, description: str):
    return "".join((
        f"<NEWDLG>",
        f"#ebox[%MBG](x:0,y:0,w:1024,h:768)",
        f"#pix[%PX1](%MBG[x:0,y:0,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
        f"#exec(LW_enbbox&0&%L0)",
        f"#exec(LW_enbbox&0&%B)",
        f"#exec(LW_enbbox&0&%FLBOX)",
        f"#exec(LW_enbbox&0&%BP)",
        f"#exec(LW_enbbox&0&%L)",
        f"#exec(LW_enbbox&0&%BB)",
        f"#exec(LW_enbbox&0&%B1)",
        f"#exec(LW_enbbox&0&%BG)",
        f"#exec(LW_enbbox&0&%B2)",
        f"#exec(LW_enbbox&0&%BPANEL)",
        f"#exec(LW_enbbox&0&%BPANEL2)",
        f"#exec(LW_enbbox&0&%TB)",
        f"#exec(LW_enbbox&0&%B_VOTE)",
        f"#exec(LW_enbbox&0&%MBG)",
        f"#exec(LW_enbbox&0&%B0)",
        f"#exec(LW_enbbox&0&%M)",
        f"#exec(LW_enbbox&0&%LB)",
        f"#exec(LW_enbbox&0&%MB)",
        f"#exec(LW_enbbox&0&%EBG)",
        f"#exec(LW_enbbox&0&%LBX)",
        f"#exec(LW_enbbox&0&%BARDLD)",
        f"#exec(LW_enbbox&0&%BF2)",
        f"#exec(LW_enbbox&0&%B01)",
        f"#exec(LW_enbbox&0&%BF)",
        f"#exec(LW_enbbox&0&%BTABLE)",
        f"#exec(LW_enbbox&0&%SB)",
        f"#ebox[%BTABLE2](x:0,y:0,w:100%,h:100%)",
        f"#font(BC12,BC12,BC12)",
        f"#def_panel(11,Interf3/elements/b02,21,20,14,15,4,5,12,16,8,8)",
        f"#pan[%MPN](%BTABLE2[x:306,y:310+15,w:415,h:220-15],11)",
        f"#pix[%PXP1](%BTABLE2[x:306+20,y:310+20,w:100%,h:100%],{{}},Internet/pix/i_pri0,32,32,32,32)",
        f"#pix[%PX2](%BTABLE2[x:576,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX3](%BTABLE2[x:401,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX4](%BTABLE2[x:451,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX5](%BTABLE2[x:501,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX6](%BTABLE2[x:551,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX0](%BTABLE2[x:391,y:310-10,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)",
        f"#pix[%PX1](%BTABLE2[x:626,y:310-10,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)",
        f"#font(BG18,BG18,RG18)",
        f"#ctxt[%TTEXT](%BTABLE2[x:306,y:310-1,w:415,h:20],{{0}},\"{title}\")",
        f"#font(BC12,RC12,RC12)",
        f"#ctxt[%MTXT0](%BTABLE2[x:306+20,y:310+22,w:415-40,h:20],{{}},\"{description}\")",
        f"#exec(LW_vis&0&%MTXT0)",
        f"#ctxt[%MTXT](%BTABLE2[x:306+20,yc:420-3,w:415-40,h:%MTXT0-310-23],{{}},\"{description}\")",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#font(WG14,BG14,WG14)",
        f"#gpbtn[%PXBT2](%BTABLE2[x:0,y:499-16,w:100%,h:70],{{GW|open&demologin.dcml\\00}},\"OK\")",
        f"<NEWDLG>",
    ))

def newGameDlg(player: classes.Player):
    return "".join((
        f"<NGDLG>",
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)",
        f"#exec(LW_cfile&{player.nickname}\\00&Bastet/%GV_VE_TITLE)",
        f"#exec(LW_cfile&\\00&Bastet/%GV_VE_PASSWD)",
        f"#exec(LW_cfile&\\00&Bastet/%GV_VE_MAX_PL)",
        f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&new_game_dlg_create.dcml\\00&max_players=<%GV_VE_MAX_PL>^type=<%GV_VE_TYPE>^password=<%GV_VE_PASSWD>^title=<%GV_VE_TITLE>\\00|LW_lockall}}{{GW|open&cancel.dcml\\00|LW_lockall}},1,0,13,252,\"CREATE NEW GAME\",,26,\"Create\",\"Cancel\")",
        f"#ebox[%L](x:245,y:100,w:450,h:210)",
        f"#font(BC12,RC12,RC12)",
        f"#txt[%L_NAME](%L[x:11,y:48,w:160,h:20],{{}},\"Game Title:\")",
        f"#pan[%P_NAME](%L[x:15,y:68,w:382,h:14],1)",
        f"#font(BC12,GC12,GC12)",
        f"#edit[%E_NAME](%L[x:19,y:67,w:377,h:18],{{%GV_VE_TITLE}},0,0,0,1)",
        f"#font(BC12,RC12,RC12)",
        f"#txt[%L_PASS](%L[x:11,y:95,w:160,h:20],{{}},\"Password:\")",
        f"#pan[%P_PASS](%L[x:15,y:114,w:382,h:14],1)",
        f"#font(BC12,GC12,GC12)",
        f"#edit[%E_PASS](%L[x:19,y:113,w:377,h:18],{{%GV_VE_PASSWD}},0,0,1)",
        f"#font(BC14,RC14,RC14)",
        f"#txt[%L_MAXPL](%L[x:11,y:145,w:150,h:24],{{}},\"Max Players:\")",
        f"#cbb[%E_MAXPL](%L[x:130,y:139,w:273,h:24],{{%GV_VE_MAX_PL}},2,3,4,5,6,7,0)",
        f"#font(BC14,RC14,RC14)",
        f"#txt[%L_MAXPL](%L[x:11,y:175,w:151,h:24],{{}},\"Type:\")",
        f"""#cbb[%E_TYPE](%L[x:130,y:169,w:273,h:24],{{%GV_VE_TYPE}},{''.join([f'{_type.name},' for _type in classes.GameTypes.types])},0)""",
        f"{''.join([f'{_type.name},' for _type in classes.GameTypes.types])}"
        f"<NGDLG>",
    ))


def createGame(host: classes.Player, options: dict, gamemanager: classes.GameManager):
    lobbyID = gamemanager.createLobby(
        host=host,
        maxPlayers=int(options['max_players'])+2,
        password=options['password'],
        gameTitle=options['title'],
        gameType=classes.getGameType(int(options.get("type", 0)))
    )
    maxPlayers = options.get('max_players', )
    gameTitle = options.get('title')
    return "".join((
        f"<NGDLG>",
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)",
        f"#exec(LW_file&Internet/Cash/cancel.cml|LW_gvar&%GOPT&/OPT00 /OPT10 /OPT20 /OPT30 /OPT60 /PAGE2 /NOCOMP&%CG_GAMEID&{lobbyID}&%CG_MAXPL&{maxPlayers}&%CG_GAMENAME&\"{gameTitle}\"&%COMMAND&CGAME)",
        f"<NGDLG>",
    ))


def joinGame(player: classes.Player, options, gamemanager: classes.GameManager):
    lobby = gamemanager.getLobby(options.get("id_room", "_"))
    if lobby:
        if lobby.isFull():
            return common.getFile("lobby_full.dcml")
        elif lobby.host.sessionID == player.sessionID:
            return common.getFile("join_game_own.dcml")\
                .replace("LOBBY_ID", options["id_room"])
        else:
            if lobby.password:
                if options.get("password", "") == "":
                    return common.getFile("password_prompt.dcml")\
                        .replace("LOBBYID", options["id_room"])
                elif options.get("password", "") != lobby.password:
                    return common.getFile("incorrect_password.dcml")
            gamemanager.joinLobby(lobby, player)
            return common.getFile("join_game.dcml")\
                .replace("LOBBYID", options["id_room"])\
                .replace("MAXPLAYERS", str(lobby.maxPlayers))\
                .replace("GAMEHOST", lobby.host.nickname)\
                .replace("IPADDR", lobby.ipAddress[0])\
                .replace("PORT", str(config.TCPPORT))
    return common.getFile("join_game_incorrect.dcml").replace("LOBBY_ID", options["id_room"])


def lobbyFull():
    return "".join((
        f"<NGDLG>",
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%)",
        f"#pix[%PX1](%L0[x:0-62,y:0-136,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
        f"#exec(LW_enbbox&0&%L0)",
        f"#exec(LW_enbbox&0&%B)",
        f"#exec(LW_enbbox&0&%FLBOX)",
        f"#exec(LW_enbbox&0&%BP)",
        f"#exec(LW_enbbox&0&%L)",
        f"#exec(LW_enbbox&0&%BB)",
        f"#exec(LW_enbbox&0&%B1)",
        f"#exec(LW_enbbox&0&%BG)",
        f"#exec(LW_enbbox&0&%B2)",
        f"#exec(LW_enbbox&0&%BPANEL)",
        f"#exec(LW_enbbox&0&%BPANEL2)",
        f"#exec(LW_enbbox&0&%TB)",
        f"#exec(LW_enbbox&0&%B_VOTE)",
        f"#exec(LW_enbbox&0&%MBG)",
        f"#exec(LW_enbbox&0&%B0)",
        f"#exec(LW_enbbox&0&%M)",
        f"#exec(LW_enbbox&0&%LB)",
        f"#exec(LW_enbbox&0&%MB)",
        f"#exec(LW_enbbox&0&%EBG)",
        f"#exec(LW_enbbox&0&%LBX)",
        f"#exec(LW_enbbox&0&%BARDLD)",
        f"#exec(LW_enbbox&0&%BF2)",
        f"#exec(LW_enbbox&0&%B01)",
        f"#exec(LW_enbbox&0&%BF)",
        f"#exec(LW_enbbox&0&%BTABLE2)",
        f"#exec(LW_enbbox&0&%SB)",
        f"#ebox[%BTABLE](x:0,y:0,w:100%,h:100%)",
        f"#font(BC12,BC12,BC12)",
        f"#def_panel(11,Interf3/elements/b02,21,20,14,15,4,5,12,16,8,8)",
        f"#pan[%MPN](%BTABLE[x:242,y:115+15,w:415,h:220-15],11)",
        f"#pix[%PXP1](%BTABLE[x:242+20,y:115+20,w:100%,h:100%],{{}},Internet/pix/i_pri0,32,32,32,32)",
        f"#pix[%PX2](%BTABLE[x:522,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX3](%BTABLE[x:327,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX4](%BTABLE[x:377,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX5](%BTABLE[x:427,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX6](%BTABLE[x:477,y:115-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX0](%BTABLE[x:317,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)",
        f"#pix[%PX1](%BTABLE[x:572,y:115-10,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)",
        f"#font(BG18,BG18,RG18)",
        f"#ctxt[%TTEXT](%BTABLE[x:242,y:115-1,w:415,h:20],{{0}},\"ERROR\")",
        f"#font(BC12,RC12,RC12)",
        f"#ctxt[%MTEXT0](%BTABLE[x:242+20,y:115+22,w:415-40,h:20],{{}},\"This lobby is full\")",
        f"#exec(LW_vis&0&%MTEXT0)",
        f"#ctxt[%MTEXT](%BTABLE[x:242+20,yc:225-3,w:415-40,h:%MTEXT0-115-159],{{}},\"This lobby is full\")",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#font(WG14,BG14,WG14)",
        f"#gpbtn[%PXBT](%BTABLE[x:520-433,y:303-16,w:100%,h:70],{{GW|open&cancel.dcml\\00|LW_lockall}},\"OK\")",
        f"<NGDLG>",
    ))


def dbtbl(gamemanager: classes.GameManager, player: classes.Player):
    lobbies = gamemanager.getLobbies(player.lobbySorting, player.lobbyResort)
    return "".join((
        f"<DBTBL>",
        f"#exec(LW_time&15000&l_games_btn.cml\\00)",
        f"#block(l_games_btn.cml,l_g):GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall",
        f"#end(l_g)",
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%)",
        f"#font(R2C12,R2C12,RC12)",
        f"#stbl[%TBL](%BB[x:154,y:42,w:523,h:291],{{GW|open&dbtbl.dcml\\00&order=r.title^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=u.nick^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=t.name^resort=\\00|LW_lockall}}{{}}{{}},5,7,33,1,25,1,14,1,14,1,14,1,20,\"{{Game Title\",\"{{Host\",\"{{Type\",\"Players\",\"Ping\")",
        f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-21,25)",
        f"#sbox[%SB](x:150,y:60,w:526+4,h:271)",
        f"#font(RC12,RC12,RC12)",
        f"#txt[%PL](%TB[x:130,y:10,w:200,h:20],{{}},\"Last update: {datetime.now().strftime('%H:%M:%S')}\")",
        "".join(
        [f"#apan[%APAN{str(idx)}](%SB[x:0,y:{str(idx*21)}-2,w:100%,h:20],"\
        f"#font(BC12,BC12,BC12)"\
        f"{{GW|open&joinGame.dcml\\00&delete_old=true^id_room={str(lid)}\\00|LW_lockall}},8)"\
        f"#ping[%PING{str(idx)}](%SB[x:86%+30,y:{str(idx*21)}+4,w:14,h:20],"\
        f"{common.reverse_address(lobby.ipAddress)})"
            for idx, (lid, lobby) in enumerate(lobbies.items())]),
        f"#font(BC12,BC12,BC12)",
        f"#stbl[%ROOM_LST](%SB[x:4,y:0,w:523,h:42],{{}},5,0,33,0,25,1,14,1,14,1,14,1",
        "".join(
        [f',21,"{lobby.gameTitle + (lambda : "  *password*  " if lobby.password != "" else "")()}",'\
            f'"{lobby.host.nickname}",'\
            f'"{lobby.gameType.name}",'\
            f'"{str(lobby.getPlayerCount())}/{str(lobby.maxPlayers)}",'\
            f'""'
            for _, lobby in lobbies.items()]),
        f")#font(BC14,WC14,BC14)",
        f"#sbtn[%B_J](%BB[x:521,y:377,w:100,h:305],{{GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall}},\"Refresh\")",
        f"#sbtn[%B_CREDITS](%BB[x:50,y:377,w:100,h:305],{{GW|url&https://0x7350.blogspot.com/\\00}},\"Credits\")",
        f"#sbtn[%B_DISCORD](%BB[x:170,y:377,w:100,h:305],{{GW|url&https://discord.gg/7tTAnPnNWG\\00}},\"Discord\")",
        f"#hint(%B_DISCORD,\"Find mates to play with\")",
        f"#sbtn[%B_DONATE](%BB[x:290,y:377,w:100,h:305],{{GW|url&https://paypal.me/NorbertBudzinski\\00}},\"Donate\")",
        f"#hint(%B_DONATE,\"Buy me a coffee\")",
        f"#pix[%I_HEART](%BB[x:358,y:354,w:50%,h:50%],{{}},interf3/custom,0,0,0,0)",
        f"<DBTBL>",
    ))

def startup():
    return "".join((
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
        f"#font(RG18,RG18,RG18)",
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")",
        f"#font(BG18,BG18,BG18)",
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"CUSTOM GAMES\")",
        f"#font(R2C12,R2C12,R2C12)",
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
        f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1) ",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"Lobbies\")",
        # f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1)",
        # f"#font(RC12,R2C12,RC12)",
        # f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")",
        # f"#hint(%BT1,\"News, events, forum and punishment list\")",
        # f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        # f"#font(RC12,R2C12,RC12)",
        # f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
        # f"#hint(%BT2,\"Player list, personal mail and clan information\")",
        # f"#font(RC12,RC12,RC12)",
        # f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
        # f"#gpbtn[%BT4](%TB[x:318,y:22,w:-22,h:-18],{{}},\"Custom Games\")",
        # f"#hint(%BT4,\"Play custom games\")",
        # f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        # f"#font(RC12,R2C12,RC12)",
        # f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
        # f"#hint(%BT5,\"Played games and their scores\")",
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)<VOTING>",
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)<VOTING>",
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
        # f"#font(RC14,GC14,RC14)",
        # f"#ctxt[%TIT1](%B[x:0,y:106,w:146,h:24],{{GW|open&games.dcml\\00|LW_lockall}},\"{{Custom Games}}\")",
        # f"#hint(%TIT1,\"Play custom games\")",
        # f"#ctxt[%LIST33](%B[x:0,y:%TIT1-9,w:146,h:24],{{GW|open&map.dcml\\00|LW_lockall}},\"{{Rating Games}}\")",
        f"#pan[%PAN](%B[x:154,y:42,w:523,h:291],7)",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%B_C](%B[x:641,y:377,w:100,h:305],{{GW|open&new_game_dlg.dcml\\00&delete_old=true\\00|LW_lockall}},\"Create\")<DBTBL>",
        f"#exec(GW|open&dbtbl.dcml\\00)<DBTBL><NGDLG><NGDLG>",
        f"#block(cancel.cml,CAN)<NGDLG><NGDLG>",
        f"#end(CAN)",
    ))

def cancel():
    return "".join((
        f"<NGDLG>",
        f"<NGDLG>"
    ))


def logConfDlg():
    return "".join((
        f"#ebox[%EBG](x:0,y:0,w:1024,h:768)",
        f"#exec(LW_enbbox&0&%L0)",
        f"#exec(LW_enbbox&0&%B)",
        f"#exec(LW_enbbox&0&%FLBOX)",
        f"#exec(LW_enbbox&0&%BP)",
        f"#exec(LW_enbbox&0&%L)",
        f"#exec(LW_enbbox&0&%BB)",
        f"#exec(LW_enbbox&0&%B1)",
        f"#exec(LW_enbbox&0&%BG)",
        f"#exec(LW_enbbox&0&%B2)",
        f"#exec(LW_enbbox&0&%BPANEL)",
        f"#exec(LW_enbbox&0&%BPANEL2)",
        f"#exec(LW_enbbox&0&%TB)",
        f"#exec(LW_enbbox&0&%B_VOTE)",
        f"#exec(LW_enbbox&0&%MBG)",
        f"#exec(LW_enbbox&0&%B0)",
        f"#exec(LW_enbbox&0&%M)",
        f"#exec(LW_enbbox&0&%LB)",
        f"#exec(LW_enbbox&0&%MB)",
        f"#exec(LW_enbbox&0&%EBG)",
        f"#exec(LW_enbbox&0&%LBX)",
        f"#exec(LW_enbbox&0&%BARDLD)",
        f"#exec(LW_enbbox&0&%BF2)",
        f"#exec(LW_enbbox&0&%B01)",
        f"#exec(LW_enbbox&0&%BF)",
        f"#exec(LW_enbbox&0&%BTABLE2)",
        f"#exec(LW_enbbox&0&%SB)",
        f"#ebox[%BTABLE](x:0,y:0,w:100%,h:100%)",
        f"#font(BC12,BC12,BC12)",
        f"#def_panel(11,Interf3/elements/b02,-1,-1,-1,-1,-1,-1,-1,-1,8,8)",
        f"#pan[%MPNT](%BTABLE[x:251,y:308,w:523,h:240],11)",
        f"#def_panel(11,Interf3/elements/b02,-1,-1,14,15,4,5,11,16,-1,-1)",
        f"#pan[%MPN](%BTABLE[x:251,y:308+4,w:523,h:240-4],11)",
        f"#pix[%PXT1](%BTABLE[x:251-208,y:308-189,w:50,h:70],{{}},Interf3/elements/b02,18,18,18,18)",
        f"#pix[%PXT2](%BTABLE[x:566,y:308-189,w:50,h:70],{{}},Interf3/elements/b02,19,19,19,19)",
        f"#pix[%PX2](%BTABLE[x:617+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX3](%BTABLE[x:347+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX4](%BTABLE[x:397+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX5](%BTABLE[x:447+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX6](%BTABLE[x:497+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX7](%BTABLE[x:547+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX8](%BTABLE[x:597+5,y:308-5,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX0](%BTABLE[x:342,y:308-5,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)",
        f"#pix[%PX1](%BTABLE[x:672,y:308-5,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)",
        f"#font(BG18,BG18,RG18)",
        f"#ctxt[%TTEXT](%BTABLE[x:251+2,y:308+4,w:523,h:20],{{0}},\"LOGIN CONFIRMATION\")",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#font(WG14,BG14,WG14)",
        f"#gpbtn[%PXBT](%BTABLE[x:348-433,y:517-16,w:100%,h:70],{{GW|open&log_user.dcml\\00&VE_NICK=<%GV_VE_NICK>\\00|LW_lockall}},\"Login\")",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#font(WG14,BG14,WG14)",
        f"#gpbtn[%PXBT](%BTABLE[x:519-433,y:517-16,w:100%,h:70],{{LW_key&#CANCEL}},\"Cancel\")",
        f"#ebox[%LBX](x:270,y:310,w:500,h:220)",
        f"#pix[%PX1](%LBX[x:2,y:54,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)",
        f"#font(BC14,BC14,BC14)",
        f"#txt[%L_NICK](%LBX[x:74,y:115,w:100%,h:20],{{}},\"Nickname\")",
        f"#pan[%P_NICK](%LBX[x:167,y:115,w:238,h:14],1)",
        f"#edit[%E_NICK](%LBX[x:172,y:112,w:232,h:18],{{%GV_VE_NICK}})",
        f"#pix[%PX2](%LBX[x:4,y:157,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)",
        f"<MESDLG>",
        f"<MESDLG>",
        f"#block(l_games_btn.cml,CAN)<MESDLG>",
        f"<MESDLG>",
        f"#end(CAN)",
        f"#hint(%L_NICK,\"Enter your nickname\")",
        f"#hint(%Login,\"Join the server\")",
    ))



def games():
 return "".join((
    f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
    f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
    f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
    f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
    f"#font(RG18,RG18,RG18)",
    f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")",
    f"#font(BG18,BG18,BG18)",
    f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"CUSTOM GAMES\")",
    f"#font(R2C12,R2C12,R2C12)",
    f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
    f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1) ",
    f"#font(RC12,R2C12,RC12)",
    f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"Lobbies\")",
    # f"#def_gp_btn(Internet/pix/i_pri0,53,53,0,1) ",
    # f"#font(RC12,R2C12,RC12)",
    # f"#gpbtn[%BT1](%TB[x:74,y:23,w:-22,h:-18],{{GW|open&news.dcml\\00|LW_lockall}},\"News & Events\")",
    # f"#hint(%BT1,\"News, events, forum and punishment list\")",
    # f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
    # f"#font(RC12,R2C12,RC12)",
    # f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
    # f"#hint(%BT2,\"Player list, personal mail and clan information\")",
    # f"#font(RC12,RC12,RC12)",
    # f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1) ",
    # f"#gpbtn[%BT4](%TB[x:318,y:22,w:-22,h:-18],{{}},\"Custom Games\")",
    # f"#hint(%BT4,\"Play custom games\")",
    # f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1) ",
    # f"#font(RC12,R2C12,RC12)",
    # f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
    # f"#hint(%BT5,\"Played games and their scores\")",
    f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)<VOTING>",
    f"#exec(GW|open&voting.dcml\\00&question=46\\00)<VOTING>",
    f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
    # f"#font(RC14,GC14,RC14)",
    # f"#ctxt[%TIT1](%B[x:0,y:106,w:146,h:24],{{GW|open&games.dcml\\00|LW_lockall}},\"{{Custom Games}}\")",
    # f"#hint(%TIT1,\"Play custom games\")",
    # f"#ctxt[%LIST33](%B[x:0,y:%TIT1-9,w:146,h:24],{{GW|open&map.dcml\\00|LW_lockall}},\"{{Rating Games}}\")",
    f"#pan[%PAN](%B[x:154,y:42,w:523,h:291],7)",
    f"#font(BC14,WC14,BC14)",
    f"#sbtn[%B_C](%B[x:641,y:377,w:100,h:305],{{GW|open&new_game_dlg.dcml\\00&delete_old=true\\00|LW_lockall}},\"Create\")<DBTBL>",
    f"#exec(GW|open&dbtbl.dcml\\00)<DBTBL><NGDLG><NGDLG>",
    f"#block(cancel.cml,CAN)<NGDLG><NGDLG>",
    f"#end(CAN)",
))
