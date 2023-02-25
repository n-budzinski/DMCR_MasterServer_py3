from datetime import datetime
import pkt
import utils
import classes
from classes import get_game_type
from main import SETTINGS


HOST = SETTINGS["HOST"]
IRC_CHAT_ADDRESS = SETTINGS["IRC_CHAT_ADDRESS"]
TCP_PORT = SETTINGS["TCP_PORT"]


def process_request(data, player: classes.Player, gamemanager):
    response_parameters = []
    header, data = pkt.unpack(data)
    reqfunction = data[0][0]
    parameters = data[0][1]
    request = parameters[0].decode()

    retaction = "LW_show"
    magic_bytes = parameters[len(parameters) - 2].decode()

    if player.packet_ordinal != header.packet_ordinal:
        player.packet_ordinal = header.packet_ordinal
        return response_parameters.append(["LW_show", "<NGDLG>#exec(GW|open&log_user.dcml\\00&VE_NICK=<%GV_VE_NICK>\\00<NGDLG>"])

    # if player.session_id == b'0':
    #     player.session_id = int(parameters[len(parameters)-1])
    #     response_parameters.append([retaction, "exec(LW_key&#CANCEL)"])

    elif reqfunction == "setipaddr":
        return

    elif reqfunction == "leave":
        gamemanager.leave_lobby(player)
        return

    elif reqfunction == "start":
        player.lobby.has_begun = True
        return

    elif reqfunction == "url":
        retaction = "LW_time"
        returl = "open:" + parameters[0].decode('utf8')
        return pkt.pack([[retaction, "0", returl]], magic_bytes)

    elif reqfunction == "gmalive":
        return

    elif reqfunction == "stats":
        return

    elif reqfunction == "endgame":
        gamemanager.leave_lobby(player)
        return

    elif reqfunction == "alive":
        if gamemanager.does_exist(player.lobby_id):
            player.lobby.set_reported_player_count(int.from_bytes(parameters[0][0:1], 'little'))
        return

    elif reqfunction == "login":
        gamemanager.leave_lobby(player)
        response_parameters.append([retaction, utils.get_file("demologin.dcml")])

    elif reqfunction == "open":

        options = parameters[1].decode(pkt.ENCODING).split(sep="^")

        if request == "log_user.dcml":
            response_parameters.append([retaction, log_user(player, options, gamemanager)])

        elif request == "log_conf_dlg.dcml":
            response_parameters.append([retaction, utils.get_file(request)])

        elif request == "dbtbl.dcml":
            response_parameters.append([retaction, browser_get(options, gamemanager, player)])

        elif request == "cancel.dcml":
            response_parameters.append([retaction, utils.get_file(request)])

        elif request == "startup.dcml":
            response_parameters.append([retaction, utils.get_file(request)])

        elif request == "voting.dcml":
            response_parameters.append([retaction, voting(options)])

        elif request == "games.dcml":
            response_parameters.append([retaction, browser_get(options, gamemanager, player)])

        elif request == "join_game.dcml":
            response_parameters.append([retaction, join_game(player, options, gamemanager)])

        elif request == "new_game_dlg.dcml":
            # gamemanager.leave_lobby(player)
            response_parameters.append([retaction, new_game_dlg(player, options)])

        elif request == "new_game_dlg_create.dcml":
            # gamemanager.leave_lobby(player)
            response_parameters.append([retaction, create_game(player, options, gamemanager)])

        else:
            response_parameters.append([retaction, utils.get_file("cancel.dcml")])

    else:
        raise ValueError

    return pkt.pack(response_parameters, magic_bytes)


def create_game(host: classes.Player, options: list, gamemanager: classes.GameManager):
    max_players = None
    game_type = None
    game_password = None
    game_title = None

    for option in options:
        option = option.strip("'")

        if option.startswith("max_players="):
            max_players = int(option[12:])+2
            if max_players > 7:
                max_players = 7

        elif option.startswith("type="):
            game_type = get_game_type(game_type=int(option[5:]))

        elif option.startswith("password="):
            if len(option[9:]) > 1:
                game_password = option[9:]

        elif option.startswith("title="):
            game_title = option[6:]
            if len(game_title) < 3 or not game_title.isalnum():
                return utils.get_file("new_game_dlg.dcml")

    if None in [max_players, game_type, game_title]:
        return utils.get_file("cancel.dcml")

    lid = gamemanager.create_lobby(
        host=host,
        max_players=max_players,
        password=game_password,
        game_title=game_title,
        game_type=game_type
        )

    output = utils.get_file("new_game_dlg_create.dcml")\
        .replace("MAXPLAYERS", str(max_players))\
        .replace("LOBBYID", str(lid))\
        .replace("GAMETITLE", game_title)

    return output


