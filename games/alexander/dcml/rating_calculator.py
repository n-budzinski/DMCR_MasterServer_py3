import sqlalchemy
from math import floor, ceil

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

def rating_calculator(options: dict, database: sqlalchemy.Engine) -> str:
    win, loss = 0, 0
    if options['score1'] and options['score2']:
        you, opponent = int(options['score1']), int(options['score2'])
        win = abs(floor(clip(you + 10 * 1 * (opponent + 100) / (you + 100) - you, 0, 100)))
        loss = abs(ceil(clip(you + 10 * -1 * (you + 100) / (opponent + 100) - you, -100, -1)))

    return "".join((
        f"<RGDLG>",
        f"#ebox[%B2](x:427,y:266,w:288,h:72)",
        f"#def_panel(9,Internet/pix/i_pri0,-1,-1,-1,-1,-1,-1,30,-1,-1,-1)",
        f"#pan[%P4](%B2[x:31,y:0-32,w:0,h:137],10)",
        f"#pan[%P5](%B2[x:127,y:0-32,w:0,h:137],10)",
        f"#pan[%P6](%B2[x:223,y:0-32,w:0,h:137],10)",
        f"#font(R2C12,BC12,BC12)",
        f"#ctxt[%I1](%B2[x:96,y:1,w:96,h:20],{{}},\"You\")",
        f"#ctxt[%I2](%B2[x:192,y:1,w:96,h:20],{{}},\"Enemy\")",
        f"#pan[%P1](%B2[x:64,y:49,w:257,h:0],9)" if not win or not loss else\
        f"#pan[%P2](%B2[x:0-32,y:67,w:353,h:0],9)\
        #pan[%P3](%B2[x:0-32,y:85,w:353,h:0],9)",
        f"#font(R2C14,R2C14,R2C14)",
        f"#ctxt[%I3](%B2[x:0,y:11,w:96,h:20],{{}},\"Score\")",\
        f"#font(R2C12,R2C12,R2C12)\
        #ctxt[%I3](%B2[x:0,y:36,w:96,h:20],{{}},\"You win\")\
        #ctxt[%I3](%B2[x:0,y:54,w:96,h:20],{{}},\"You lose\")\
        #font(BC12,R2C12,R2C12)\
        #stbl[%TBL](%B2[x:96,y:36,w:192,h:36],{{}},2,0,50,1,50,1,17,\"+{win} pt\",\"-{win} pt\",17,\"-{loss} pt\",\"+{loss} pt\")" if options['score1'] and options['score2'] else "",
        f"#pan[%P1](%B2[x:104,y:18,w:80,h:10],1)",
        f"#font(BC12,RC12,RC12)",
        f"#edit[%E1](%B2[x:104,y:15,w:80,h:17],{{%GV_SCORE1}},0,1)",
        f"#pan[%P2](%B2[x:200,y:18,w:80,h:10],1)",
        f"#edit[%E2](%B2[x:200,y:15,w:80,h:17],{{%GV_SCORE2}},0,1,0,1)",
        f"#exec(LW_cfile&{options['score1']}\\00&Cookies/%GV_SCORE1)\
        #exec(LW_cfile&{options['score2']}\\00&Cookies/%GV_SCORE2)" if options['score1'] and options['score2'] else "",
        f"#font(BC14,WC14,BC14)",
        f"#sbtn[%BT](%B2[x:242,y:110,w:45,h:205],{{GW|open&rating_calculator.dcml\\00&score1=<%GV_SCORE1>^score2=<%GV_SCORE2>\\00|LW_lockall}},\"Calculate\")",
        f"<RGDLG>"
))