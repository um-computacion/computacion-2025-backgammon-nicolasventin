from src.game.tablero import Tablero
from src.game.jugador import Jugador
from src.game.dado import Dice
from .checker import Checker

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
        
        if start_point < 0 or start_point > 23 or end_point < 0 or end_point > 23:
             return False 

        player = self.obtener_jugador_actual()       
        player_color = player.__ficha__

        start_list = self.__board__.__puntos__[start_point]
        end_list = self.__board__.__puntos__[end_point]
        
        if not start_list or start_list[0].get_color() != player_color:
            return False 
        distance = end_point - start_point 
        is_white = (player_color == 'B') 

        if is_white and distance >= 0:
            return False
        if not is_white and distance <= 0:
            return False        
        required_distance = abs(distance)       
        if required_distance not in self.__dados_restantes__:
            return False 
        if end_list:
            opponent_color = 'N' if is_white else 'B'
            if end_list[0].get_color() == opponent_color and len(end_list) >= 2:
                return False 
        return True    

    def ejecutar_movimiento(self, start_point: int, end_point: int):
        """Aplica el movimiento al tablero y consume el dado utilizado."""
        
        if self.validar_movimiento(start_point, end_point):            
            self.__board__.mover_ficha(start_point, end_point)
            distance = abs(end_point - start_point)
            try:
                self.__dados_restantes__.remove(distance)
            except ValueError:
                pass
        
        else:
            raise ValueError("Movimiento inválido según las reglas del Backgammon.")