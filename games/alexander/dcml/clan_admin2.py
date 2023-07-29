import sqlalchemy

def clan_admin2(options: dict, database: sqlalchemy.Engine) -> str:
    # · ·open· ·   clan_admin2.dcml -   clanID=288^signature=GOTT^new_jointer=136995
    # clan_admin2.dcml ·   clanID=288^leaver=136995

    if options['new_jointer']:
        if options['again'] == 'true':
            ###removes existing clan
            return " ".join((
                f"<NGDLG> ",
                f"#exec(GW|open&clan_users.dcml\\00&clanID=288\\00|LW_lockall) ",
                f"<NGDLG>"
        ))
        else:
            ## if has a clan
            return " ".join((
            f"<NGDLG> ",
            f"#ebox[%L0](x:0,y:0,w:100%,h:100%) ",
            f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&clan_admin2.dcml\\00&again=true^clanID=288^new_jointer=136995\\00}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"NOTICE\",\"Delete clan [SAM]\",26,\"OK\",\"Cancel\") ",
            f"<NGDLG>",
    ))

    elif options['leaver']:
        #leaves clan
        return " ".join((
            f"<NGDLG> ",
            f"#exec(GW|open&clan_users.dcml\\00&clanID=288\\00|LW_lockall) ",
            f"<NGDLG>"
    ))

    else:
        ###removes existing clan
        return " ".join((
            f"<NGDLG> ",
            f"#exec(GW|open&clan_users.dcml\\00&clanID=288\\00|LW_lockall) ",
            f"<NGDLG>"
    ))
    