from __future__ import annotations


class GameTypes:

    class GameType:
        def __init__(
            self,
                name: str) -> None:
            self.name = name

    NORMAL = GameType(name="Normal")
    RANKED = GameType(name="Ranked")

    types = [NORMAL, RANKED]

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

    def getGameType(gameType: int):
        if gameType in range(0, len(GameTypes.types)):
            return GameTypes.types[gameType]
        return GameTypes.types[0]


class Lobby:
    def __init__(self, 
                 host: Player, 
                 maxPlayers: int, 
                 password: str = None, 
                 gameTitle: str = "A game lobby", 
                 gameType: GameTypes.GameType = GameTypes.NORMAL):
        self.host = host
        self.__players__ = []
        self.maxPlayers = maxPlayers
        self.gameType = gameType
        self.password = password
        self.gameTitle = gameTitle
        self.reportedPlayerCount = 0
        self.hasBegun = False
        self.ipAddress = host.ipAddress

    def getPlayers(self) -> list:
        '''
                Returns:
                        Players (list): A list of Players present in the lobby.
        '''
        return self.__players__

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

    def getPlayerCount(self):
        '''
                Returns:
                        Player Count (int): Player count of the lobby known to the server.
        '''
        return len(self.__players__)

    def __addPlayer(self, player: Player):
        self.__players__.append(player)

    def hasPassword(self):
        return self.password is not None

    def isFull(self):
        return self.getPlayerCount() >= self.maxPlayers


class Player:
    def __init__(self, 
                 ipAddress, 
                 sessionID: str, 
                 lobby: Lobby = None, 
                 playerName: str = 'Player'):
        self.ipAddress = ipAddress
        self.sessionID = sessionID
        self.playerName = playerName
        self.lobby = lobby
        self.packetOrdinal = 0
        self.gameVersion = 0
        self.lobbySorting = None
        self.lobbyResort = False

    def __str__(self):
        return str(self.sessionID) + " " + str(self.ipAddress)

    def joinLobby(self, gameManager: GameManager, lobbyID: str):
        gameManager.__joinToLobby(self, lobbyID)

    def leaveLobby(self, gameManager: GameManager):
        try:
            if self == self.lobby.host:
                gameManager.__closeLobby(self.lobby)
            else:
                self.__players__.pop(self.__players__.index(self))

        except IndexError:
            pass

        except ValueError:
            pass

        gameManager.__leaveLobby(self)


class GameManager:

    def __init__(self):
        self.lobbies = {}  # LobbyID: Lobby Object
        self.players = {}  # SessionID: Player Object


    def __contains__(self, LobbyID: str):
        return LobbyID in self.lobbies

    def createLobby(self, 
                    host: Player, 
                    maxPlayers: int, 
                    password: str = None, 
                    gameTitle: str = "", 
                    gameType: GameTypes.GameType = GameTypes.NORMAL
                    ) -> int:
        
        from common import genID
        LobbyID = genID()

        self.lobbies[LobbyID] = Lobby(
            host=host, 
            maxPlayers=maxPlayers, 
            password=password, 
            gameTitle=gameTitle, 
            gameType=gameType
            )
        
        self.__joinToLobby(host, self.lobbies[LobbyID])

    def __closeLobby(self, LobbyId: str):
        try:
            del self.lobbies[LobbyId]
        except KeyError:
            pass

    def __joinToLobby(self, player: Player, lobby: Lobby):
        self.__leaveLobby(player)
        player.lobby = lobby
        lobby.__addPlayer(player)

    def __leaveLobby(self, player: Player):
        try:
            self.players.pop(player.sessionID)
        except KeyError:
            pass

    def getLobbies(self, order: str = None, resort: bool = False):
        if order is None:
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
