import sqlalchemy
from ...common import reverse_address

def dbtbl(database: sqlalchemy.Engine):
    with database.connect() as connection:
        lobbies = connection.execute(sqlalchemy.text(
            f"SELECT id, title, host_id, (SELECT name FROM lobby_types WHERE name = type)\
                AS type, max_players, players, password, ip, (SELECT nick FROM players WHERE players.player_id = host_id)\
                AS nick FROM lobbies")).fetchall()
    lobby_list = []
    if lobbies:
            lobby_list.extend(("".join(
            [f"#apan[%JPAN{idx}](%SB[x:0,y:{idx*18},w:100%-1,h:17],{{GW|open&join_game.dcml\\00&delete_old=true^id_room={str(lobby[0])}\\00|LW_lockall}},8,,)\
            #font(BC12,BC12,BC12)\
            #ping[%PING{idx}](%SB[x:90%+20,y:{str(idx*18)}+5,w:10,h:20],{reverse_address(lobby[-2])})"
             for idx, lobby in enumerate(lobbies)]),
            f"#def_tbl_line(-1,-1)",
            f"#font(BC12,BC12,BC12) ",
            f"#stbl[%ROOM_LST](%SB[x:0,y:3,w:545,h:100%-3],{{}},5,0,35,0,24,1,17,1,14,1,10,1",
            "".join([f',18,"{str(lobby[1]) + (" (Y) " if lobby[6] != "" else " (N) ")}", {lobby[-1]},"{lobby[3]}","{lobby[5]}/{lobby[4]}",""' for lobby in lobbies]),
            f")#font(GC14,RC14,RC14)#sbtn[%B_J](%B[x:312,y:354,w:0,h:0],{{GW|open&join_game.dcml\\00&delete_old=true^id_room=<%GV_SELECTED_PAN>\\00|LW_lockall}},\"Join\")"))

    return "\n".join((
        f"<DBTBL> ",
        f"#block(l_games_btn.cml,l_g):GW|open&dbtbl.dcml\\00&order=^resort=\\00|LW_lockall ",
        f"#end(l_g) ",
        f"#sbox[%SB](x:150,y:63,w:545,h:275) ",
        f"#ebox[%BB](x:0,y:0,w:100%,h:100%) ",
        f"#font(R2C12,R2C12,RC12) ",
        f"#stbl[%TBL](%BB[x:150,y:42,w:545,h:296],{{GW|open&dbtbl.dcml\\00&order=r.title^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=u.nick^resort=\\00|LW_lockall}}{{GW|open&dbtbl.dcml\\00&order=t.name^resort=\\00|LW_lockall}}{{}}{{}},5,6,35,1,24,1,17,1,14,1,10,1,24,\"{{Game Title (Password)\",\"{{Host\",\"{{Type\",\"Players\",\"Ping\") ",
        "".join(lobby_list),
        f"#font(GC14,RC14,RC14) ",
        f"#sbtn[%B_R](%B[x:446,y:354,w:0,h:0],{{GW|open&dbtbl.dcml\\00&order=r.hbtime^resort=\\00|LW_lockall}},\"Refresh\") ",
        f"<DBTBL>"
    ))