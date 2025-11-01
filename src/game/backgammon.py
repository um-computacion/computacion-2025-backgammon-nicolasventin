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
        """
        Recibe:
            name_p1 (str): Nombre del Jugador 1 (Fichas 'W').
            name_p2 (str): Nombre del Jugador 2 (Fichas 'B').
        Hace:
            Inicializa las dependencias: Tablero, Dado, y los dos Jugadores.
            Configura el turno inicial y la lista de dados restantes.
            Registra las estrategias de validación (Patrón Strategy).
        Devuelve:
            Nada.
        """
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
        """
        Recibe:
            Nada.
        Hace:
            Calcula el índice del jugador actual basado en `__turno__`.
        Devuelve:
            (Jugador): La instancia del objeto Jugador que tiene el turno.
        """
        player_index = self.__turno__ % 2
        return self.__players__[player_index]

    def tirar_dados(self):
        """
        Recibe:
            Nada.
        Hace:
            Llama a `Dice.get_dice()` y almacena el resultado (como lista)
            en `__dados_restantes__`.
        Devuelve:
            (list): Una lista de 2 o 4 enteros con los dados del turno.
        """
        self.__dados_restantes__ = list(Dice.get_dice())
        return self.__dados_restantes__

    def _get_strategy_key(self, start_point: int, end_point: int) -> str:
        """
        Recibe:
            start_point (int): El punto de origen del movimiento.
            end_point (int): El punto de destino del movimiento.
        Hace:
            Determina qué tipo de movimiento se está intentando (normal,
            desde la barra, o bear off) basado en los puntos de
            origen/destino y el jugador actual.
        Devuelve:
            (str): La clave ("normal", "bar", "bear_off") para el
                   diccionario `__estrategias_validacion__`.
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
        Recibe:
            start_point (int): El punto de origen del movimiento.
            end_point (int): El punto de destino del movimiento.
        Hace:
            Actúa como un despachador (Dispatcher).
            1. Valida los rangos básicos de los puntos.
            2. Usa `_get_strategy_key` para determinar el tipo de movimiento.
            3. Llama a la función de validación específica (ej: `_validar_normal`).
        Devuelve:
            (Tuple[bool, Optional[str]]):
                - (True, None) si el movimiento es válido.
                - (False, "Mensaje de error") si el movimiento es inválido.
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
        """
        Recibe:
            start_point (int): El punto de origen (0-5 para W, 18-23 para B).
            _end_point (int): -1 (W) o 25 (B). No se usa aquí.
            player (Jugador): El jugador actual.
        Hace:
            Valida un movimiento de "bear off" (sacar ficha).
            1. Verifica que no haya fichas en la barra.
            2. Verifica que `is_home_board_ready` sea True.
            3. Verifica si existe un dado exacto (`required_distance`).
            4. Si no, verifica si hay un dado mayor Y `is_point_farthest` es True.
        Devuelve:
            (Optional[str]): None si es válido, o un mensaje de error si falla.
        """
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
        """
        Recibe:
            _start_point (int): 24 (W) o -1 (B). No se usa aquí.
            end_point (int): El punto de destino (0-5 para B, 18-23 para W).
            player (Jugador): El jugador actual.
        Hace:
            Valida un movimiento para sacar una ficha de la barra.
            1. Verifica que haya fichas en la barra.
            2. Calcula la distancia requerida para entrar.
            3. Llama a `_validar_punto_llegada` para verificar el dado y bloqueo.
        Devuelve:
            (Optional[str]): None si es válido, o un mensaje de error si falla.
        """
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
        """
        Recibe:
            start_point (int): El punto de origen (0-23).
            end_point (int): El punto de destino (0-23).
            player (Jugador): El jugador actual.
        Hace:
            Valida un movimiento normal en el tablero.
            1. Verifica que no haya fichas en la barra.
            2. Verifica que el jugador posea fichas en `start_point`.
            3. Verifica que el movimiento sea en la dirección correcta.
            4. Llama a `_validar_punto_llegada` para verificar el dado y bloqueo.
        Devuelve:
            (Optional[str]): None si es válido, o un mensaje de error si falla.
        """
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
        """
        Recibe:
            end_point (int): El punto de destino.
            required_distance (int): El valor del dado necesario.
            player_color (str): El color del jugador actual.
        Hace:
            Valida los dos factores comunes de un movimiento:
            1. Verifica que `required_distance` esté en `__dados_restantes__`.
            2. Verifica que `end_point` no esté bloqueado (`is_point_blocked`).
        Devuelve:
            (Optional[str]): None si es válido, o un mensaje de error si falla.
        """
        if required_distance not in self.__dados_restantes__:
            return f"No tienes un dado de {required_distance}."

        if self.__board__.is_point_blocked(end_point, player_color):
            return f"El punto de destino ({end_point}) está bloqueado por el oponente."

        return None

    def ejecutar_movimiento(self, start_point: int, end_point: int):
        """
        Recibe:
            start_point (int): El punto de origen validado.
            end_point (int): El punto de destino validado.
        Hace:
            Actúa como despachador (Dispatcher) para ejecutar un movimiento.
            1. Llama a `validar_movimiento` (control de seguridad).
            2. Llama a `_ejecutar_movimiento_tablero` para hacer el 'hit' y mover.
            3. Llama a `usar_dado_para_movimiento` para consumir el dado.
        Devuelve:
            Nada.
        """
        es_valido, mensaje_error = self.validar_movimiento(start_point, end_point)
        if not es_valido:
            raise ValueError(mensaje_error)

        clave_estrategia = self._get_strategy_key(start_point, end_point)

        self._ejecutar_movimiento_tablero(start_point, end_point, clave_estrategia)

        self.usar_dado_para_movimiento(start_point, end_point, clave_estrategia)

    def _ejecutar_movimiento_tablero(
        self, start_point: int, end_point: int, clave_estrategia: str
    ):
        """
        Recibe:
            start_point (int): El punto de origen.
            end_point (int): El punto de destino.
            clave_estrategia (str): El tipo de movimiento ("normal", "bar", "bear_off").
        Hace:
            Interactúa con el tablero.
            1. Si el movimiento no es "bear_off", verifica si debe hacer 'hit'.
            2. Llama a `self.__board__.mover_ficha()` para mover la ficha.
        Devuelve:
            Nada.
        """
        player_color = self.obtener_jugador_actual().ficha

        if clave_estrategia != "bear_off":
            end_color, _ = self.__board__.get_point_info(end_point)
            if end_color is not None and end_color != player_color:
                self.__board__.hit_opponent(end_point)

        self.__board__.mover_ficha(start_point, end_point)

    def usar_dado_para_movimiento(
        self, start_point: int, end_point: int, clave_estrategia: str
    ):
        """
        Recibe:
            start_point (int): El punto de origen.
            end_point (int): El punto de destino.
            clave_estrategia (str): El tipo de movimiento.
        Hace:
            Calcula qué dado se utilizó para el movimiento (incluyendo
            la lógica de 'bear off' con dado mayor) y lo elimina de
            la lista `__dados_restantes__`.
        Devuelve:
            Nada.
        """
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
        """
        Recibe:
            Nada.
        Hace:
            Verifica si el jugador actual ha ganado llamando a
            `get_piece_count` en el tablero.
        Devuelve:
            (bool): True si el jugador actual tiene 0 fichas en juego,
                    False en caso contrario.
        """
        player_color = self.obtener_jugador_actual().ficha
        return self.__board__.get_piece_count(player_color) == 0

