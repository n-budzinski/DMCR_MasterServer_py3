import sqlalchemy

def clan_load_image(options: dict, database: sqlalchemy.Engine, player_id) -> str:
    if options['signature'] and options['icon_name']:
        return " ".join((
        f"<NGDLG>",
        f"#exec(GW|setclan&{options['signature']}.png\\00&<@%GV_CURFILE>&)",
        f"#exec(GW|open&clan_load_image.dcml\\00&help=true^signature={options['signature']}^icon_name={options['icon_name']}.png^gdwrite=true\\00|LW_lockall)",
        f"<NGDLG>",
    ))
    return " ".join((
        f"<NGDLG> ",
        f"#ebox[%L0](x:0,y:0,w:100%,h:100%) ",
        f"#table[%TBL](%L0[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&clan_load_image.dcml\\00&help=true^signature=SAM^icon_name=<%GV_CLAN_ICON>\\00|LW_lockall}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"CLAN ICON\",\"\",26,\"Upload\",\"Cancel\") ",
        f"#ebox[%BI](x:254,y:138,w:416,h:167) ",
        f"#pan[%P1](%BI[x:181,y:14,w:175,h:141],5) ",
        f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-3,6) ",
        f"#def_scroll(Interf3/elements/scroll3,0,0) ",
        f"#sbox[%FLBOX](x:437,y:152,w:175,h:140) ",
        f"#font(BC12,BC12,BC12)",
        f"#txt[%L](%BI[x:5,y:14,w:100,h:24],{{}},\"Icon:\") ",
        f"#pan[%P2](%BI[x:9,y:33,w:150,h:14],1) ",
        f"#font(BC12,BC12,BC12) ",
        f"#edit[%Eic](%BI[x:13,y:32,w:152,h:18],{{%GV_CLAN_ICON}}) ",
        f"#exec(LW_enb&0&%Eic)",
        f"#font(BC12,BC12,BC12)",
        f"#txt[%L](%BI[x:5,y:59,w:100,h:24],{{}},\"Disk:\") ",
        f"#cbb[%DISK](%BI[x:4,y:71,w:162,h:18],{{%CBVAR}},\"-\") ",
        f"#fbrowse({{%GV_FULLWAY}}{{%GV_CURFILE}}{{%GV_CLAN_ICON}},%DISK,%FLBOX,*.*) ",
        f"<%FLBOX> ",
        f"<%FLBOX> ",
        f"<NGDLG>",
    ))