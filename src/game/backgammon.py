"""
Módulo principal del juego Backgammon.
Maneja la lógica de la partida, turnos y movimientos.
"""

from typing import Tuple, Optional
from src.game.tablero import Tablero
from src.game.jugador import Jugador
from src.game.dado import Dice

class BackgammonGame:
    """Clase principal que maneja la lógica y el estado de la partida."""

    def __init__(self, name_p1="Jugador 1", name_p2="Jugador 2"):
        """Inicializa el tablero, los dados, los jugadores y el turno."""
        self.__board__ = Tablero()
        self.__dice__ = Dice()
        self.__players__ = [Jugador(name_p1, "W"), Jugador(name_p2, "B")]
        self.__turno__ = 0
        self.__dados_restantes__ = []

        self.__estrategias_validacion__ = {
            "bear_off": self._validar_bear_off,
            "bar": self._validar_desde_barra,
            "normal": self._validar_normal,
        }

    def obtener_jugador_actual(self):
        """Retorna el objeto Jugador cuyo turno es actualmente."""
        player_index = self.__turno__ % 2
        return self.__players__[player_index]

    def tirar_dados(self):
        """Tira los dados y establece los valores disponibles para el turno."""
        self.__dados_restantes__ = list(Dice.get_dice())
        return self.__dados_restantes__

    def _get_strategy_key(self, start_point: int, end_point: int) -> str:
        """
        Retorna la clave para el diccionario de estrategias.
        """
        player = self.obtener_jugador_actual()
        is_white = player.is_white()

        is_bearing_off_move = (is_white and end_point == -1) or (
            not is_white and end_point == 25
        )
        if is_bearing_off_move:
            return "bear_off"

        is_bar_move = (is_white and start_point == 24) or (
            not is_white and start_point == -1
        )
        if is_bar_move:
            return "bar"

        return "normal"

    def validar_movimiento(
        self, start_point: int, end_point: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Verifica si un movimiento es legal.
        """
        if start_point < -1 or start_point > 24 or end_point < -1 or end_point > 25:
            return (False, "Puntos fuera del rango del tablero.")

        player = self.obtener_jugador_actual()
        clave_estrategia = self._get_strategy_key(start_point, end_point)

        if clave_estrategia not in self.__estrategias_validacion__:
            return (False, "Estrategia de movimiento desconocida.")

        funcion_validadora = self.__estrategias_validacion__[clave_estrategia]

        mensaje_error = funcion_validadora(start_point, end_point, player)

        if mensaje_error:
            return (False, mensaje_error)

        return (True, None)

    def _validar_bear_off(
        self, start_point: int, _end_point: int, player: Jugador
    ) -> Optional[str]:
        """Valida 'bear off'. Retorna un mensaje de error o None."""
        player_color = player.ficha
        is_white = player.is_white()

        if self.__board__.get_bar_count(player_color) > 0:
            return "Debes sacar tus fichas de la barra primero."
        if not self.__board__.is_home_board_ready(player_color):
            return "No puedes sacar fichas hasta que todas estén en tu home board."

        if is_white:
            required_distance = start_point + 1
        else:
            required_distance = 24 - start_point

        if required_distance in self.__dados_restantes__:
            return None

        available_dice = [
            d for d in self.__dados_restantes__ if d >= required_distance
        ]
        if not available_dice:
            return f"No tienes un dado de {required_distance} o mayor."

        if not self.__board__.is_point_farthest(start_point, player_color):
            return (
                f"No puedes usar un dado mayor ({min(available_dice)}) "
                f"porque la ficha en {start_point} no es la más alejada."
            )

        return None

    def _validar_desde_barra(
        self, _start_point: int, end_point: int, player: Jugador
    ) -> Optional[str]:
        """Valida ÚNICAMENTE un movimiento desde la barra."""       
        player_color = player.ficha
        is_white = player.is_white()

        if self.__board__.get_bar_count(player_color) == 0:
            return "No tienes fichas en la barra."

        if is_white:
            required_distance = 24 - end_point
        else:
            required_distance = end_point + 1

        return self._validar_punto_llegada(end_point, required_distance, player_color)

    def _validar_normal(
        self, start_point: int, end_point: int, player: Jugador
    ) -> Optional[str]:
        """Valida un movimiento normal en el tablero."""
        player_color = player.ficha
        is_white = player.is_white()

        if self.__board__.get_bar_count(player_color) > 0:
            return "Debes sacar tus fichas de la barra primero."

        start_color, start_count = self.__board__.get_point_info(start_point)
        if start_color != player_color or start_count == 0:
            return f"No tienes fichas en el punto de inicio ({start_point})."

        distance = end_point - start_point
        if (is_white and distance >= 0) or (not is_white and distance <= 0):
            return "Movimiento en la dirección incorrecta."

        required_distance = abs(distance)
        return self._validar_punto_llegada(end_point, required_distance, player_color)

    def _validar_punto_llegada(
        self, end_point: int, required_distance: int, player_color: str
    ) -> Optional[str]:
        """Valida el dado y el punto de llegada (común a mov. normal y bar)."""
        if required_distance not in self.__dados_restantes__:
            return f"No tienes un dado de {required_distance}."

        if self.__board__.is_point_blocked(end_point, player_color):
            return f"El punto de destino ({end_point}) está bloqueado por el oponente."

        return None

    def ejecutar_movimiento(self, start_point: int, end_point: int):
        """Aplica el movimiento al tablero y usa el dado utilizado."""
        es_valido, mensaje_error = self.validar_movimiento(start_point, end_point)
        if not es_valido:
            raise ValueError(mensaje_error)

        clave_estrategia = self._get_strategy_key(start_point, end_point)

        self._ejecutar_movimiento_tablero(start_point, end_point, clave_estrategia)

        self.usar_dado_para_movimiento(start_point, end_point, clave_estrategia)

    def _ejecutar_movimiento_tablero(
        self, start_point: int, end_point: int, clave_estrategia: str
    ):
        """Ejecuta el 'hit' (si aplica) y mueve la ficha en el tablero."""
        player_color = self.obtener_jugador_actual().ficha

        if clave_estrategia != "bear_off":
            end_color, _ = self.__board__.get_point_info(end_point)
            if end_color is not None and end_color != player_color:
                self.__board__.hit_opponent(end_point)

        self.__board__.mover_ficha(start_point, end_point)

    def usar_dado_para_movimiento(
        self, start_point: int, end_point: int, clave_estrategia: str
    ):
        """Calcula el dado utilizado y lo elimina de la lista de dados."""
        is_white = self.obtener_jugador_actual().is_white()

        required_distance = 0
        is_bearing_off_move = clave_estrategia == "bear_off"

        if clave_estrategia == "bar":
            required_distance = (24 - end_point) if is_white else (end_point + 1)
        elif is_bearing_off_move:
            required_distance = (start_point + 1) if is_white else (24 - start_point)
        else:
            required_distance = abs(end_point - start_point)

        used_dice = required_distance
        if required_distance not in self.__dados_restantes__:
            if is_bearing_off_move:
                possible_dice = [
                    d for d in self.__dados_restantes__ if d >= required_distance
                ]
                if possible_dice:
                    used_dice = min(possible_dice)
                else:
                    raise ValueError("Lógica de dados inconsistente.")
            else:
                raise ValueError("Dado no encontrado para movimiento normal/bar.")

        try:
            self.__dados_restantes__.remove(used_dice)
        except ValueError:
            pass

    def check_victory(self) -> bool:
        """Verifica si el jugador actual ha ganado."""
        player_color = self.obtener_jugador_actual().ficha
        return self.__board__.get_piece_count(player_color) == 0
