

def _ebox(id, posX, posY, width, height) -> str:
    return f"#ebox[%{id}](x:{posX},y:{posY},w:{width},h:{height})"

def _pix(id, parentID, posX, posY, width, height, element, a, b, c, d) -> str:
    return f"#pix[%{id}](%{parentID}[x:{posX},y:{posY},w:{width},h:{height}],{{}},{element},{a},{b},{c},{d})"

def _exec(cmd, execs: dict) -> str:
    e = [cmd]
    for key, value in execs.items():
        e.append(f"{key+'&'+value if(value is not None) else key}")
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

def _end(a):
    return f"#end({a})"

def _hint(parentID, text):
    return f"#hint(%{parentID},\"{text}\")"

def _voting() -> str:
    return "<VOTING>"

def _mesdlg() -> str:
    return "<MESDLG>"

def _ngdlg() -> str:
    return "<NGDLG>"


def logUser(gameManager, options, chatAddress, player) -> str:
    from common import checkAlpha
    gameManager.leaveLobby(player)
    player.nickname = options.get("VE_NICK")
    if len(player.nickname) > 3 and checkAlpha(player.nickname):
        return "\n".join((
                _mesdlg(),
                _ebox("MBG", 0, 0, 1024, 768),
                _pix("PX1", "MBG", 0, 0, 1024, 768, "Interf3/internet", 0, 0, 0, 0),
                _exec("LW_key", {
                    f"{player.sessionID}": None
                }),
                _exec("LW_gvar", {
                    "%PROF": f"{player.sessionID}",
                    "%NAME":"n/a",
                    "%NICK":f"{player.nickname}",
                    "%MAIL":"n/a",
                    "%PASS":"DEMO",
                    "%GMID":"XXXX-XXXX-XXXX-DEMO",
                    "%CHAT":f"{chatAddress}",
                    "%CHNL1":"#GSP!conquest_m!5\\00",
                    "%CHNL2":"#GSP!conquest!3\\00",
                }),
                _mesdlg(),
                ))
    else:
        return "\n".join((
                _mesdlg(),
                _ebox("MBG", 0, 0, 1024, 768),
                _pix("PX1", "MBG", 0, 0, 1024, 768, "Interf3/internet", 0, 0, 0, 0),
                _exec("LW_enbbox", {
                    f"0": "%L0"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B"
                }),
                _exec("LW_enbbox", {
                    f"0": "%FLBOX"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BP"
                }),
                _exec("LW_enbbox", {
                    f"0": "%L"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B1"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BG"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B2"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BPANEL"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BPANEL2"
                }),
                _exec("LW_enbbox", {
                    f"0": "%TB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B_VOTE"
                }),
                _exec("LW_enbbox", {
                    f"0": "%MBG"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B0"
                }),
                _exec("LW_enbbox", {
                    f"0": "%M"
                }),
                _exec("LW_enbbox", {
                    f"0": "%LB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%MB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%EBG"
                }),
                _exec("LW_enbbox", {
                    f"0": "%LBX"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BARDLD"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BF2"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B01"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BF"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BTABLE"
                }),
                _exec("LW_enbbox", {
                    f"0": "%SB"
                }),
                _ebox("%BTABLE", 0, 0, "100%", "100%"),
                _font("BC12", "BC12", "BC12"),
                _def_panel(11, "Interf3/elements/b02",21,20,14,15,4,5,12,16,8,8),
                _pan("MPN", "BTABLE2", 306, 310+15, 415, 220-15, 11),
                _pix("PXP1", "BTABLE2", 306-20, 310+20, "100%", "100%", "Internet/pix/i_pri0", 32, 32, 32, 32),
                _pix("PX2", "BTABLE2", 576, 310-10, 50, 70, "Internet/pix/head01", 2, 2, 2, 2),
                _pix("PX3", "BTABLE2", 401, 310-10, 50, 70, "Internet/pix/head01", 2, 2, 2, 2),
                _pix("PX4", "BTABLE2", 451, 310-10, 50, 70, "Internet/pix/head01", 2, 2, 2, 2),
                _pix("PX5", "BTABLE2", 501, 310-10, 50, 70, "Internet/pix/head01", 2, 2, 2, 2),
                _pix("PX6", "BTABLE2", 551, 310-10, 50, 70, "Internet/pix/head01", 2, 2, 2, 2),
                _pix("PX0", "BTABLE2", 391, 310-10, 50, 70, "Internet/pix/head01", 0, 0, 0, 0),
                _pix("PX1", "BTABLE2", 626, 310-10, 50, 70, "Internet/pix/head01", 1, 1, 1, 1),
                _font("BG18", "BG18", "RG18"),
                _ctxt("TTEXT", "BTABLE2", 306, 310-1, 415, 20, "", "ERROR"),
                _font("BC12", "RC12", "RC12"),
                _ctxt("TTEXT", "BTABLE2", 306+20, 310+22, 415-40, 20, "",
                      "Incorrect nickname! Nickname must begin with a letter\
                          and must not contain other characters than letters and digits in its body.\
                            Press Edit button to check nickname. Press Cancel to exit"),
                _exec("LW_vis", {
                    f"0": "%MTXT0"
                }),
                _ctxt("MTXT", "BTABLE2", 306+20, 420-3, 415-40, "%MTXT0 - 310 - 23", "",
                      "Incorrect nickname! Nickname must begin with a letter\
                          and must not contain other characters than letters and digits in its body.\
                            Press Edit button to check nickname. Press Cancel to exit"),
                _def_gp_btn("Internet/pix/i_pri0", 49, 50, 0, 0),
                _font("WG14", "BG14", "WG14"),
                _gpbtn("TTEXT", "BTABLE2", 349-433, 499-16, "100%", 70, "GW|open&log_conf_dlg.dcml\\00&VE_NICK=|LW_lockall","EDIT"),
                _def_gp_btn("Internet/pix/i_pri0", 49, 50, 0, 0),
                _font("WG14", "BG14", "WG14"),
                _gpbtn("TTEXT", "BTABLE2", 520-433, 499-16, "100%", 70, "LW_file&Internet/Cash/l_games_btn.cml","Cancel"),
                _mesdlg()
                ))


