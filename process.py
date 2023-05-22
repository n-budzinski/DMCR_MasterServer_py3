
import common
import classes
import dcml.dcml as dcml

class Object():
    pass

def processRequest(command, parameters, player: classes.Player, gamemanager: classes.GameManager):
    responseParameters = []
    responseCommand = "LW_show"
    
    if command == "setipaddr":
        return

    elif command == "leave":
        gamemanager.leaveLobby(player)
        return

    elif command == "start":
        if player.lobby:
            player.lobby.hasBegun = True
        return

    elif command == "url":
        return [["LW_time", "0", "open:" + parameters[0].decode('utf8')]]

    elif command == "gmalive":
        return

    elif command == "stats":
        return

    elif command == "endgame":
        gamemanager.leaveLobby(player)
        return

    elif command == "alive":
        if player.lobby:
            player.lobby.setReportedPlayerCount(int.from_bytes(parameters[0][0:1]))
        return

    elif command == "login":
        gamemanager.leaveLobby(player)
        # responseParameters.append([responseCommand, common.get_file("login.dcml")])
        responseParameters.append([responseCommand, dcml.login()])

    elif command == "open":
        request = parameters[0].decode()
        options = {'others': []}
        for option in parameters[1].decode().split(sep="^"):
            t = (option.strip("'").split(sep="="))
            if len(t) == 2:
                options[t[0]] = t[1]
            else:
                options["others"].append(t[0])

        if request == "log_user.dcml":
            responseParameters.append([responseCommand, dcml.logUser(gamemanager, options, player)])

        elif request == "log_conf_dlg.dcml":
            responseParameters.append([responseCommand, common.getFile(request)])

        elif request == "dbtbl.dcml":
            responseParameters.append([responseCommand, dcml.browser(gamemanager, player)])

        elif request == "cancel.dcml":
            responseParameters.append([responseCommand, dcml.cancel()])

        elif request == "startup.dcml":
            responseParameters.append([responseCommand, dcml.startup()])

        elif request == "voting.dcml":
            responseParameters.append([responseCommand, dcml.voting(options)])

        elif request == "demologin.dcml":
            responseParameters.append([responseCommand, dcml.login()])

        elif request == "games.dcml":
            responseParameters.append([responseCommand, dcml.browser(gamemanager, player)])

        elif request == "joinGame.dcml":
            responseParameters.append([responseCommand, dcml.joinGame(player, options, gamemanager)])

        elif request == "new_game_dlg.dcml":
            responseParameters.append([responseCommand, dcml.newGameDlg(player, options)])

        elif request == "new_game_dlg_create.dcml":
            responseParameters.append([responseCommand, dcml.createGame(player, options, gamemanager)])

        else:
            responseParameters.append([responseCommand, dcml.cancel()])

    else:
        raise NotImplementedError

    return responseParameters
