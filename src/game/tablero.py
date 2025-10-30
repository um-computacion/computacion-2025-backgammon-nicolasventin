"""
Módulo que define la clase Tablero y su lógica interna.
"""

from .checker import Checker


class Tablero:
    """Clase que maneja el estado del tablero de Backgammon."""

    def __init__(self):
        """Inicializa el tablero con posiciones y el estado del juego."""
        self.__turnos__ = 0
        self.__puntos__: list[list[Checker]] = [[] for _ in range(24)]

        self.__bar_blancas__: list[Checker] = []
        self.__bar_negras__: list[Checker] = []

        def create_checkers(color, count):
            return [Checker(color) for _ in range(count)]

        self.__puntos__[23].extend(create_checkers("W", 2))
        self.__puntos__[12].extend(create_checkers("W", 5))
        self.__puntos__[7].extend(create_checkers("W", 3))
        self.__puntos__[5].extend(create_checkers("W", 5))

        self.__puntos__[0].extend(create_checkers("B", 2))
        self.__puntos__[11].extend(create_checkers("B", 5))
        self.__puntos__[16].extend(create_checkers("B", 3))
        self.__puntos__[18].extend(create_checkers("B", 5))

    def get_bar_count(self, color: str) -> int:
        """Retorna cuántas fichas tiene un jugador en la barra."""
        if color == "W":
            return len(self.__bar_blancas__)
        return len(self.__bar_negras__)

    def get_point_info(self, point_index: int) -> tuple[str | None, int]:
        """
        Retorna el color del dueño y la cantidad de fichas en un punto.
        (Reemplaza el acceso directo a __puntos__).
        """
        if 0 <= point_index <= 23:
            point_list = self.__puntos__[point_index]
            count = len(point_list)
            if count == 0:
                return (None, 0)
            return (point_list[0].color, count)
        return (None, 0) # Índices fuera de rango (como -1 o 24) no tienen info

    def is_point_blocked(self, point_index: int, player_color: str) -> bool:
        """Verifica si el punto está bloqueado por el oponente."""
        color_en_punto, count = self.get_point_info(point_index)
        if color_en_punto is None or color_en_punto == player_color:
            return False
        return count >= 2

    def is_point_farthest(self, point_index: int, player_color: str) -> bool:
        """Verifica si la ficha es la más alejada en el home board."""
        if player_color == "W":
            check_range = range(point_index + 1, 6)
        else:
            check_range = range(18, point_index)

        for i in check_range:
            color, count = self.get_point_info(i)
            if color == player_color and count > 0:
                return False
        return True

    def is_home_board_ready(self, color: str) -> bool:
        """Verifica si todas las fichas de un color están en el cuadrante de inicio (Home Board)."""

        if self.get_bar_count(color) > 0:
            return False
        if color == "W":
            check_range = range(6, 24)
        else:
            check_range = range(0, 18)

        for point_index in check_range:
            point_color, point_count = self.get_point_info(point_index)
            if point_color == color and point_count > 0:
                return False
        return True

    def get_piece_count(self, color: str) -> int:
        """
        Retorna el número total de fichas de un color que
        aún están en el tablero (puntos + barra).
        """
        count = self.get_bar_count(color)
        for point_list in self.__puntos__:
            if point_list and point_list[0].color == color:
                count += len(point_list)
        return count

    def hit_opponent(self, end_point: int) -> bool:
        """Verifica si hay un hit en end_point y mueve la ficha rival a la barra."""
        point_list = self.__puntos__[end_point]
        color_en_punto, count = self.get_point_info(end_point)

        if count == 1 and color_en_punto is not None:
            hit_checker = point_list.pop()
            hit_checker.comida = True
            if hit_checker.color == "W":
                self.__bar_blancas__.append(hit_checker)
            elif hit_checker.color == "B":
                self.__bar_negras__.append(hit_checker)
            return True
        return False

    def mover_ficha(self, start_point: int, end_point: int):
        """Mueve una ficha de start_point a end_point. Asume que el movimiento es válido."""
        if start_point < -1 or start_point > 24:
            raise ValueError("Punto de inicio fuera de rango (-1 a 24).")
        checker_to_move = None
        if start_point == 24:
            if not self.__bar_blancas__:
                raise ValueError("No hay fichas blancas en la barra.")
            checker_to_move = self.__bar_blancas__.pop()
        elif start_point == -1:
            if not self.__bar_negras__:
                raise ValueError("No hay fichas negras en la barra.")
            checker_to_move = self.__bar_negras__.pop()
        else:
            start_list = self.__puntos__[start_point]
            if not start_list:
                raise ValueError("No hay fichas para mover en el punto de inicio.")
            checker_to_move = start_list.pop()
        
        checker_to_move.comida = False

        if end_point not in (-1, 25):
            self.__puntos__[end_point].append(checker_to_move)
