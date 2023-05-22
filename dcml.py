from __future__ import annotations
import config


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
            f"#exec(LW_cfile&\\00&Cookies/%GV_VE_PASSWD)",
            f"<MESDLG>",
            f"#ebox[%TB](x:0,y:0,w:1024,h:768)",
            f"#pix[%PX1](%TB[x:0,y:0,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
            f"#exec(LW_key&{player.sessionID})",
            f"#exec(LW_gvar&"\
            f"%PROF&{player.sessionID}&"\
            f"%NAME&n/a&"\
            f"%NICK&{player.nickname}&"\
            f"%MAIL&n/a&"\
            f"%PASS&DEMO&"\
            f"%GMID&XXXX-XXXX-XXXX-DEMO&"\
            f"%CHAT&{config.IRCADDRESS}&"\
            f"%CHNL1&#GSP!conquest_m!5\\00&"\
            f"%CHNL2&#GSP!conquest!3\\00)",
            f"<MESDLG>",
        ))

    else:
        return mesError("ERROR", "INCORRECT NICKNAME")

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
        f"//#exec(LW_cfile&\\00&Bastet/%GV_VE_NICK)",
        f"#edit[%E_NICK](%LBX[x:172,y:112,w:232,h:18],{{%GV_VE_NICK}},\"Player\")",
        f"#pix[%PX2](%LBX[x:4,y:157,w:100%,h:100%],{{}},Internet/pix/i_pri0,35,35,35,35)",
        f"<NEWDLG>",
        f"<NEWDLG>",
        f"#block(newdlg.cml,CAN)",
        f"<NEWDLG>",
        f"<NEWDLG>",
        f"#end(CAN)",
        f"#hint(%L_NICK,\"Enter your nickname\")",
        f"#hint(%Login,\"Join the server\")",
    ))


def voting():
    return "\n".join((
        _voting(),
        _font("GC12", "R2C12", "RC12"),
        _txt("ANS0", "B_VOTE", 5, 3, "100%-10", 14, "", "Top donations: "),
        _apan("PAN1", "B_VOTE", 0-3, "%ANS0+0+10", "100%-4", 13,
              "GW|open&voting.dcml\\00&question=32^answer=65\\00|LW_lockall", 14, ""),
        _font("R2C12", "R2C12", "RC12"),
        _txt("ANS1", "B_VOTE", 0, "%ANS0+0+11", "100%", 20, "", "1. - "),
        _ctxt("RES1", "B_VOTE", 105, "%ANS0+0+11", 40, 20, "", "0"),
        _apan("PAN2", "B_VOTE", 0-3, "%ANS0+14+10", "100%-4", 13,
              "GW|open&voting.dcml\\00&question=32^answer=62\\00|LW_lockall", 14, ""),
        _font("R2C12", "R2C12", "RC12"),
        _txt("ANS2", "B_VOTE", 0, "%ANS0+14+11", "100%", 20, "", "2. - "),
        _ctxt("RES2", "B_VOTE", 105, "%ANS0+14+11", 40, 20, "", "0"),
        _apan("PAN3", "B_VOTE", 0-3, "%ANS0+28+10", "100%-4", 13,
              "GW|open&voting.dcml\\00&question=32^answer=63\\00|LW_lockall", 14, ""),
        _font("R2C12", "R2C12", "RC12"),
        _txt("ANS3", "B_VOTE", 0, "%ANS0+28+11", "100%", 20, "", "3. - "),
        _ctxt("RES3", "B_VOTE", 105, "%ANS0+28+11", 40, 20, "", "0"),
        _apan("PAN4", "B_VOTE", 0-3, "%ANS0+42+10", "100%-4", 13,
              "GW|open&voting.dcml\\00&question=32^answer=64\\00|LW_lockall", 14, ""),
        _font("R2C12", "R2C12", "RC12"),
        _txt("ANS4", "B_VOTE", 0, "%ANS0+42+11", "100%", 20, "", "4. - "),
        _ctxt("RES4", "B_VOTE", 105, "%ANS0+42+11", 40, 20, "", "0"),
        _voting(),
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
