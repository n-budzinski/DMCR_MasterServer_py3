from __future__ import annotations
from __future__ import absolute_import
from .common import genID

class GameTypes:
    class GameType:
        def __init__(
            self,
                name: str,
                aiEnabled: bool = False,
                allowDesigned: bool = False) -> None:
            self.name = name
            self.aiEnabled = aiEnabled
            self.allowDesigned = allowDesigned

    def __init__(self, gametypes) -> None:
        self._nextcurrent = 0
        self.types = []
        for type in gametypes:
            self.types.append(self.GameType(**type))
        self.typeslen = len(self.types)

    def getGameType(self, gameType: int):
        if gameType in range(0, len(self.types)):
            return self.types[gameType]
        return self.types[0]

    def __iter__(self):
        return self

    def __next__(self):

        if self._nextcurrent < self.typeslen:
            self._nextcurrent += 1
            return self.types[self._nextcurrent-1]
        raise StopIteration


class Lobby:
    def __init__(self,
                 host,
                 maxPlayers: int,
                 lobbyID: str,
                 gameType: GameTypes.GameType,
                 password: str = "",
                 gameTitle: str = "A game lobby)"):
        self.host = host
        self._players = []
        self.maxPlayers = int(maxPlayers)
        self.gameType = gameType
        self.password = password
        self.gameTitle = gameTitle
        self.lobbyID = lobbyID
        self.reportedPlayerCount = 0
        self.hasBegun = False
        self.ipAddress = host.ipAddress

    def getPlayers(self) -> list:
        '''
                Returns:
                        Players (list): A list of Players present in the lobby.
        '''
        return self._players

    def getReportedPlayerCount(self) -> int:
        '''
                Returns:
                        Player Count (int): Player count of the lobby reported by the host.
        '''
        return self.reportedPlayerCount

    def setReportedPlayerCount(self, count: int):
        '''
                Parameters:
                        count (str): An integer representing the current amount of players reported by the host.
        '''
        self.reportedPlayerCount = count

    def getPlayerCount(self) -> int:
        '''
                Returns:
                        Player Count (int): Player count of the lobby known to the server.
        '''
        return len(self._players)

    def _addPlayer(self, player: Player):
        self._players.append(player)

    def hasPassword(self):
        return self.password != ""

    def isFull(self):
        return self.getPlayerCount() >= self.maxPlayers


class Player:
    def __init__(self,
                 ipAddress,
                 lobby = None,
                 nickname: str = 'Player'):
        self.ipAddress = ipAddress
        self.nickname = nickname
        self.lobby = lobby
        self.language = 0
        self.profileID = "-1"
        self.lobbySorting = ""
        self.lobbyResort = False

    def __str__(self):
        return str(self.profileID) + " " + str(self.ipAddress)


class GameManager:

    def __init__(self):
        self.lobbies = {}  # LobbyID: Lobby Object
        self.players = {}  # profileID: Player Object

    def __contains__(self, LobbyID: str):
        return LobbyID in self.lobbies

    def createLobby(self,
                    host: Player,
                    maxPlayers: int,
                    gameType: GameTypes.GameType,
                    password: str = "",
                    gameTitle: str = "",
                    ) -> str:

        
        lobbyID = genID()

        self.lobbies[lobbyID] = Lobby(
            host=host,
            maxPlayers=maxPlayers,
            password=password,
            gameTitle=gameTitle,
            gameType=gameType,
            lobbyID=lobbyID
        )

        self._joinToLobby(self.lobbies[lobbyID], host)
        return lobbyID

    def _closeLobby(self, LobbyId: str):

        try:
            self.lobbies.pop(LobbyId)

        except KeyError:
            pass

    def _joinToLobby(self, lobby: Lobby, player: Player):
        if player.lobby is not None:
            self._closeLobby(player.lobby.lobbyID)
        player.lobby = lobby
        player.lobby._addPlayer(player)

    def disconnect(self, player: Player):
        try:
            self.leaveLobby(player)
            self.players.pop(player.profileID)
        except KeyError:
            pass

    def leaveLobby(self, player: Player):
        try:
            if player.lobby is not None:
                if player == player.lobby.host:
                    self._closeLobby(player.lobby.lobbyID)
                else:
                    player.lobby._players.pop(
                        player.lobby._players.index(player))

        except IndexError:
            pass

        except ValueError:
            pass

    def joinLobby(self, lobby: Lobby, player: Player):
        self._joinToLobby(lobby, player)

    def getLobbies(self, order: str, resort: bool = False):
        if order == "":
            pass
        elif order == "r.title":  # r.title - room title
            return dict(sorted(self.lobbies.items(), key=lambda x: x[1].game_title, reverse=resort))
        elif order == "t.name":  # t.name - game type name
            return dict(sorted(self.lobbies.items(), key=lambda x: x[1].game_type.name, reverse=resort))
        elif order == "u.nick":  # u.nick - host nick
            return dict(sorted(self.lobbies.items(), key=lambda x: x[1].host.player_name, reverse=resort))
        return self.lobbies

    def getLobby(self, lobbyID: str) -> Lobby:
        '''
                Parameters:
                        LobbyID (str): LobbyID of the desired lobby.

                Returns:
                        Lobby (Lobby): A requested lobby.
                        If the lobby does not exist, returns None.
        '''
        return self.lobbies.get(lobbyID, None)
