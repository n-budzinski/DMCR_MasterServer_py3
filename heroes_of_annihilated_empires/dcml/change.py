def change(options: dict) -> str:
    VE_PROF=options.get("VE_PROF", "n/a")
    VE_NAME=options.get("VE_NAME", "n/a")
    VE_NICK=options.get("VE_NICK", "n/a")
    VE_PASS=options.get("VE_PASS", "n/a")
    VE_MAIL=options.get("VE_MAIL", "n/a")
    VE_GMID=options.get("VE_GMID", "n/a")
    accounts=options.get("accounts", "")
    cansel=options.get("cansel", "")
    save_pass = options.get("save_pass", None)
    return "".join((
        f"<MESDLG>"
        f"#ebox[%D](x:0,y:0,w:1024,h:768)"
        f"#exec(LW_cfile&{accounts}\\00&Cookies/%GV_VE_ACCOUNTS)"
        f"#exec(GW|open&log_user.dcml\\00&cansel={cansel}^save_pass={save_pass}^icon_last_update=1098287226^VE_PROF={VE_PROF}^VE_NAME={VE_NAME}^VE_NICK={VE_NICK}^VE_MAIL={VE_MAIL}^VE_PASS={VE_PASS}^VE_GMID={VE_GMID}^accounts={accounts}\\00|LW_lockall)"
        f"<MESDLG>"
    ))