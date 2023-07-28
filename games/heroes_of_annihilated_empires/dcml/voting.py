import sqlalchemy

def voting(options: dict, database: sqlalchemy.Engine):
    with database.connect() as connection:
        question = options.get("question")
        answer = options.get("answer")
        latest_vote = connection.execute(sqlalchemy.text("SELECT votes.id, votes.subject\
                        FROM votes ORDER BY id DESC LIMIT 1")).fetchone()
        if latest_vote:
            answers = connection.execute(sqlalchemy.text(f"SELECT vote_answers.id, vote_answers.text, vote_answers.votes\
                            FROM vote_answers WHERE vote_answers.vote_id = '{latest_vote[0]}' LIMIT 4")).fetchall()
            return "".join((
                f"<VOTING>",
                f"#font(GC12,R2C12,RC12)",
                f"#txt[%ANS0](%B_VOTE[x:5,y:3,w:100%-10,h:14],{{}},\"{latest_vote[1]}\")",
                "".join([
                f'#apan[%PAN{idx+1}](%B_VOTE[x:0-3,y:%ANS0+{idx*14},w:100%-4,h:13],{{GW|open&voting.dcml\\00&question={latest_vote[1]}^answer={answer[0]}\\00|LW_lockall}},14,\"\")\
                #font(R2C12,R2C12,RC12)\
                #txt[%ANS{idx+1}](%B_VOTE[x:0,y:%ANS0+{idx*14}+1,w:100%,h:20],{{}},\"{idx+1}. {answer[1]} \")\
                #ctxt[%RES{idx+1}](%B_VOTE[x:105,y:%ANS0+{idx*14}+1,w:40,h:20],{{}},\"{answer[2]}\")'
                for idx, answer in enumerate(answers)]),
                "#font(RC12,R2C12,RC12)",
                "#txt[%VIEW](%B_VOTE[x:5,y:100%-17,w:100%,h:20],{GW|open&voting_view.dcml\\00|LW_lockall},\"{View all votes}\")",
                f"<VOTING>"
            ))
        else:
            return "".join((
                f"<VOTING>",
                f"<VOTING>"
            ))
