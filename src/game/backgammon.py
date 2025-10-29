from src.game.tablero import Tablero
from src.game.jugador import Jugador
from src.game.dado import Dice
from src.game.checker import Checker


class BackgammonGame:
    """Clase principal que maneja la lógica y el estado de la partida."""

    def __init__(self, name_p1="Jugador 1", name_p2="Jugador 2"):
        """Inicializa el tablero, los dados, los jugadores y el turno."""
        self.__board__ = Tablero()
        self.__dice__ = Dice()
        self.__players__ = [Jugador(name_p1, "W"), Jugador(name_p2, "B")]
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

        if start_point < -1 or start_point > 24 or end_point < -1 or end_point > 25:
            return False

        player = self.obtener_jugador_actual()
        player_color = player.__ficha__
        is_white = player_color == "W"

        has_bar_checkers = (len(self.__board__.__bar_blancas__) > 0 and is_white) or (
            len(self.__board__.__bar_negras__) > 0 and not is_white
        )

        is_bearing_off_move = (is_white and end_point == -1) or (
            not is_white and end_point == 25
        )
        is_bar_move = (is_white and start_point == 24) or (
            not is_white and start_point == -1
        )

        if is_bearing_off_move:
            if has_bar_checkers:
                return False
            if not self.__board__._is_home_board_ready(player_color):
                return False

            if is_white:
                required_distance = start_point + 1
            else:
                required_distance = 24 - start_point

            if required_distance in self.__dados_restantes__:
                return True

            available_dice = [
                d for d in self.__dados_restantes__ if d >= required_distance
            ]
            if not available_dice:
                return False

            is_farthest = True
            if is_white:
                check_range = range(start_point + 1, 6)
            else:
                check_range = range(18, start_point)

            for point_index in check_range:
                point_list = self.__board__.__puntos__[point_index]
                if point_list and point_list[0].get_color() == player_color:
                    is_farthest = False
                    break

            if is_farthest:
                return True

            return False

        elif is_bar_move:
            if not has_bar_checkers:
                return False
            if is_white:
                required_distance = 24 - end_point
            else:
                required_distance = end_point + 1

        else:
            if has_bar_checkers:
                return False

            if start_point == 24 or start_point == -1:
                return False

            start_list = self.__board__.__puntos__[start_point]
            if not start_list or start_list[0].get_color() != player_color:
                return False

            distance = end_point - start_point
            if is_white and distance >= 0:
                return False
            if not is_white and distance <= 0:
                return False
            required_distance = abs(distance)

        if required_distance not in self.__dados_restantes__:
            return False

        end_list = self.__board__.__puntos__[end_point]
        if end_list:
            opponent_color = "B" if is_white else "W"
            if end_list[0].get_color() == opponent_color and len(end_list) >= 2:
                return False
        return True

    def ejecutar_movimiento(self, start_point: int, end_point: int):
        """Aplica el movimiento al tablero y consume el dado utilizado."""

        player_color = self.obtener_jugador_actual().__ficha__
        is_white = player_color == "W"
        is_bearing_off_move = (is_white and end_point == -1) or (
            not is_white and end_point == 25
        )

        if self.validar_movimiento(start_point, end_point):

            if not is_bearing_off_move:
                end_list = self.__board__.__puntos__[end_point]
                if end_list and end_list[0].get_color() != player_color:
                    self.__board__.hit_opponent(end_point)

            self.__board__.mover_ficha(start_point, end_point)

            if start_point == 24:
                distance = 24 - end_point
            elif start_point == -1:
                distance = end_point + 1
            elif is_bearing_off_move:
                if is_white:
                    required_distance = start_point + 1
                else:
                    required_distance = 24 - start_point

                used_dice = required_distance
                if required_distance not in self.__dados_restantes__:
                    possible_dice = [
                        d for d in self.__dados_restantes__ if d >= required_distance
                    ]
                    if possible_dice:
                        used_dice = min(possible_dice)
                    else:
                        raise Exception("Lógica de dados de Bear Off inconsistente.")
                distance = used_dice
            else:
                distance = abs(end_point - start_point)
            try:
                self.__dados_restantes__.remove(distance)
            except ValueError:
                if is_bearing_off_move:
                    try:
                        possible_dice = [
                            d
                            for d in self.__dados_restantes__
                            if d >= required_distance
                        ]
                        if possible_dice:
                            self.__dados_restantes__.remove(min(possible_dice))
                        else:
                            pass
                    except ValueError:
                        pass
                else:
                    pass

        else:
            raise ValueError("Movimiento inválido según las reglas del Backgammon.")

    def check_victory(self) -> bool:
        """Verifica si el jugador actual ha ganado."""
        player_color = self.obtener_jugador_actual().__ficha__
        return self.__board__.get_piece_count(player_color) == 0
