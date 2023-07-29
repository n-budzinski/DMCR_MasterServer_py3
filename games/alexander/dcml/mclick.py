import sqlalchemy

def mclick(options: dict, database: sqlalchemy.Engine) -> str:
    return "".join((
        f"<MCLICK>",
        f"<MCLICK>"
    ))