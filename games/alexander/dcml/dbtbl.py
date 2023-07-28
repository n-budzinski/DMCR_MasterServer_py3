import sqlalchemy
from ...common import reverse_address

def dbtbl(database: sqlalchemy.Engine):
    with database.connect() as connection:
        lobbies = connection.execute(sqlalchemy.text(
            f"SELECT id, title, host_id, (SELECT name FROM lobby_types WHERE name = type)\
                AS type, max_players, players, password, ip, (SELECT nick FROM players WHERE players.player_id = host_id)\
                AS nick FROM lobbies")).fetchall()
# if lobbies:
    return "".join((
        f"<DBTBL> ",
        f"#exec(LW_time&30000&l_games_btn.cml\\00) ",
        f"#block(l_games_btn.cml,l_g):GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall ",
        f"#end(l_g) ",
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%) ",
        f"#font(R2C12,R2C12,RC12) ",
        f"#stbl[%TBL](%BB[x:154,y:42,w:523,h:291],{{GW|open&dbtbl.dcml\\00&order=r.title^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=u.nick^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=t.name^resort=\\00|LW_lockall}}{{}}{{}},5,7,33,1,25,1,14,1,14,1,14,1,20,\"{{Game Title\",\"{{Host\",\"{{Type\",\"Players\",\"Ping\") ",
        f"#def_sbox(Internet/pix/i_pri%d,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,6,-21,25) ",
        f"#sbox[%SB](x:150,y:60,w:526+4,h:271) ",
        "".join(
        [f"#apan[%APAN{idx}](%SB[x:0,y:{idx*21}-2,w:100%,h:20],"\
        f"{{GW|open&join_game.dcml\\00&delete_old=true^id_room={str(lobby[0])}\\00|LW_lockall}},8)"\
        f"#font(BC12,BC12,BC12)"\
        f"#ping[%PING{idx}](%SB[x:86%+30,y:{str(idx*21)}+4,w:14,h:20],"\
        f"{reverse_address(lobby[-2])})"
            for idx, lobby in enumerate(lobbies)]),
        f"#font(BC12,BC12,BC12) ",
        f"#stbl[%ROOM_LST](%SB[x:4,y:0,w:523,h:21],{{}},5,0,33,0,25,1,14,1,14,1,14,1",
        "".join(
        [f',21,{str(lobby[1]) + "  *password*  " if lobby[6] != "" else ""}, {lobby[-1]},"{lobby[3]}","{lobby[5]}/{lobby[4]}",""' for lobby in lobbies]),
        f")#font(BC14,WC14,BC14) ",
        f"#sbtn[%B_J](%BB[x:521,y:377,w:100,h:305],{{GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall}},\"Refresh\")",
        f"#sbtn[%B_CREDITS](%BB[x:50,y:377,w:100,h:305],{{GW|url&https://0x7350.blogspot.com/\\00}},\"Credits\")",
        f"#sbtn[%B_DISCORD](%BB[x:170,y:377,w:100,h:305],{{GW|url&https://discord.gg/7tTAnPnNWG\\00}},\"Discord\")",
        f"#hint(%B_DISCORD,\"Find mates to play with\")",
        f"#sbtn[%B_DONATE](%BB[x:290,y:377,w:100,h:305],{{GW|url&https://paypal.me/NorbertBudzinski\\00}},\"Donate\")",
        f"#hint(%B_DONATE,\"Buy me a coffee\")",
        f"#sbtn[%B_J](%BB[x:521,y:377,w:100,h:305],{{GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall}},\"Refresh\") ",
        f"<DBTBL>"
    ))