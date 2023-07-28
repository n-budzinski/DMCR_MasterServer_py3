import sqlalchemy
from datetime import datetime

def voting_view(database: sqlalchemy.Engine):
    output = []

    with database.connect() as connection:
        votings = connection.execute(sqlalchemy.text(f"SELECT id, subject, published_at FROM votes;")).fetchall()
        n = None
        for idx, voting in enumerate(votings):
            output.append(
                f'#font(R2C12,R2C12,RC12)\
                #rtxt[%DATE{idx}](%SB[x:100%-210,y:{25-20 if not output else f"%ANS{idx-1}_{n}+40-20"},w:200,h:20],{{}},"Published {voting[2].strftime("%m.%d.%Y") if type(voting[2]) == datetime else voting[2]}")\
                #font(GC14,R2C14,RC14)\
                #ctxt[%ANS{idx}_0](%SB[x:5,y:{25-3 if not output else f"%ANS{idx-1}_{n}+40-3"},w:100%-10,h:20],{{}},"{voting[1]}")\
                #font(BC12,R2C12,RC12)')
            n = 0
            answers = connection.execute(sqlalchemy.text(f"SELECT text, votes FROM vote_answers WHERE vote_id = {voting[0]} LIMIT 4;")).fetchall()
            for idy, answer in enumerate(answers):
                n = idy + 1
                output.append(
                    f'#txt[%ANS{idx}_{idy+1}](%SB[x:10,y:%ANS{idx}_{idy},w:100%-30,h:20],{{}},"- {answer[0]}")\
                    #rtxt[%RES{idx}_{idy+1}](%SB[x:100%-110,y:%ANS{idx}_{idy},w:100,h:20],{{}},"{answer[1]}")')
            output.append(f'#pan[%HPAN{idx}](%SB[x:0-32,y:%ANS{idx}_{n}+40,w:100%+65,h:0],9)')

    return "".join((
        f"#ebox[%TB](x:0,y:0,w:100%,h:100%)",
        f"#pix[%PXT1](%TB[x:0,y:38,w:100%,h:100%],{{}},Internet/pix/i_pri0,12,12,12,12)",
        f"#pix[%PXT2](%TB[x:0,y:263,w:100%,h:100%],{{}},Internet/pix/i_pri0,13,13,13,13)",
        f"#pan[%P1](%TB[x:42,y:0-22,w:0,h:80],10)",
        f"#font(RG18,RG18,RG18)",
        f"#txt[%PL](%TB[x:737,y:0,w:150,h:20],{{}},\"Players\")",
        f"#font(BG18,BG18,BG18)",
        f"#ctxt[%TTTEXT](%TB[x:0-62,y:0-32,w:1024,h:20],{{}},\"NEWS & EVENTS\")",
        f"#font(R2C12,R2C12,R2C12)",
        f"#txt[%TMTEXT](%TB[x:0,y:514,w:100,h:20],{{}},\"Message:\")",
        f"#font(RC12,RC12,RC12)",
        f"#def_gp_btn(Internet/pix/i_pri0,51,51,0,1)",
        f"#gpbtn[%BT1](%TB[x:74,y:22,w:-22,h:-18],{{GW|open&news.dcml\\00&language=\\00|LW_lockall}},\"News & Events\")",
        f"#hint(%BT1,\"News, events, forum and punishment list\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT2](%TB[x:196,y:23,w:-22,h:-18],{{GW|open&users_list.dcml\\00|LW_lockall}},\"Player List\")",
        f"#hint(%BT2,\"Player list, personal mail and clan information\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT4](%TB[x:318,y:23,w:-22,h:-18],{{GW|open&games.dcml\\00|LW_lockall}},\"Custom Games\")",
        f"#hint(%BT4,\"Play custom games\")",
        f"#def_gp_btn(Internet/pix/i_pri0,52,52,0,1)",
        f"#font(RC12,R2C12,RC12)",
        f"#gpbtn[%BT5](%TB[x:440,y:23,w:-22,h:-18],{{GW|open&scored_games.dcml\\00&player_id=0\\00|LW_lockall}},\"Scored Games\")",
        f"#hint(%BT5,\"Played games and their scores\")",
        f"#ebox[%B_VOTE](x:5,y:396,w:140,h:103)",
        f"<VOTING>",
        f"#exec(GW|open&voting.dcml\\00&question=46\\00)",
        f"<VOTING>",
        f"#ebox[%B](x:0,y:0,w:100%,h:100%)",
        f"#font(RC14,R2C14,RC14)",
        f"#ctxt[%LIST1](%B[x:0,y:106,w:146,h:24],{{GW|open&news.dcml\\00|LW_lockall}},\"{{News & Events}}\")",
        f"#font(RC14,GC14,RC14)",
        f"#ctxt[%LIST2](%B[x:0,y:%LIST1-9,w:146,h:24],{{GW|open&voting_view.dcml\\00|LW_lockall}},\"{{View votes}}\")",
        f"#pan[%PAN](%B[x:154,y:42,w:526-3,h:291],7)",
        f"#sbox[%SB](x:150,y:42+4,w:526+4,h:291-8)",
        "".join(output),
        f"#font(R2C14,R2C14,RC14)",
        f"#ctxt[%LIST5](%B[x:0,y:%LIST2-9,w:146,h:24],{{GW|open&punishments.dcml\\00|LW_lockall}},\"{{Punishments}}\")",
        f"#hint(%LIST5,\"List of punished players\")",
        f"#edit[%E_FT](%B[x:0,y:0,w:0,h:0],{{%GV_FORUM_LAST_TIME}})",
        f"#ctxt[%LIST6](%B[x:0,y:%LIST5-9,w:146,h:24],{{GW|open&forum.dcml\\00&last_view=<%GV_FORUM_LAST_TIME>\\00|LW_lockall}},\"{{Forum}}\")",
        f"#hint(%LIST6,\"Read and write forum messages\")",
        f"<NGDLG>",
        f"<NGDLG>",
        f"#block(cancel.cml,CAN)<NGDLG>",
        f"<NGDLG>",
        f"#end(CAN)"))