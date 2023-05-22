from datetime import datetime
import packets
import common
import classes
from classes import getGameType
import config
import dcml


class Object():
    pass


def processRequest(command, parameters, player: classes.Player, gamemanager: classes.GameManager):
    responseParameters = []
    responseCommand = "LW_show"
    
    if player.sessionID == b'0':
        responseParameters.append([responseCommand, "exec(LW_key&#CANCEL)"])

    elif command == "setipaddr":
        return

    elif command == "leave":
        gamemanager.leaveLobby(player)
        return

    elif command == "start":
        if player.lobby:
            player.lobby.hasBegun = True
        return

    elif command == "url":
        responseCommand = "LW_time"
        returl = "open:" + parameters[0].decode('utf8')
        return [[responseCommand, "0", returl]]

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
            responseParameters.append([responseCommand, browser(options, gamemanager, player)])

        elif request == "cancel.dcml":
            responseParameters.append([responseCommand, common.getFile(request)])

        elif request == "startup.dcml":
            responseParameters.append([responseCommand, common.getFile(request)])

        elif request == "voting.dcml":
            responseParameters.append([responseCommand, voting(options)])

        elif request == "demologin.dcml":
            responseParameters.append([responseCommand, dcml.login()])

        elif request == "games.dcml":
            responseParameters.append([responseCommand, browser(options, gamemanager, player)])

        elif request == "joinGame.dcml":
            responseParameters.append([responseCommand, joinGame(player, options, gamemanager)])

        elif request == "new_game_dlg.dcml":
            responseParameters.append([responseCommand, newGameDlg(player, options)])

        elif request == "new_game_dlg_create.dcml":
            responseParameters.append([responseCommand, createGame(player, options, gamemanager)])

        else:
            responseParameters.append([responseCommand, common.getFile("cancel.dcml")])

    else:
        raise ValueError

    return responseParameters


def createGame(host: classes.Player, options: dict, gamemanager: classes.GameManager):

    lobbyID = gamemanager.createLobby(
        host=host,
        maxPlayers=int(options['max_players'])+2,
        password=options['password'],
        gameTitle=options['title'],
        gameType=getGameType(int(options['type']))
    )

    output = common.getFile("new_game_dlg_create.dcml")\
        .replace("MAXPLAYERS", options['max_players'])\
        .replace("LOBBYID", lobbyID)\
        .replace("GAMETITLE", options['title'])

    return output


def joinGame(player: classes.Player, options, gamemanager: classes.GameManager):

    lobby = gamemanager.getLobby(options["id_room"])
    if lobby:
        if lobby.isFull():
            return common.getFile("lobby_full.dcml")
        elif lobby.host.sessionID == player.sessionID:
            return common.getFile("join_game_own.dcml")\
                .replace("LOBBY_ID", options["id_room"])
        else:
            if lobby.password:
                if options.get("password", "") == "":
                    return common.getFile("password_prompt.dcml")\
                        .replace("LOBBYID", options["id_room"])
                elif options.get("password", "") != lobby.password:
                    return common.getFile("incorrect_password.dcml")
            gamemanager.joinLobby(lobby, player)
            return common.getFile("join_game.dcml")\
                .replace("LOBBYID", options["id_room"])\
                .replace("MAXPLAYERS", str(lobby.maxPlayers))\
                .replace("GAMEHOST", lobby.host.nickname)\
                .replace("IPADDR", lobby.ipAddress[0])\
                .replace("PORT", str(config.TCPPORT))
    return common.getFile("join_game_incorrect.dcml").replace("LOBBY_ID", options["id_room"])


def browser(options: dict, gamemanager: classes.GameManager, player: classes.Player):
    lobbies = gamemanager.getLobbies(player.lobbySorting, player.lobbyResort)
    lastupdate = datetime.now()
    lastupdate = lastupdate.strftime("%H:%M:%S")
    entrypos = 0
    currlobby = 0
    buttonstring = ""
    pingstring = ""
    newlobbystring = common.getFile("dbtbl.dcml")
    newlobbystring = newlobbystring.replace("//LASTUPDATE", lastupdate)
    for (lid, lobby) in lobbies.items():
        buttonstringtemp = \
            f"#apan[%APAN{str(currlobby)}](%SB[x:0,y:{str(entrypos)}-2,w:100%,h:20],"\
            f"{{GW|open&joinGame.dcml\\00&delete_old=true^id_room={str(lid)}\\00|LW_lockall}},8)"\
            f"#font(BC12,BC12,BC12)"\
            f"#ping[%PING{str(currlobby)}](%SB[x:86%+30,y:{str(entrypos)}+4,w:14,h:20],"\
            f"{common.reverse_address(lobby.ipAddress)})"
        buttonstring += buttonstringtemp
        entrypos += 21
        pingstringtemp = \
            f',21,"{lobby.gameTitle + (lambda : "  *password*  " if lobby.password != "" else "")()}",'\
            f'"{lobby.host.nickname}",'\
            f'"{lobby.gameType.name}",'\
            f'"{str(lobby.getPlayerCount())}/{str(lobby.maxPlayers)}",'\
            '""'
        currlobby += 1
        pingstring += pingstringtemp
    newlobbystring = newlobbystring\
        .replace("//BUTTONSTRING", buttonstring)\
        .replace("//PINGSTRING", pingstring)
    return newlobbystring


def newGameDlg(player: classes.Player, options: dict):
    return common.getFile("new_game_dlg.dcml")\
        .replace("NICKNAME", player.nickname) \
        .replace("//TYPES", "".join([f'{_type.name},' for _type in classes.GameTypes.types]))


def voting(options: dict):
    question = options.get("question")
    answer = options.get("answer")
    return common.getFile("voting.dcml")
