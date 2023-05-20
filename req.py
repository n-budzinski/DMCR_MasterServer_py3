from datetime import datetime
import pkt
import common
import classes
from classes import getGameType
from main import SETTINGS as set
import dcml


HOST = set["HOST"]
IRC_CHAT_ADDRESS = set["IRC_CHAT_ADDRESS"]
TCP_PORT = set["TCP_PORT"]

class Object():
    pass


def process_request(packetData, player: classes.Player, gamemanager: classes.GameManager):
    responseParameters = []
    header, data = pkt.unpack(packetData)
    requestCommand = data[0][0]
    parameters = data[0][1]
    request = parameters[0].decode()

    responseCommand = "LW_show"
    integrity = parameters[len(parameters) - 2].decode()

    if player.packetOrdinal != header.packetOrdinal:
        # player.packetOrdinal = header.packetOrdinal
        # return responseParameters.append(["LW_show", "<NGDLG>#exec(GW|open&log_user.dcml\\00&VE_NICK=<%GV_VE_NICK>\\00<NGDLG>"])
        gamemanager.leaveLobby(player)
        #responseParameters.append([responseCommand, common.get_file("login.dcml")])
        responseParameters.append([responseCommand, dcml.demoLogin()])

    if player.sessionID == b'0':
        responseParameters.append([responseCommand, "exec(LW_key&#CANCEL)"])

    elif requestCommand == "setipaddr":
        return

    elif requestCommand == "leave":
        gamemanager.leaveLobby(player)
        return

    elif requestCommand == "start":
        if player.lobby:
            player.lobby.hasBegun = True
        return

    elif requestCommand == "url":
        responseCommand = "LW_time"
        returl = "open:" + parameters[0].decode('utf8')
        return pkt.pack([[responseCommand, "0", returl]], integrity)

    elif requestCommand == "gmalive":
        return

    elif requestCommand == "stats":
        return

    elif requestCommand == "endgame":
        gamemanager.leaveLobby(player)
        return

    elif requestCommand == "alive":
        if player.lobby:
            player.lobby.setReportedPlayerCount(int.from_bytes(parameters[0][0:1], 'little'))
        return

    elif requestCommand == "login":
        gamemanager.leaveLobby(player)
        #responseParameters.append([responseCommand, common.get_file("login.dcml")])
        responseParameters.append([responseCommand, dcml.demoLogin()])

    elif requestCommand == "open":

        options = {'others':[]}
        for option in parameters[1].decode(pkt.ENCODING).split(sep="^"):
            t = (option.strip("'").split(sep="="))
            if len(t) == 2:
                options[t[0]] = t[1]
            else:
                options["others"].append(t[0])


        if request == "log_user.dcml":
            responseParameters.append([responseCommand, dcml.logUser(gamemanager, options, IRC_CHAT_ADDRESS, player)])

        elif request == "log_conf_dlg.dcml":
            responseParameters.append([responseCommand, common.get_file(request)])

        elif request == "dbtbl.dcml":
            responseParameters.append([responseCommand, browser_get(options, gamemanager, player)])

        elif request == "cancel.dcml":
            responseParameters.append([responseCommand, common.get_file(request)])

        elif request == "startup.dcml":
            responseParameters.append([responseCommand, common.get_file(request)])

        elif request == "voting.dcml":
            responseParameters.append([responseCommand, voting(options)])

        elif request == "games.dcml":
            responseParameters.append([responseCommand, browser_get(options, gamemanager, player)])

        elif request == "joinGame.dcml":
            responseParameters.append([responseCommand, joinGame(player, options, gamemanager)])

        elif request == "new_game_dlg.dcml":
            responseParameters.append([responseCommand, new_game_dlg(player, options)])

        elif request == "new_game_dlg_create.dcml":
            responseParameters.append([responseCommand, createGame(player, options, gamemanager)])

        else:
            responseParameters.append([responseCommand, common.get_file("cancel.dcml")])

    else:
        raise ValueError

    return pkt.pack(responseParameters, integrity)


def createGame(host: classes.Player, options: dict, gamemanager: classes.GameManager):

    lobbyID = gamemanager.createLobby(
        host=host,
        maxPlayers=int(options['max_players'])+2,
        password=options['password'],
        gameTitle=options['title'],
        gameType= getGameType(int(options['type']))
        )

    output = common.get_file("new_game_dlg_create.dcml")\
        .replace("MAXPLAYERS", options['max_players'])\
        .replace("LOBBYID", lobbyID)\
        .replace("GAMETITLE", options['title'])

    return output


def joinGame(player: classes.Player, options, gamemanager: classes.GameManager):

    lobby = gamemanager.getLobby(options["id_room"])
    if lobby:
        if lobby.isFull():
            return common.get_file("lobby_full.dcml")
        elif lobby.host.sessionID == player.sessionID:
            return common.get_file("join_game_own.dcml")\
                .replace("LOBBY_ID", options["id_room"])
        else:
            if lobby.password:
                if options.get("password","") is "":
                    return common.get_file("password_prompt.dcml")\
                        .replace("LOBBYID", options["id_room"])
                elif options.get("password","") != lobby.password:
                    return common.get_file("incorrect_password.dcml")
            gamemanager.joinLobby(lobby, player)
            return common.get_file("join_game.dcml")\
                .replace("LOBBYID", options["id_room"])\
                .replace("MAXPLAYERS", str(lobby.maxPlayers))\
                .replace("GAMEHOST", lobby.host.nickname)\
                .replace("IPADDR", lobby.ipAddress[0])\
                .replace("PORT", str(TCP_PORT))
    return common.get_file("join_game_incorrect.dcml").replace("LOBBY_ID", options["id_room"])


def browser_get(options: dict, gamemanager:classes.GameManager, player:classes.Player):
    lobbies = gamemanager.getLobbies(player.lobbySorting, player.lobbyResort)
    lastupdate = datetime.now()
    lastupdate = lastupdate.strftime("%H:%M:%S")
    entrypos = 0
    currlobby = 0
    buttonstring = ""
    pingstring = ""
    newlobbystring = common.get_file("dbtbl.dcml")
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


def new_game_dlg(player: classes.Player, options: dict):
    return common.get_file("new_game_dlg.dcml")\
        .replace("NICKNAME", player.nickname) \
        .replace("//TYPES", "".join([f'{_type.name},' for _type in classes.GameTypes.types]))


def voting(options: dict):
    question = options.get("question")
    answer  = options.get("answer")
    return common.get_file("voting.dcml")


# def log_user(player: classes.Player, options, gamemanager):
#     ve_nick = None
#     gamemanager.leave_lobby(player)
#     for option in options:
#         option = option.strip("'")
#         if option.startswith("VE_NICK="):
#             player.nickname = option[8:]
#     if len(player.nickname) < 3 or not common.check_alpha(player.nickname):
#         return common.get_file("log_user_bad.dcml")
#     return common.get_file("log_user.dcml")\
#         .replace("NICKNAME", player.nickname)\
#         .replace("PLAYERID", str(player.session_id)) \
#         .replace("CHAT_ADDRESS", IRC_CHAT_ADDRESS)
