"""
Módulo que define la clase Tablero y su lógica interna.
"""

from .checker import Checker


class Tablero:
    """Clase que maneja el estado del tablero de Backgammon."""

    def __init__(self):
        """
        Recibe:
            Nada.
        Hace:
            Inicializa el estado del juego:
            - Crea las 24 listas de puntos (`__puntos__`).
            - Crea las 2 listas de la barra (`__bar_blancas__`, `__bar_negras__`).
            - Coloca las 15 fichas Blancas ('W') y 15 Negras ('B') en sus
              posiciones iniciales estándar.
        Devuelve:
            Nada.
        """
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
        """
        Recibe:
            color (str): El color a consultar ('W' o 'B').
        Hace:
            Consulta el número de fichas en la barra para ese color.
        Devuelve:
            (int): El conteo de fichas en la barra.
        """
        if color == "W":
            return len(self.__bar_blancas__)
        return len(self.__bar_negras__)

    def get_point_info(self, point_index: int) -> tuple[str | None, int]:
        """
        Recibe:
            point_index (int): El índice del punto a consultar (0-23).
        Hace:
            Consulta el estado de un punto específico del tablero.
        Devuelve:
            (tuple): (color, count)
                     - color (str | None): El color de las fichas en el punto
                       ('W' o 'B'), o None si está vacío.
                     - count (int): El número de fichas en ese punto.
        """
        if 0 <= point_index <= 23:
            point_list = self.__puntos__[point_index]
            count = len(point_list)
            if count == 0:
                return (None, 0)
            return (point_list[0].color, count)
        return (None, 0)  # Índices fuera de rango (como -1 o 24) no tienen info

    def is_point_blocked(self, point_index: int, player_color: str) -> bool:
        """
        Recibe:
            point_index (int): El punto de destino a verificar.
            player_color (str): El color del jugador que intenta moverse.
        Hace:
            Verifica si el punto de destino está "bloqueado" (tiene 2 o
            más fichas del oponente).
        Devuelve:
            (bool): True si el punto está bloqueado, False en caso contrario.
        """
        color_en_punto, count = self.get_point_info(point_index)
        if color_en_punto is None or color_en_punto == player_color:
            return False
        return count >= 2

    def is_point_farthest(self, point_index: int, player_color: str) -> bool:
        """
        Recibe:
            point_index (int): El punto de la ficha que intenta hacer bear off.
            player_color (str): El color del jugador ('W' o 'B').
        Hace:
            Verifica si hay otras fichas del mismo color en puntos
            más alejados (con un índice mayor para 'W', menor para 'B')
            dentro del home board.
        Devuelve:
            (bool): True si esta es la ficha más alejada, False si hay
                    fichas en puntos más lejanos.
        """
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
        """
        Recibe:
            color (str): El color del jugador a verificar ('W' o 'B').
        Hace:
            Verifica si todas las 15 fichas de ese jugador están dentro
            de su "home board" (puntos 0-5 para 'W', 18-23 para 'B') y
            que no tenga fichas en la barra.
        Devuelve:
            (bool): True si el jugador está listo para hacer "bear off",
                    False en caso contrario.
        """

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
        Recibe:
            color (str): El color de las fichas a contar ('W' o 'B').
        Hace:
            Suma todas las fichas de ese color (en los 24 puntos y
            en la barra) para saber cuántas siguen en juego.
        Devuelve:
            (int): El número total de fichas de ese color (0-15).
        """
        count = self.get_bar_count(color)
        for point_list in self.__puntos__:
            if point_list and point_list[0].color == color:
                count += len(point_list)
        return count

    def hit_opponent(self, end_point: int) -> bool:
        """
        Recibe:
            end_point (int): El punto de destino donde se produce el 'hit'.
        Hace:
            Asume que el movimiento es válido. Quita la ficha oponente
            única ('blot') de ese punto, la marca como 'comida' y
            la añade a la barra correspondiente.
        Devuelve:
            (bool): True si se realizó un 'hit', False si no (aunque
                    esta implementación asumida siempre retorna True
                    si se cumplen las condiciones).
        """
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
        """
        Recibe:
            start_point (int): El punto de origen (0-23, o 24/BAR_W, -1/BAR_B).
            end_point (int): El punto de destino (0-23, o -1/OFF_W, 25/OFF_B).
        Hace:
            Realiza la acción física de mover una ficha.
            1. Saca (pop) la ficha superior del origen (sea un punto o la barra).
            2. La añade (append) al destino (sea un punto o la bandeja de bear off).
            Lanza ValueError si se intenta mover desde un origen inválido o vacío.
        Devuelve:
            Nada.
        """
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
