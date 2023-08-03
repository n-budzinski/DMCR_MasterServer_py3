def critical_error(file: str):
    return "".join((f"<MESDLG>",
        f"#ebox[%MBG](x:0,y:0,w:1024,h:768)",
        f"#exec(LW_cfile&n/a\\00&Cookies/%GV_VE_ICQ)",
        f"#exec(LW_cfile&n/a\\00&Cookies/%GV_VE_PHON)",
        f"#def_dtbl_button_hotkey(13,27)",
        f"#table[%TBL](%MBG[x:306,y:325,w:415,h:205],{{}}{{}}{{GW|open&{file}\\00|LW_lockall}}{{LW_file&Internet/Cash/l_games_btn.cml}},2,0,3,13,252,\"CRITICAL ERROR\",\"Server error occurred while processing your request! Press Try Again button to attempt process request again. Press Cancel to exit\",26,\"Try Again\",\"Cancel\")",
        f"<MESDLG>"
    ))