from __future__ import annotations


def get_game_type(game_type: int):
    if game_type in range(0, len(GameTypes.types)):
        return GameTypes.types[game_type]
    return GameTypes.types[0]


class GameTypes:

    class GameType:
        def __init__(
            self,
                name: str) -> None:
            self.name = name

    GAMETYPE_NORMAL = GameType(name="Normal")
    GAMETYPE_RANKED = GameType(name="Ranked")

    types = [GAMETYPE_NORMAL, GAMETYPE_RANKED]

    def __init__(self) -> None:
        self.__nextcurrent__ = 0
        self.typeslen = len(self.types)

    def __iter__(self):
        return self

    def __next__(self):

        if self.__nextcurrent__ < self.typeslen:
            self.__nextcurrent__ += 1
            return self.types[self.__nextcurrent__-1]
        raise StopIteration


class Lobby:

    def __init__(
        self,
        host: Player,
        max_players: int,
        password: str,
        game_title: str,
        lobby_id: int,
        game_type: GameTypes.GameType = GameTypes.GAMETYPE_NORMAL
    ):

        self.host = host
        self.__players__ = []
        self.max_players = max_players
        self.game_type = game_type
        self.password = password
        self.game_title = game_title
        self.reported_player_count = 0
        self.lobby_id = lobby_id
        self.has_begun = False
        self.ip_address = host.ip_address

    def get_players(self):
        return self.__players__

    def get_reported_player_count(self):
        return self.reported_player_count

    def set_reported_player_count(self, count: int):
        self.reported_player_count = count

    def get_player_count(self):
        return len(self.__players__)

    def remove_player(self, player: Player):

        try:
            self.__players__.pop(self.__players__.index(player))

        except IndexError:
            pass

        except ValueError:
            pass

    def add_player(self, player: Player):
        """Should not be called directly. Use GameManager to handle Lobby logic."""
        self.__players__.append(player)

    def has_password(self):
        return self.password is not None

    def is_full(self):
        return self.get_player_count() >= self.max_players


class Player:

    def __init__(
        self,
        ip_address,
        session_id: int,
        lobby: Lobby = None,
        player_name: str = 'Player',
    ):

        self.ip_address = ip_address
        self.session_id = session_id
        self.player_name = player_name
        self.lobby_id = -1
        self.lobby = lobby
        self.packet_ordinal = 0
        self.game_version = 0
        self.lobby_sorting = None
        self.lobby_resort = False

    def __str__(self):
        return str(self.session_id) + " " + str(self.ip_address)

def join_lobby(target_lobby: Lobby, player: Player):
    target_lobby.add_player(player)


class GameManager:

    sid = lid = 0
    lobbies = {}  # LID: LOBBYOBJ
    players = {}  # SID: PLAYEROBJ

    def __init__(self) -> None:
        pass

    def create_lobby(
        self,
        host: Player,
        max_players: int,
        password: str,
        game_title: str,
            game_type: GameTypes.GameType = GameTypes.GAMETYPE_NORMAL) -> int:

        self.lobbies[self.lid] = Lobby(
            host=host,
            max_players=max_players,
            password=password,
            game_title=game_title,
            lobby_id=self.lid,
            game_type=game_type,
            )
        self.player_connect(host, self.lobbies[self.lid])
        self.lid += 1
        return self.lid-1

    def __close_lobby(self, lobby: Lobby):
        try:
            del self.lobbies[lobby.lobby_id]

        except KeyError:
            pass

    def leave_lobby(self, player: Player):

        if player.lobby is not None:

            if player == player.lobby.host:
                self.__close_lobby(player.lobby)

            else:
                player.lobby.remove_player(player)

    def player_disconnect(self, player: Player):

        try:
            self.leave_lobby(player)
            self.players.pop(player.session_id)

        except KeyError:
            pass

    def player_connect(self, player: Player, lobby: Lobby):
        self.leave_lobby(player)
        player.lobby = lobby
        lobby.add_player(player)

    def does_exist(self, lid: int):
        if lid in self.lobbies:
            return True
        return False

    def get_lobbies(self, order:str=None, resort:bool=False):
        if order is None:
            pass
        elif order == "r.title": # r.title - room title
            return dict(sorted(self.lobbies.items(), key=lambda x: x[1].game_title, reverse=resort))
        elif order == "t.name": # t.name - game type name
            return dict(sorted(self.lobbies.items(), key=lambda x: x[1].game_type.name, reverse=resort))
        elif order == "u.nick": # u.nick - host nick
            return dict(sorted(self.lobbies.items(), key=lambda x: x[1].host.player_name, reverse=resort))
        return self.lobbies

    def get_lobby(self, lid: int) -> Lobby:
        if lid in self.lobbies:
            return self.lobbies[lid]
