import sqlalchemy

def join_pl_cmd(options: dict, database: sqlalchemy.Engine, player_id) -> str:
    if options['VE_PLAYER'] == str(player_id):
        return "".join((
            f"<NGDLG> ",
            f"#ebox[%BF2](x:0,y:0,w:100%,h:100%) ",
            f"#table[%TBL](%BF2[x:243,y:130,w:415,h:205],{{}}{{}}{{GW|open&join_pl_cmd.dcml\\00&VE_PLAYER=136995\\00}}{{LW_file&Internet/Cash/cancel.cml}},2,0,3,13,252,\"ERROR\",\"You cannot join the room! This is an incorrect room. Press Cancel button to exit\",26,\"Try Again\",\"Cancel\")",
            f"<NGDLG>",
        ))
    else:
        return ""