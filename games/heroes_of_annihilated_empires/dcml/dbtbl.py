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
        f"<DBTBL>",
        f"#block(l_games_btn.cml,l_g):GW|open&dbtbl.dcml\\00&order=^resort=\\00|LW_lockall",
        f"#end(l_g)",
        f"#sbox[%SB](x:150,y:63,w:545,h:275)",
        "".join(
        [f"#apan[%APAN{idx}](%SB[x:0,y:{idx*21}-2,w:100%,h:20],"\
        f"{{GW|open&join_game.dcml\\00&delete_old=true^id_room={str(lobby[0])}\\00|LW_lockall}},8)"\
        f"#font(BC12,BC12,BC12)"\
        f"#ping[%PING{idx}](%SB[x:86%+30,y:{str(idx*21)}+4,w:14,h:20],"\
        f"{reverse_address(lobby[-2])})"
            for idx, lobby in enumerate(lobbies)]),
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%)",
        f"#font(R2C12,R2C12,RC12)",
        f"#stbl[%TBL](%BB[x:150,y:42,w:545,h:296],{{GW|open&dbtbl.dcml\\00&order=r.title^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=u.nick^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=t.name^resort=\\00|LW_lockall}}{{}}{{}},5,6,35,1,24,1,17,1,14,1,10,1,24",
        "".join(
        [f',21,{str(lobby[1]) + "  *password*  " if lobby[6] != "" else ""}, {lobby[-1]},"{lobby[3]}","{lobby[5]}/{lobby[4]}",""' for lobby in lobbies]),
        '{{Game Title (Password)","{{Host","{{Type","Players","Ping")',
        f")#font(GC14,RC14,RC14)",
        f"#sbtn[%B_R](%B[x:446,y:354,w:0,h:0],{{GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall}},\"Refresh\")",
        f"<DBTBL>",
        
    ))