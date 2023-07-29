from ..classes import GameManager, Player
from collections import defaultdict
from .dcml.log_user import log_user
from .dcml.log_conf_dlg import log_conf_dlg
from .dcml.change import change
from .dcml.change_account2 import change_account2
from .dcml.new_game_dlg import new_game_dlg
from .dcml.startup import startup
from .dcml.games import games
from .dcml.cancel import cancel
from .dcml.news import news
from .dcml.users_list import users_list
from .dcml.log_new_form import log_new_form
from .dcml.dbtbl import dbtbl
from .dcml.voting_view import voting_view
from .dcml.voting import voting
from .dcml.reg_new_user import reg_new_user
from .dcml.join_game import join_game
from .dcml.punishments import punishments
from .dcml.forum import forum
from .dcml.forum_add import forum_add
from .dcml.forum_search import forum_search

from .helpers.create_game import create_game
from .helpers.login import login
from .helpers.critical_error import critical_error
from .helpers.leave_lobby import leave_lobby
import sqlalchemy

def processRequest(request, database: sqlalchemy.Engine, address):
    print(request)
    command, parameters, options, player_id = request[0], request[1], request[2], request[-1].decode()
    responseParameters = []
    if command == "setipaddr":
        lobby_id, ip, port = request[1].decode(), *request[2].decode().split(':')
        
        with database.connect() as connection:
            connection.execute(sqlalchemy.text(f"UPDATE lobbies SET ip = '{ip}' WHERE host_id = {lobby_id}"))
            connection.commit()
        return

    elif command == "leave":
        leave_lobby(player_id, database)

    elif command == "start":
        # if player.lobby:
        #     player.lobby.hasBegun = True
        return

    elif command == "url":
        url = parameters.decode()
        return [["LW_time", "0", "open:" + url]]

    elif command == "gmalive":
        return

    elif command == "stats":
        return

    elif command == "endgame":
        return

    elif command == "alive":
        # if player.lobby:
        #     player.lobby.setReportedPlayerCount(int.from_bytes(parameters[0:1]))
        return

    elif command == "login":
        responseParameters.append(["LW_show", login(parameters.decode(), database)])

    elif command == "open":
            request = parameters.decode()
            opts = defaultdict(lambda: None)
            for option in options.decode().split(sep="^"):
                t = (option.strip("'").split(sep="="))
                if len(t) == 2:
                    opts[t[0]] = t[1]
            try:

                if request == "log_user.dcml":
                    responseParameters.append(["LW_show", log_user(opts, database)])

                elif request == "log_conf_dlg.dcml":
                    responseParameters.append(["LW_show", log_conf_dlg(opts)])

                elif request == "dbtbl.dcml":
                    responseParameters.append(["LW_show", dbtbl(database)])

                elif request == "cancel.dcml":
                    responseParameters.append(["LW_show", cancel()])

                elif request == "startup.dcml":
                    responseParameters.append(["LW_show", startup()])

                elif request == "voting.dcml":
                    responseParameters.append(["LW_show", voting(opts, database)])

                elif request == "voting_view.dcml":
                    responseParameters.append(["LW_show", voting_view(database)])

                elif request == "reg_new_user.dcml":
                    responseParameters.append(["LW_show", reg_new_user(opts, database)])

                elif request == "games.dcml":
                    responseParameters.append(["LW_show", games()])

                elif request == "change.dcml":
                    responseParameters.append(["LW_show", change(opts)])

                elif request == "change_account2.dcml":
                    responseParameters.append(["LW_show", change_account2()])

                elif request == "log_new_form.dcml":
                    responseParameters.append(["LW_show", log_new_form(opts, database)])

                elif request == "news.dcml":
                    responseParameters.append(["LW_show", news(database)])

                elif request == "users_list.dcml":
                    responseParameters.append(["LW_show", users_list(opts, database)])

                elif request == "join_game.dcml":
                    responseParameters.append(["LW_show", join_game(opts, database)])

                elif request == "new_game_dlg.dcml":
                    leave_lobby(player_id, database)
                    responseParameters.append(["LW_show", new_game_dlg(database)])

                elif request == "punishments.dcml":
                    responseParameters.append(["LW_show", punishments(database)])

                elif request == "forum.dcml":
                    responseParameters.append(["LW_show", forum(opts, database, player_id)])

                elif request == "forum_add.dcml":
                    responseParameters.append(["LW_show", forum_add(opts, database, player_id)])

                elif request == "forum_search.dcml":
                    responseParameters.append(["LW_show", forum_search()])

                elif request == "new_game_dlg_create.dcml":
                    responseParameters.append(["LW_show", create_game(opts, player_id, address, database)])

                else:
                    responseParameters.append(["LW_show", cancel()])

            except PermissionError:
                responseParameters.append(["LW_show", critical_error(request)])

    return responseParameters