def join_game(player: classes.Player, options, gamemanager: classes.GameManager):
    lobby = None
    delete_old = False
    lobby_id = None
    password = None

    for option in options:
        option = option.strip("'")
        if option.startswith("delete_old="):
            delete_old = option[11:]
        elif option.startswith("id_room="):
            lobby_id = int(option[8:])
        elif option.startswith("password="):
            if len(option[9:]) > 1:
                password = str(option[9:])

    lobby = gamemanager.get_lobby(lobby_id)
    if lobby:
        if lobby.is_full():
            return utils.get_file("lobby_full.dcml")
        elif lobby.host.session_id == player.session_id:
            return utils.get_file("join_game_own.dcml")\
                .replace("LOBBY_ID", str(lobby_id))
        else:
            if lobby.password:
                if password is None:
                    return utils.get_file("password_prompt.dcml")\
                        .replace("LOBBYID", lobby_id)
                elif password != lobby.password:
                    return utils.get_file("incorrect_password.dcml")
            gamemanager.player_connect(player, lobby)
            return utils.get_file("join_game.dcml")\
                .replace("LOBBYID", str(lobby_id))\
                .replace("MAXPLAYERS", str(lobby.max_players))\
                .replace("GAMEHOST", lobby.host.player_name)\
                .replace("IPADDR", lobby.ip_address[0])\
                .replace("PORT", str(TCP_PORT))
    return utils.get_file("join_game_incorrect.dcml").replace("LOBBY_ID", str(lobby_id))


def browser_get(options: list, gamemanager:classes.GameManager, player:classes.Player):

    """Handles dbtbl (available lobby table) calls."""
    order = None
    # resort = False

    for option in options:
        option = option.strip("'")
        if option.startswith("order="):
            order = option[6:]
            if order != "r.hbtime":
                player.lobby_sorting = order
                if order == player.lobby_sorting:
                    player.lobby_resort = not player.lobby_resort

        # elif option.startswith("resort="):
        #     if option[7:]:
        #         resort = True

    lobbies = gamemanager.get_lobbies(player.lobby_sorting, player.lobby_resort)
    lastupdate = datetime.now()
    lastupdate = lastupdate.strftime("%H:%M:%S")
    entrypos = 0
    currlobby = 0
    buttonstring = ""
    pingstring = ""
    newlobbystring = utils.get_file("dbtbl.dcml")
    newlobbystring = newlobbystring.replace("//LASTUPDATE", lastupdate)
    for (lid, lobby) in lobbies.items():
        buttonstringtemp = \
            f"#apan[%APAN{str(currlobby)}](%SB[x:0,y:{str(entrypos)}-2,w:100%,h:20],"\
            f"{{GW|open&join_game.dcml\\00&delete_old=true^id_room={str(lid)}\\00|LW_lockall}},8)"\
            f"#font(BC12,BC12,BC12)"\
            f"#ping[%PING{str(currlobby)}](%SB[x:86%+30,y:{str(entrypos)}+4,w:14,h:20],"\
            f"{utils.reverse_address(lobby.ip_address)})"
        buttonstring += buttonstringtemp
        entrypos += 21
        pingstringtemp = \
            f',21,"{lobby.game_title + (lambda : "  *password*  " if lobby.password is not None else "")()}",'\
            f'"{lobby.host.player_name}",'\
            f'"{lobby.game_type.name}",'\
            f'"{str(lobby.get_player_count())}/{str(lobby.max_players)}",'\
            '""'
        currlobby += 1
        pingstring += pingstringtemp
    newlobbystring = newlobbystring\
        .replace("//BUTTONSTRING", buttonstring)\
        .replace("//PINGSTRING", pingstring)
    return newlobbystring


def new_game_dlg(player: classes.Player, options: list):
    delete_old = None
    for option in options:
        option = option.strip("'")
        if option.startswith("delete_old="):
            delete_old = option[11:]
    return utils.get_file("new_game_dlg.dcml")\
        .replace("NICKNAME", player.player_name) \
        .replace("//TYPES", "".join([f'{_type.name},' for _type in classes.GameTypes.types]))


def voting(options: list):
    question = None
    answer = None
    for option in options:
        option = option.strip("'")
        if option.startswith("question="):
            question = option[9:]
        elif option.startswith("answer="):
            answer = option[7:]
    return utils.get_file("voting.dcml")


def log_user(player: classes.Player, options, gamemanager):
    ve_nick = None
    gamemanager.leave_lobby(player)
    for option in options:
        option = option.strip("'")
        if option.startswith("VE_NICK="):
            player.player_name = option[8:]
    if len(player.player_name) < 3 or not utils.check_alpha(player.player_name):
        return utils.get_file("log_user_bad.dcml")
    return utils.get_file("log_user.dcml")\
        .replace("NICKNAME", player.player_name)\
        .replace("PLAYERID", str(player.session_id)) \
        .replace("CHAT_ADDRESS", IRC_CHAT_ADDRESS)
