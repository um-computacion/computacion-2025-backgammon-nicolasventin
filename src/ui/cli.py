"""
Módulo de la Interfaz de Línea de Comandos (CLI) para Backgammon.
Contiene la Vista (CLIRenderer) y el Controlador (CLIController).
"""

import os
import time
from typing import Optional
from src.game.backgammon import BackgammonGame
from src.game.tablero import Tablero
from src.game.jugador import Jugador

class CLIRenderer:
    """
    Maneja toda la salida visual (la 'Vista') para la consola.
    """
    BOARD_WIDTH = 52

    def clear_screen(self):
        """
        Recibe:
            Nada.
        Hace:
            Limpia la pantalla de la terminal usando 'cls' (Windows)
            o 'clear' (Linux/macOS).
        Devuelve:
            Nada.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_drawing_grid(self, tablero: Tablero) -> list[list[str]]:
        """
        Recibe:
            tablero (Tablero): La instancia del tablero de juego.
        Hace:
            Crea la matriz de datos 10x12 para dibujar el tablero.
            Consulta al tablero usando `get_point_info` (DIP) y
            coloca los caracteres 'W' y 'B' en la grilla.
        Devuelve:
            (list[list[str]]): La matriz 10x12 representando el tablero.
        """
        height, width = 10, 12
        grid = [[" " for _ in range(width)] for _ in range(height)]

        for c in range(12):
            point = 11 - c
            owner, n = self.get_owner_and_count(tablero, point)
            if not owner or n == 0:
                continue
            piece = self.get_piece_char(owner)
            if n <= 5:
                for r in range(n):
                    grid[r][c] = piece
            else:
                for r in range(4):
                    grid[r][c] = piece
                grid[4][c] = str(n - 4)

        for c in range(12):
            point = 12 + c
            owner, n = self.get_owner_and_count(tablero, point)
            if not owner or n == 0:
                continue
            piece = self.get_piece_char(owner)
            if n <= 5:
                for k in range(n):
                    grid[9 - k][c] = piece
            else:
                for k in range(4):
                    grid[9 - k][c] = piece
                grid[5][c] = str(n - 4)
        return grid

    def get_owner_and_count(self, tablero: Tablero, idx: int) -> tuple[str | None, int]:
        """
        Recibe:
            tablero (Tablero): La instancia del tablero.
            idx (int): El índice del punto (0-23).
        Hace:
            Es un helper INTERNO para `get_drawing_grid`. Consulta
            `tablero.get_point_info` y traduce el color ('W'/'B')
            a un string ('white'/'black').
        Devuelve:
            (tuple): ('white'/'black' o None, count).
        """
        color, count = tablero.get_point_info(idx)
        if color is None:
            return (None, 0)
        owner_str = "white" if color == "W" else "black"
        return (owner_str, count)

    def get_piece_char(self, owner: str) -> str:
        """
        Recibe:
            owner (str): 'white' o 'black'.
        Hace:
            Traduce el string 'white'/'black' al caracter 'W'/'B'.
        Devuelve:
            (str): 'W' o 'B'.
        """
        return "W" if owner == "white" else "B"

    def mostrar_tablero(self, tablero: Tablero):
        """
        Recibe:
            tablero (Tablero): La instancia del tablero.
        Hace:
            1. Llama a `get_drawing_grid` para obtener la matriz.
            2. Imprime por consola la representación gráfica completa
               del tablero, incluyendo cabeceras y la barra.
        Devuelve:
            Nada.
        """
        grid = self.get_drawing_grid(tablero)

        print(" 11  10  09  08  07  06  ||  05  04  03  02  01  00")
        print("=" * self.BOARD_WIDTH)

        for i, row in enumerate(grid):
            row_str = ""
            for c in range(6):
                row_str += f" {row[c]:<2} "
            row_str += " || "
            for c in range(6, 12):
                row_str += f" {row[c]:<2} "
            print(row_str)

            if i == 4:
                print("-" * 24 + "BAR " + "-" * 24)

        print("=" * self.BOARD_WIDTH)
        print(" 12  13  14  15  16  17  ||  18  19  20  21  22  23")

    def mostrar_estado_juego(self, game: BackgammonGame):
        """
        Recibe:
            game (BackgammonGame): La instancia del juego.
        Hace:
            Consulta el estado actual del juego (jugador actual, dados,
            conteo en barra) y lo imprime en la consola.
        Devuelve:
            Nada.
        """
        jugador = game.obtener_jugador_actual()
        fichas_bar_blancas = game.__board__.get_bar_count("W")
        fichas_bar_negras = game.__board__.get_bar_count("B")

        print("=" * self.BOARD_WIDTH)
        print(f"Turno de: {jugador.obtener_info()}")
        print(f"Dados restantes: {game.__dados_restantes__}")
        print(f"Fichas en Barra: White (W): {fichas_bar_blancas} | Black (B): {fichas_bar_negras}")
        print("=" * self.BOARD_WIDTH + "\n")

    def mostrar_mensaje(self, mensaje: str):
        """
        Recibe:
            mensaje (str): Un mensaje de información.
        Hace:
            Imprime el mensaje con formato de información (>>).
        Devuelve:
            Nada.
        """
        print(f"\n>> {mensaje}\n")

    def mostrar_mensaje_error(self, mensaje: str):
        """
        Recibe:
            mensaje (str): Un mensaje de error.
        Hace:
            Imprime el mensaje con formato de error (¡ERROR!).
        Devuelve:
            Nada.
        """
        print(f"\n¡ERROR! {mensaje}")
        print("-" * self.BOARD_WIDTH)

    def mostrar_ganador(self, jugador: Jugador):
        """
        Recibe:
            jugador (Jugador): El jugador que ha ganado la partida.
        Hace:
            Imprime un mensaje de victoria felicitando al jugador.
        Devuelve:
            Nada.
        """
        print("*" * self.BOARD_WIDTH)
        print(f"\n¡¡¡ FELICITACIONES, {jugador.obtener_info()} !!!")
        print("¡HAS GANADO LA PARTIDA!")
        print("*" * self.BOARD_WIDTH)

    def pausar_para_continuar(self):
        """
        Recibe:
            Nada.
        Hace:
            Pausa la ejecución y espera que el usuario presione Enter.
        Devuelve:
            Nada.
        """
        input("\nPresiona Enter para continuar...")


class CLIController:
    """Maneja el flujo del juego (el 'Controlador')."""

    def __init__(self):
        """
        Recibe:
            Nada.
        Hace:
            Inicializa las instancias del Modelo (`BackgammonGame`)
            y de la Vista (`CLIRenderer`).
        Devuelve:
            Nada.
        """
        self.__game__ = BackgammonGame("Jugador 1", "Jugador 2")
        self.__renderer__ = CLIRenderer()
        self.__ultimo_error__: Optional[str] = None

    def parsear_input(self, input_str: str, color_jugador: str) -> tuple[int, int]:
        """
        Recibe:
            input_str (str): El texto ingresado por el usuario (ej: "23 18").
            color_jugador (str): 'W' o 'B', para mapear "BAR" y "OFF".
        Hace:
            Convierte el string de entrada en los índices numéricos
            que entiende el `BackgammonGame`. Mapea "BAR" a 24 (W) o -1 (B)
            y "OFF" a -1 (W) o 25 (B).
        Devuelve:
            (tuple[int, int]): (start_point, end_point).
        """
        partes = input_str.strip().upper().split()
        if len(partes) != 2:
            raise ValueError("Input inválido. Se esperan 2 partes (ej: '5 2' o 'BAR 3').")
        start_str, end_str = partes
        start_point = 0
        end_point = 0

        if start_str == "BAR":
            start_point = 24 if color_jugador == 'W' else -1
        else:
            try:
                start_point = int(start_str)
            except ValueError as exc:
                raise ValueError(f"Punto de inicio '{start_str}' no es válido.") from exc

        if end_str == "OFF":
            end_point = -1 if color_jugador == 'W' else 25
        else:
            try:
                end_point = int(end_str)
            except ValueError as exc:
                raise ValueError(f"Punto de fin '{end_str}' no es válido.") from exc
        return (start_point, end_point)

    def realizar_turno(self, jugador: Jugador):
        """
        Recibe:
            jugador (Jugador): El jugador que tiene el turno.
        Hace:
            Maneja el bucle completo de un turno:
            1. Tira los dados.
            2. Mientras queden dados:
               a. Renderiza el tablero y estado.
               b. Pide un input al usuario.
               c. Parsea el input.
               d. Valida el movimiento con `game.validar_movimiento`.
               e. Ejecuta el movimiento con `game.ejecutar_movimiento`.
               f. Maneja errores de parseo, validación o ejecución.
        Devuelve:
            Nada.
        """

        dados = self.__game__.tirar_dados()
        self.__renderer__.mostrar_mensaje(f"{jugador.obtener_info()} ha sacado: {dados}")

        while self.__game__.__dados_restantes__:
            self.__renderer__.clear_screen()
            self.__renderer__.mostrar_tablero(self.__game__.__board__)
            self.__renderer__.mostrar_estado_juego(self.__game__)

            if self.__ultimo_error__:
                self.__renderer__.mostrar_mensaje_error(self.__ultimo_error__)

            try:
                input_str = input(
                    f"Ingrese movimiento para {jugador.ficha} (ej: 23 18, BAR 20, 3 OFF): "
                )

                if input_str.strip().upper() == "PASAR":
                    self.__renderer__.mostrar_mensaje("Turno cedido.")
                    self.__game__.__dados_restantes__ = []
                    continue

                start, end = self.parsear_input(input_str, jugador.ficha)

            except ValueError as e:
                self.__ultimo_error__ = f"Input inválido: {e}"
                continue

            es_valido, mensaje_error = self.__game__.validar_movimiento(start, end)

            if not es_valido:
                self.__ultimo_error__ = mensaje_error
                continue

            try:
                self.__game__.ejecutar_movimiento(start, end)
                self.__ultimo_error__ = None
            except ValueError as e:
                self.__ultimo_error__ = str(e)
                continue

        self.__renderer__.clear_screen()
        self.__renderer__.mostrar_tablero(self.__game__.__board__)
        self.__renderer__.mostrar_mensaje(f"Fin del turno de {jugador.obtener_info()}.")
        time.sleep(1.5)

    def iniciar_juego(self):
        """
        Recibe:
            Nada.
        Hace:
            Inicia el bucle principal del juego. Alterna los turnos
            infinitamente hasta que `game.check_victory()` sea True.
            Al finalizar, muestra al ganador.
        Devuelve:
            Nada.
        """
        jugador_ganador = None

        while True:
            self.__renderer__.clear_screen()
            self.__renderer__.mostrar_tablero(self.__game__.__board__)

            jugador_actual = self.__game__.obtener_jugador_actual()

            if self.__game__.check_victory():
                indice_ganador = (self.__game__.__turno__ - 1) % 2
                jugador_ganador = self.__game__.__players__[indice_ganador]
                break

            self.realizar_turno(jugador_actual)
            self.__game__.__turno__ += 1

        if jugador_ganador:
            self.__renderer__.clear_screen()
            self.__renderer__.mostrar_tablero(self.__game__.__board__)
            self.__renderer__.mostrar_ganador(jugador_ganador)

if __name__ == "__main__":
    try:
        controlador = CLIController()
        controlador.iniciar_juego()
    except KeyboardInterrupt:
        print("\n¡Juego interrumpido! Adiós.")
