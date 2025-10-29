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

    def draw(self):
        """Devuelve la grilla del tablero (matriz 10x12) como estructura de datos."""
        height, width = 10, 12
        grid = [[" " for _ in range(width)] for _ in range(height)]

        for c in range(12):
            point = 11 - c
            owner, n = self.owner_and_count_from_puntos(point)
            if not owner or n == 0:
                continue
            piece = self.piece(owner)
            if n <= 5:
                for r in range(n):
                    grid[r][c] = piece
            else:
                for r in range(4):
                    grid[r][c] = piece
                grid[4][c] = str(n - 4)

        for c in range(12):
            point = 12 + c
            owner, n = self.owner_and_count_from_puntos(point)
            if not owner or n == 0:
                continue
            piece = self.piece(owner)
            if n <= 5:
                for k in range(n):
                    grid[9 - k][c] = piece
            else:
                for k in range(4):
                    grid[9 - k][c] = piece
                grid[5][c] = str(n - 4)

        return grid

    def mover_ficha(self, start_point: int, end_point: int):
        """Mueve una ficha de start_point a end_point. Asume que el movimiento es válido."""
        if start_point < -1 or start_point > 24:
            raise ValueError("Punto de inicio fuera de rango (-1 a 24).")
        checker_to_move = None
        if start_point == 24:
            if not self.__bar_blancas__:
                raise ValueError("No hay fichas blancas en la barra.")
            checker_to_move = self.__bar_blancas__.pop()
            checker_to_move.comida = False
        elif start_point == -1:
            if not self.__bar_negras__:
                raise ValueError("No hay fichas negras en la barra.")
            checker_to_move = self.__bar_negras__.pop()
            checker_to_move.comida = False
        else:
            start_list = self.__puntos__[start_point]
            if not start_list:
                raise ValueError("No hay fichas para mover en el punto de inicio.")
            checker_to_move = start_list.pop()
        if end_point not in (-1, 25):
            self.__puntos__[end_point].append(checker_to_move)

    def is_home_board_ready(self, color: str) -> bool:
        """Verifica si todas las fichas de un color están en el cuadrante de inicio (Home Board)."""

        if color == "W" and len(self.__bar_blancas__) > 0:
            return False
        if color == "B" and len(self.__bar_negras__) > 0:
            return False
        if color == "W":
            check_range = range(6, 24)
        else:
            check_range = range(0, 18)
        for point_index in check_range:
            point_list = self.__puntos__[point_index]
            if point_list and point_list[0].get_color() == color:
                return False
        return True

    def get_piece_count(self, color: str) -> int:
        """
        Retorna el número total de fichas de un color que 
        aún están en el tablero (puntos + barra).
        """
        count = 0

        if color == "W":
            count += len(self.__bar_blancas__)
        else:
            count += len(self.__bar_negras__)

        for point_list in self.__puntos__:
            if point_list and point_list[0].get_color() == color:
                count += len(point_list)
        return count

    def hit_opponent(self, end_point: int) -> bool:
        """Verifica si hay un hit en end_point y mueve la ficha rival a la barra."""

        point_list = self.__puntos__[end_point]

        if len(point_list) == 1:
            hit_checker = point_list.pop()
            hit_checker.comida = True
            if hit_checker.get_color() == "W":
                self.__bar_blancas__.append(hit_checker)
            elif hit_checker.get_color() == "B":
                self.__bar_negras__.append(hit_checker)

            return True

        return False

    def owner_and_count_from_puntos(self, idx: int):
        """Helper: Retorna el dueño ('white'/'black') y la cantidad de fichas en un punto."""
        point_list = self.__puntos__[idx]
        count = len(point_list)
        if count == 0:
            return (None, 0)
        owner_color = point_list[0].get_color()
        owner_str = "white" if owner_color == "W" else "black"

        return (owner_str, count)

    def piece(self, owner: str) -> str:
        """Helper: Retorna el símbolo 'W' o 'B' para la representación de datos (no visual)."""
        return "W" if owner == "white" else "B"
