from src.game.tablero import Tablero
from src.game.jugador import Jugador
from src.game.dado import Dice

class BackgammonGame:
    """Clase principal que maneja la lógica y el estado de la partida."""
    def __init__(self, name_p1="Jugador 1", name_p2="Jugador 2"):
        """Inicializa el tablero, los dados, los jugadores y el turno."""
        self.__board__ = Tablero()
        self.__dice__ = Dice()
        self.__players__ = [
            Jugador(name_p1, "B"),
            Jugador(name_p2, "N")
        ]
        self.__turno__ = 0
        self.__dados_restantes__ = []

    def obtener_jugador_actual(self):
        """Retorna el objeto Jugador cuyo turno es actualmente."""
        player_index = self.__turno__ % 2
        return self.__players__[player_index]

    def tirar_dados(self):
        """Tira los dados y establece los valores disponibles para el turno."""
        self.__dados_restantes__ = list(Dice.get_dice())
        return self.__dados_restantes__
    
    def validar_movimiento(self, start_point: int, end_point: int) -> bool:
        """Verifica si un movimiento de start_point a end_point es legal."""
        player = self.obtener_jugador_actual()       
        is_white = (player.__ficha__ == "B") 
        ficha_count_start = self.__board__.__puntos__[start_point]
        if is_white and ficha_count_start <= 0:
            return False 
        if not is_white and ficha_count_start >= 0:
            return False           
        distance = end_point - start_point 
        if is_white and distance >= 0:
            return False
        if not is_white and distance <= 0:
            return False       
        required_distance = abs(distance)       
        if required_distance not in self.__dados_restantes__:
            return False 
        ficha_count_end = self.__board__.__puntos__[end_point]
        if is_white:
            if ficha_count_end <= -2:
                return False 
        else:
            if ficha_count_end >= 2:
                return False        
        return True    