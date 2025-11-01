"""
Pruebas unitarias para el módulo de UI (CLIRenderer y CLIController).
"""

import unittest
from unittest.mock import patch, MagicMock
from src.game.tablero import Tablero
from src.game.jugador import Jugador
from src.game.backgammon import BackgammonGame
from src.game.checker import Checker
from src.ui.cli import CLIRenderer, CLIController


class TestCLIRenderer(unittest.TestCase):
    """Pruebas para la clase CLIRenderer (la 'Vista')."""

    def setUp(self):
        """
        Recibe:
            Nada.
        Hace:
            Se ejecuta antes de cada test. Crea instancias de
            CLIRenderer, Tablero, BackgammonGame y un Jugador 'W'.
        Devuelve:
            Nada.
        """
        self.renderer = CLIRenderer()
        self.tablero = Tablero()
        self.game = BackgammonGame()
        self.jugador_w = Jugador("Jugador 1", "W")

    def test_get_piece_char(self):
        """
        Recibe:
            Nada.
        Hace:
            Prueba el helper `_get_piece_char`.
        Devuelve:
            Verifica que 'white' se convierta en 'W' y 'black' en 'B'.
        """
        self.assertEqual(self.renderer.get_piece_char("white"), "W")
        self.assertEqual(self.renderer.get_piece_char("black"), "B")

    def test_get_owner_and_count(self):
        """
        Recibe:
            Nada.
        Hace:
            Prueba el helper `_get_owner_and_count` consultando el
            tablero inicializado.
        Devuelve:
            Verifica que devuelva la tupla correcta (ej: 'black', 2) para
            puntos ocupados y (None, 0) para puntos vacíos.
        """
        owner, count = self.renderer.get_owner_and_count(self.tablero, 0)
        self.assertEqual(owner, "black")
        self.assertEqual(count, 2)

        owner, count = self.renderer.get_owner_and_count(self.tablero, 23)
        self.assertEqual(owner, "white")
        self.assertEqual(count, 2)

        owner, count = self.renderer.get_owner_and_count(self.tablero, 1)
        self.assertEqual(owner, None)
        self.assertEqual(count, 0)

    def test_get_drawing_grid(self):
        """
        Recibe:
            Nada.
        Hace:
            Llama a `get_drawing_grid` en el tablero inicial.
        Devuelve:
            Verifica que la matriz 10x12 generada contenga los
            caracteres 'W' y 'B' en las posiciones iniciales correctas.
        """
        grid = self.renderer.get_drawing_grid(self.tablero)

        self.assertEqual(grid[0][11], "B")
        self.assertEqual(grid[1][11], "B")
        self.assertEqual(grid[9][11], "W")
        self.assertEqual(grid[8][11], "W")
        self.assertEqual(grid[9][0], "W")
        self.assertEqual(grid[5][0], "W")

    @patch("builtins.print")
    def test_mostrar_tablero(self, mock_print):
        """
        Recibe:
            mock_print (MagicMock): Mock de la función `print`.
        Hace:
            Llama a `mostrar_tablero`.
        Devuelve:
            Verifica que la salida (capturada por `mock_print`) contenga
            las cabeceras (ej: "11 10...") y la línea de la "BAR".
        """
        self.renderer.mostrar_tablero(self.tablero)

        output = "\n".join([call[0][0] for call in mock_print.call_args_list])

        self.assertIn("11  10  09  08  07  06  ||  05  04  03  02  01  00", output)
        self.assertIn("-" * 24 + "BAR " + "-" * 24, output)
        self.assertIn("12  13  14  15  16  17  ||  18  19  20  21  22  23", output)

    @patch("builtins.print")
    def test_mostrar_estado_juego(self, mock_print):
        """
        Recibe:
            mock_print (MagicMock): Mock de la función `print`.
        Hace:
            Configura un estado de juego (dados restantes, fichas en barra)
            y llama a `mostrar_estado_juego`.
        Devuelve:
            Verifica que la salida contenga el nombre del jugador,
            los dados y el conteo de la barra correctos.
        """
        self.game.__dados_restantes__ = [5, 2]
        self.game.__board__.__bar_blancas__.append(Checker("W"))

        self.renderer.mostrar_estado_juego(self.game)

        output = "\n".join([call[0][0] for call in mock_print.call_args_list])

        self.assertIn("Turno de: Jugador 1 (W)", output)
        self.assertIn("Dados restantes: [5, 2]", output)
        self.assertIn("Fichas en Barra: White (W): 1 | Black (B): 0", output)

    @patch("builtins.print")
    def test_mostrar_mensajes(self, mock_print):
        """
        Recibe:
            mock_print (MagicMock): Mock de la función `print`.
        Hace:
            Llama a `mostrar_mensaje` y `mostrar_mensaje_error`.
        Devuelve:
            Verifica que los mensajes se impriman con el formato
            correcto (ej: ">>" para info, "¡ERROR!" para error).
        """
        self.renderer.mostrar_mensaje("Test msg")
        self.assertIn(">> Test msg", mock_print.call_args_list[-1][0][0])

        self.renderer.mostrar_mensaje_error("Error msg")
        self.assertIn("¡ERROR! Error msg", mock_print.call_args_list[-2][0][0])
        self.assertIn(
            "-" * self.renderer.BOARD_WIDTH, mock_print.call_args_list[-1][0][0]
        )

    @patch("builtins.input")
    def test_pausar_para_continuar(self, mock_input):
        """
        Recibe:
            mock_input (MagicMock): Mock de la función `input`.
        Hace:
            Llama a `pausar_para_continuar`.
        Devuelve:
            Verifica que se llame a `input` con el mensaje
            "Presiona Enter para continuar...".
        """
        self.renderer.pausar_para_continuar()
        mock_input.assert_called_once_with("\nPresiona Enter para continuar...")


