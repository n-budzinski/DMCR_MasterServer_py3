def cancel():
    return "".join((
        f"<NGDLG>",
        f"#exec(LW_time&3000&l_games_btn.cml\\00)",
        f"<NGDLG>",
))