from src.game.tablero import Tablero
from src.game.jugador import Jugador
from src.game.dado import Dice

class BackgammonGame:
    def __init__(self, name_p1="Jugador 1", name_p2="Jugador 2"):
        self._board = Tablero()
        self.__dice__ = Dice()
        self.__players__ = [
            Jugador(name_p1, id_=1),
            Jugador(name_p2, id_=-1)
        ]
        self.__turno__ = 0