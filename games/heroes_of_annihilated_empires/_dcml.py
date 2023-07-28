from __future__ import annotations
from . import config
from .. import classes
from .. import common
import mysql.connector
from datetime import datetime

db = mysql.connector.connect(**config.DB)
cursor = db.cursor()

gameTypes = classes.GameTypes(config.GAMETYPES)



def mesError(title: str, description: str):
    return "".join((
        f"<NEWDLG>",
        f"#ebox[%MBG](x:0,y:0,w:1024,h:768)",
        f"#pix[%PX1](%MBG[x:0,y:0,w:1024,h:768],{{}},Interf3/internet,0,0,0,0)",
        f"#exec(LW_enbbox&0&%L0)",
        f"#exec(LW_enbbox&0&%B)",
        f"#exec(LW_enbbox&0&%FLBOX)",
        f"#exec(LW_enbbox&0&%BP)",
        f"#exec(LW_enbbox&0&%L)",
        f"#exec(LW_enbbox&0&%BB)",
        f"#exec(LW_enbbox&0&%B1)",
        f"#exec(LW_enbbox&0&%BG)",
        f"#exec(LW_enbbox&0&%B2)",
        f"#exec(LW_enbbox&0&%BPANEL)",
        f"#exec(LW_enbbox&0&%BPANEL2)",
        f"#exec(LW_enbbox&0&%TB)",
        f"#exec(LW_enbbox&0&%B_VOTE)",
        f"#exec(LW_enbbox&0&%MBG)",
        f"#exec(LW_enbbox&0&%B0)",
        f"#exec(LW_enbbox&0&%M)",
        f"#exec(LW_enbbox&0&%LB)",
        f"#exec(LW_enbbox&0&%MB)",
        f"#exec(LW_enbbox&0&%EBG)",
        f"#exec(LW_enbbox&0&%LBX)",
        f"#exec(LW_enbbox&0&%BARDLD)",
        f"#exec(LW_enbbox&0&%BF2)",
        f"#exec(LW_enbbox&0&%B01)",
        f"#exec(LW_enbbox&0&%BF)",
        f"#exec(LW_enbbox&0&%BTABLE)",
        f"#exec(LW_enbbox&0&%SB)",
        f"#ebox[%BTABLE2](x:0,y:0,w:100%,h:100%)",
        f"#font(BC12,BC12,BC12)",
        f"#def_panel(11,Interf3/elements/b02,21,20,14,15,4,5,12,16,8,8)",
        f"#pan[%MPN](%BTABLE2[x:306,y:310+15,w:415,h:220-15],11)",
        f"#pix[%PXP1](%BTABLE2[x:306+20,y:310+20,w:100%,h:100%],{{}},Internet/pix/i_pri0,32,32,32,32)",
        f"#pix[%PX2](%BTABLE2[x:576,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX3](%BTABLE2[x:401,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX4](%BTABLE2[x:451,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX5](%BTABLE2[x:501,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX6](%BTABLE2[x:551,y:310-10,w:50,h:70],{{}},Interf3/elements/head01,2,2,2,2)",
        f"#pix[%PX0](%BTABLE2[x:391,y:310-10,w:90,h:70],{{}},Interf3/elements/head01,0,0,0,0)",
        f"#pix[%PX1](%BTABLE2[x:626,y:310-10,w:90,h:70],{{}},Interf3/elements/head01,1,1,1,1)",
        f"#font(BG18,BG18,RG18)",
        f"#ctxt[%TTEXT](%BTABLE2[x:306,y:310-1,w:415,h:20],{{0}},\"{title}\")",
        f"#font(BC12,RC12,RC12)",
        f"#ctxt[%MTXT0](%BTABLE2[x:306+20,y:310+22,w:415-40,h:20],{{}},\"{description}\")",
        f"#exec(LW_vis&0&%MTXT0)",
        f"#ctxt[%MTXT](%BTABLE2[x:306+20,yc:420-3,w:415-40,h:%MTXT0-310-23],{{}},\"{description}\")",
        f"#def_gp_btn(Internet/pix/i_pri0,49,50,0,0)",
        f"#font(WG14,BG14,WG14)",
        f"#gpbtn[%PXBT2](%BTABLE2[x:0,y:499-16,w:100%,h:70],{{GW|open&demologin.dcml\\00}},\"OK\")",
        f"<NEWDLG>",
    ))