class TestCLIController(unittest.TestCase):
    """Pruebas para la clase CLIController (el 'Controlador')."""

    def setUp(self):
        """
        Recibe:
            Nada.
        Hace:
            Se ejecuta antes de cada test. Crea una instancia de
            `CLIController` y un `MagicMock` de `Jugador`.
        Devuelve:
            Nada.
        """
        self.controller = CLIController()
        self.mock_jugador = MagicMock(spec=Jugador)
        self.mock_jugador.ficha = "W"  # Corregido de color_fichas
        self.mock_jugador.nombre = "Test Player"

    def test_parsear_input_movimientos_validos(self):
        """
        Recibe:
            Nada.
        Hace:
            Llama a `parsear_input` con varios formatos de
            texto válidos (normal, BAR, OFF, mayús/minús).
        Devuelve:
            Verifica que la tupla (start_point, end_point) devuelta
            sea la correcta numéricamente para cada caso.
        """
        self.assertEqual(self.controller.parsear_input("23 20", "W"), (23, 20))
        self.assertEqual(self.controller.parsear_input("BAR 21", "W"), (24, 21))
        self.assertEqual(self.controller.parsear_input("BAR 3", "B"), (-1, 3))
        self.assertEqual(self.controller.parsear_input("2 OFF", "W"), (2, -1))
        self.assertEqual(self.controller.parsear_input("22 OFF", "B"), (22, 25))
        self.assertEqual(self.controller.parsear_input("bar 5", "B"), (-1, 5))
        self.assertEqual(self.controller.parsear_input("3 off", "W"), (3, -1))

    def test_parsear_input_errores(self):
        """
        Recibe:
            Nada.
        Hace:
            Llama a `parsear_input` con varios formatos inválidos
            (partes incompletas, texto no numérico).
        Devuelve:
            Verifica que se lance `ValueError` con el mensaje de
            error apropiado en cada caso.
        """
        with self.assertRaisesRegex(ValueError, "Input inválido"):
            self.controller.parsear_input("5", "W")
        with self.assertRaisesRegex(ValueError, "Input inválido"):
            self.controller.parsear_input("5 4 3", "W")

        with self.assertRaisesRegex(ValueError, "Punto de inicio 'FOO' no es válido"):
            self.controller.parsear_input("FOO 20", "W")

        with self.assertRaisesRegex(ValueError, "Punto de fin 'BAR' no es válido"):
            self.controller.parsear_input("20 BAR", "W")
        with self.assertRaisesRegex(ValueError, "Punto de fin 'FOO' no es válido"):
            self.controller.parsear_input("20 FOO", "W")

    @patch("time.sleep")
    @patch("builtins.input", side_effect=["bad input", "PASAR"])
    def test_realizar_turno_con_error_de_parseo(self, mock_input, _mock_sleep):
        """
        Recibe:
            mock_input (MagicMock): Mock de `input`.
            _mock_sleep (MagicMock): Mock de `time.sleep`.
        Hace:
            Simula un turno donde el usuario primero ingresa "bad input"
            (que falla `parsear_input`) y luego "PASAR".
        Devuelve:
            Verifica que `input` sea llamado 2 veces, que `__ultimo_error__`
            contenga "Input inválido" y que `ejecutar_movimiento` no se llame.
        """
        self.controller.__renderer__ = MagicMock(spec=CLIRenderer)
        mock_game = self.controller.__game__
        mock_game.tirar_dados = MagicMock(return_value=[3, 5])
        mock_game.ejecutar_movimiento = MagicMock()
        mock_game.__dados_restantes__ = [3, 5]

        self.controller.realizar_turno(self.mock_jugador)

        self.assertEqual(mock_input.call_count, 2)
        self.assertIn("Input inválido", self.controller.__ultimo_error__)
        mock_game.ejecutar_movimiento.assert_not_called()

    @patch("time.sleep")
    @patch("builtins.input", side_effect=["23 21", "PASAR"])
    def test_realizar_turno_con_error_de_validacion(self, mock_input, _mock_sleep):
        """
        Recibe:
            mock_input (MagicMock): Mock de `input`.
            _mock_sleep (MagicMock): Mock de `time.sleep`.
        Hace:
            Simula un turno donde `validar_movimiento` (mockeado)
            devuelve (False, "No tienes un dado de 2.").
        Devuelve:
            Verifica que `__ultimo_error__` contenga el mensaje del modelo
            y que `ejecutar_movimiento` no se llame.
        """
        self.controller.__renderer__ = MagicMock(spec=CLIRenderer)
        mock_game = self.controller.__game__
        mock_game.tirar_dados = MagicMock(return_value=[3, 5])
        mock_game.validar_movimiento = MagicMock(
            return_value=(False, "No tienes un dado de 2.")
        )
        mock_game.ejecutar_movimiento = MagicMock()
        mock_game.__dados_restantes__ = [3, 5]

        self.controller.realizar_turno(self.mock_jugador)

        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(self.controller.__ultimo_error__, "No tienes un dado de 2.")
        mock_game.ejecutar_movimiento.assert_not_called()

    @patch("time.sleep")
    @patch("builtins.input", side_effect=["23 20", "PASAR"])
    def test_realizar_turno_con_error_de_ejecucion(self, _mock_input, _mock_sleep):
        """
        Recibe:
            _mock_input (MagicMock): Mock de `input`.
            _mock_sleep (MagicMock): Mock de `time.sleep`.
        Hace:
            Simula un turno donde `validar_movimiento` pasa, pero
            `ejecutar_movimiento` (mockeado) lanza un ValueError.
        Devuelve:
            Verifica que el `ValueError` sea capturado, almacenado en
            `__ultimo_error__`, y que `ejecutar_movimiento` haya sido llamado.
        """
        self.controller.__renderer__ = MagicMock(spec=CLIRenderer)
        mock_game = self.controller.__game__
        mock_game.tirar_dados = MagicMock(return_value=[3, 5])
        mock_game.validar_movimiento = MagicMock(return_value=(True, None))
        mock_game.ejecutar_movimiento = MagicMock(
            side_effect=ValueError("Error de Lógica")
        )
        mock_game.__dados_restantes__ = [3, 5]

        self.controller.realizar_turno(self.mock_jugador)

        self.assertEqual(self.controller.__ultimo_error__, "Error de Lógica")
        mock_game.ejecutar_movimiento.assert_called_once()

    @patch("src.ui.cli.CLIController.realizar_turno")
    def test_iniciar_juego_termina_con_victoria(self, mock_realizar_turno):
        """
        Recibe:
            mock_realizar_turno (MagicMock): Mock del método `realizar_turno`.
        Hace:
            Simula el bucle `iniciar_juego` donde `check_victory`
            devuelve False la primera vez y True la segunda.
        Devuelve:
            Verifica que `realizar_turno` se llame solo 1 vez y
            que `mostrar_ganador` sea llamado al salir del bucle.
        """

        mock_renderer_instance = MagicMock(spec=CLIRenderer)
        self.controller.__renderer__ = mock_renderer_instance

        mock_game = self.controller.__game__
        mock_game.check_victory = MagicMock(side_effect=[False, True])

        self.controller.iniciar_juego()

        self.assertEqual(mock_realizar_turno.call_count, 1)

        mock_renderer_instance.mostrar_ganador.assert_called_once()


if __name__ == "__main__":
    unittest.main()
