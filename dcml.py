

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

def _ctxt(id, posX, posY, width, height, command, text):
    return f"#ctxt[%{id}][x:{posX},y:{posY},w:{width},h:{height}],{{{command}}},\"{text}\")"

def _def_gp_btn(element, a, b, c, d):
    return f"#def_gp_btn({element},{a},{b},{c},{d})"

def _gpbtn(id, posX, posY, width, height, command, text):
    return f"#gpbtn[%{id}][x:{posX},y:{posY},w:{width},h:{height}],{{{command}}},\"{text}\")"


def _mesdlg() -> str:
    return "<MESDLG>"

# player, options, gamemanager
def logUser(gameManager, options, chatAddress, player) -> str:
    ve_nick = None
    from common import check_alpha
    gameManager.leave_lobby(player)
    player.nickname = options.get("VE_NICK")
    if len(player.playerName) > 3 and check_alpha(player.playerName):
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
                _ctxt("TTEXT", "BTABLE2", 306, 310-1, 415, 20, "ERROR"),
                _font("BC12", "RC12", "RC12"),
                _ctxt("TTEXT", "BTABLE2", 306+20, 310+22, 415-40, 20, 
                      "Incorrect nickname! Nickname must begin with a letter\
                          and must not contain other characters than letters and digits in its body.\
                            Press Edit button to check nickname. Press Cancel to exit"),
                _exec("LW_vis", {
                    f"0": "%MTXT0"
                }),
                _ctxt("MTXT", "BTABLE2", 306+20, 420-3, 415-40, "%MTXT0" - 310 - 23, 
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