# player, options, gamemanager
def demoLogin() -> str:
    return "\n".join((
                _ebox("EBG", 0, 0, 1024, 768),
                _exec("LW_enbbox", {
                    f"0": "%L0"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B"
                }),
                _exec("LW_enbbox", {
                    f"0": "%FLBOX"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BP"
                }),
                _exec("LW_enbbox", {
                    f"0": "%L"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B1"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BG"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B2"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BPANEL"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BPANEL2"
                }),
                _exec("LW_enbbox", {
                    f"0": "%TB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B_VOTE"
                }),
                _exec("LW_enbbox", {
                    f"0": "%MBG"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B0"
                }),
                _exec("LW_enbbox", {
                    f"0": "%M"
                }),
                _exec("LW_enbbox", {
                    f"0": "%LB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%MB"
                }),
                _exec("LW_enbbox", {
                    f"0": "%EBG"
                }),
                _exec("LW_enbbox", {
                    f"0": "%LBX"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BARDLD"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BF2"
                }),
                _exec("LW_enbbox", {
                    f"0": "%B01"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BF"
                }),
                _exec("LW_enbbox", {
                    f"0": "%BTABLE2"
                }),
                _exec("LW_enbbox", {
                    f"0": "%SB"
                }),
                _ebox("BTABLE", 0, 0, "100%", "100%"),
                _font("BC12", "BC12", "BC12"),
                _def_panel(11, "Interf3/elements/b02", -1, -1, -1, -1, -1, -1, -1, -1, 8, 8),
                _pan("MPNT", "BTABLE", 251, 308, 523, 240, 11),
                _def_panel(11, "Interf3/elements/b02", -1, -1, 14, 15, 4, 5, 11, 16, -1, -1),
                _pan("MPN", "BTABLE", 251, 308, 523, 240, 11),
                _pix("PXT1", "BTABLE", 251-208, 308-189, 50, 70, "Interf3/elements/b02", 18, 18, 18, 18),
                _pix("PXT2", "BTABLE",566, 308-189, 50, 70, "Interf3/elements/b02", 19, 19, 19, 19),
                _pix("PX2", "BTABLE", 617+5, 308-5, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
                _pix("PX3", "BTABLE", 347+5, 308-5, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
                _pix("PX4", "BTABLE", 397+5, 308-5, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
                _pix("PX5", "BTABLE", 447+5, 308-5, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
                _pix("PX6", "BTABLE", 497+5, 308-5, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
                _pix("PX7", "BTABLE", 547+5, 308-5, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
                _pix("PX8", "BTABLE", 597+5, 308-5, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
                _pix("PX0", "BTABLE", 342, 308-5, 90, 70, "Interf3/elements/head01", 0, 0, 0, 0),
                _pix("PX1", "BTABLE", 672, 308-5, 90, 70, "Interf3/elements/head01", 1, 1, 1, 1),
                _font("BG18", "BG18", "RG18"),
                _ctxt("TTEXT", "BTABLE", 251+2, 308+4, 523, 20, 0, "Bastet Login"),
                _def_gp_btn("Internet/pix/i_pri0", 49, 50, 0, 0),
                _def_gp_btn("Internet/pix/i_pri0", 49, 50, 0, 0),
                _font("WG14", "BG14", "WG14"),
                _gpbtn("PXBT", "BTABLE", 348-433, 517-16, "100%", 70, "GW|open&log_user.dcml\\00&VE_NICK=<%GV_VE_NICK>\\00|LW_lockall","Login"),
                _def_gp_btn("Internet/pix/i_pri0", 49, 50, 0, 0),
                _font("WG14", "BG14", "WG14"),
                _gpbtn("PXBT", "BTABLE", 519-433, 517-16, "100%", 70, "LW_key&#CANCEL","Cancel"),
                _ebox("LBX", 270, 310, 500, 220),
                _pix("PX1", "LBX", 2, 54, "100%", "100%", "Internet/pix/i_pri0", 35, 35, 35, 35),
                _font("BC14", "BC14", "BC14"),
                _txt("L_NICK", "LBX", 74, 115, "100%", 20, "", "Nickname"),
                _pan("P_NICK", "LBX", 167, 115, 238, 14, 1),
                _edit("E_NICK", "LBX", 172, 112, 232, 18, "%GV_VE_NICK", "Player"),
                _pix("PX2", "LBX", 4, 157, "100%", "100%", "Internet/pix/i_pri0", 35, 35, 35, 35),
                _mesdlg(),
                _mesdlg(),
                _block("l_games_btn.cml","CAN"),
                _mesdlg(),
                _mesdlg(),
                _end("CAN"),
                _hint("L_NICK", "Enter your nickname"),
                _hint("Login", "Join the server"),
            ))


def voting():
        return "\n".join((
           _voting(),
           _font("GC12", "R2C12", "RC12"),
           _txt("ANS0", "B_VOTE", 5, 3, "100%-10", 14, "","Top donations: "),
           _apan("PAN1", "B_VOTE", 0-3, "%ANS0+0+10", "100%-4", 13, "GW|open&voting.dcml\\00&question=32^answer=65\\00|LW_lockall", 14, ""),
           _font("R2C12", "R2C12", "RC12"),
           _txt("ANS1","B_VOTE", 0, "%ANS0+0+11", "100%", 20, "", "1. - "),
           _ctxt("RES1","B_VOTE", 105, "%ANS0+0+11", 40, 20, "", "0"),
           _apan("PAN2","B_VOTE", 0-3, "%ANS0+14+10", "100%-4", 13, "GW|open&voting.dcml\\00&question=32^answer=62\\00|LW_lockall", 14, ""),
           _font("R2C12","R2C12","RC12"),
           _txt("ANS2","B_VOTE", 0, "%ANS0+14+11", "100%", 20, "", "2. - "),
           _ctxt("RES2","B_VOTE", 105, "%ANS0+14+11", 40, 20, "", "0"),
           _apan("PAN3","B_VOTE", 0-3, "%ANS0+28+10", "100%-4", 13, "GW|open&voting.dcml\\00&question=32^answer=63\\00|LW_lockall", 14, ""),
           _font("R2C12","R2C12","RC12"),
           _txt("ANS3","B_VOTE", 0, "%ANS0+28+11", "100%", 20, "", "3. - "),
           _ctxt("RES3", "B_VOTE", 105, "%ANS0+28+11", 40, 20, "","0"),
           _apan("PAN4", "B_VOTE", 0-3, "%ANS0+42+10", "100%-4", 13, "GW|open&voting.dcml\\00&question=32^answer=64\\00|LW_lockall", 14, ""),
           _font("R2C12", "R2C12", "RC12"),
           _txt("ANS4","B_VOTE", 0, "%ANS0+42+11", "100%", 20, "", "4. - "),
           _ctxt("RES4","B_VOTE", 105, "%ANS0+42+11", 40, 20, "", "0"),
           _voting(),
        ))

def error():
    return "\n".join((
        _ngdlg(),
        _ebox("EBG", 0, 0, 1024, 768),
        _pix("PX1","L0",0-62,0-136,1024,768,"Interf3/internet",0,0,0,0),
        _exec("LW_enbbox", {
            f"0": "%L0"
        }),
        _exec("LW_enbbox", {
            f"0": "%B"
        }),
        _exec("LW_enbbox", {
            f"0": "%FLBOX"
        }),
        _exec("LW_enbbox", {
            f"0": "%BP"
        }),
        _exec("LW_enbbox", {
            f"0": "%L"
        }),
        _exec("LW_enbbox", {
            f"0": "%BB"
        }),
        _exec("LW_enbbox", {
            f"0": "%B1"
        }),
        _exec("LW_enbbox", {
            f"0": "%BG"
        }),
        _exec("LW_enbbox", {
            f"0": "%B2"
        }),
        _exec("LW_enbbox", {
            f"0": "%BPANEL"
        }),
        _exec("LW_enbbox", {
            f"0": "%BPANEL2"
        }),
        _exec("LW_enbbox", {
            f"0": "%TB"
        }),
        _exec("LW_enbbox", {
            f"0": "%B_VOTE"
        }),
        _exec("LW_enbbox", {
            f"0": "%MBG"
        }),
        _exec("LW_enbbox", {
            f"0": "%B0"
        }),
        _exec("LW_enbbox", {
            f"0": "%M"
        }),
        _exec("LW_enbbox", {
            f"0": "%LB"
        }),
        _exec("LW_enbbox", {
            f"0": "%MB"
        }),
        _exec("LW_enbbox", {
            f"0": "%EBG"
        }),
        _exec("LW_enbbox", {
            f"0": "%LBX"
        }),
        _exec("LW_enbbox", {
            f"0": "%BARDLD"
        }),
        _exec("LW_enbbox", {
            f"0": "%BF2"
        }),
        _exec("LW_enbbox", {
            f"0": "%B01"
        }),
        _exec("LW_enbbox", {
            f"0": "%BF"
        }),
        _exec("LW_enbbox", {
            f"0": "%BTABLE2"
        }),
        _exec("LW_enbbox", {
            f"0": "%SB"
        }),
        _ebox("BTABLE", 0, 0, "100%", "100%"),
        _font("BC12", "BC12", "BC12"),
        _def_panel(11, "Interf3/elements/b02",21,20,14,15,4,5,12,16,8,8),
        _pan("MPN", "BTABLE2", 242, 115+15, 415, 220-15, 11),
        _pix("PXP1", "BTABLE2", 242+20, 115+20, "100%", "100%", "Internet/pix/i_pri0", 32, 32, 32, 32),
        _pix("PX2", "BTABLE", 522, 115-10, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
        _pix("PX3", "BTABLE", 327, 115-10, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
        _pix("PX4", "BTABLE", 377, 115-10, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
        _pix("PX5", "BTABLE", 427, 115-10, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
        _pix("PX6", "BTABLE", 477, 115-10, 50, 70, "Interf3/elements/head01", 2, 2, 2, 2),
        _pix("PX0", "BTABLE", 317, 115-10, 90, 70, "Interf3/elements/head01", 0, 0, 0, 0),
        _pix("PX1", "BTABLE", 572, 115-10, 90, 70, "Interf3/elements/head01", 1, 1, 1, 1),
        _font("BG18","BG18","RG18"),

        _ctxt("TTEXT", "BTABLE", 242, 115-1, 415, 20, 0, "ERROR"),
        _font("BC12","RC12","RC12"),
        _ctxt("MTEXT0", "BTABLE", 242+20, 115+22, 415-40, 20, "", "Critical server error!"),
        _exec("LW_vis", {
            f"0": "%MTEXT0"
        }),
        _ctxt("MTEXT", "BTABLE", 242+20, 225-3, 415-40, "%MTEXT0-115-159", "", "Critical server error!"),
        _def_gp_btn("Internet/pix/i_pri0",49,50,0,0),
        _font("WG14","BG14","WG14"),
        _gpbtn("PXBT", "BTABLE", 520-433, 303-16, "100%", 70, "GW|open&cancel.dcml\\00|LW_lockall", "OK"),
        _ngdlg(),
    ))