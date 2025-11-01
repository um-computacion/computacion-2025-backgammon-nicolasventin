"""
Pruebas unitarias para la clase BackgammonGame.
"""
import unittest
from unittest.mock import patch
from src.game.backgammon import BackgammonGame
from src.game.checker import Checker


class TestBackgammonGame(unittest.TestCase):
    """Conjunto de pruebas para la clase BackgammonGame."""

    def setUp(self):
        """
        Recibe:
            Nada.
        Hace:
            Se ejecuta antes de cada test. Crea una nueva
            instancia de `BackgammonGame` (self.game).
        Devuelve:
            Nada.
        """
        self.game = BackgammonGame()
        # Los dados se definen en cada test para mayor aislamiento

    def _setup_checkers(self, point, color, count):
        """
        Recibe:
            point (int): El índice del punto a modificar.
            color (str): 'W' o 'B'.
            count (int): Número de fichas a colocar.
        Hace:
            Helper interno para configurar escenarios de prueba. Sobrescribe
            un punto del tablero del juego (`self.game.__board__`).
        Devuelve:
            Nada.
        """
        self.game.__board__.__puntos__[point] = [Checker(color) for _ in range(count)]

    def test_turno_inicial(self):
        """
        Recibe:
            Nada.
        Hace:
            Comprueba el valor inicial de `__turno__`.
        Devuelve:
            Verifica que `self.game.__turno__` sea 0.
        """
        self.assertEqual(self.game.__turno__, 0)

    def test_jugadores_iniciales(self):
        """
        Recibe:
            Nada.
        Hace:
            Comprueba la inicialización de `__players__`.
        Devuelve:
            Verifica que haya 2 jugadores y que sus fichas
            sean 'W' (Jugador 0) y 'B' (Jugador 1).
        """
        jugadores = self.game.__players__
        self.assertEqual(len(jugadores), 2)
        self.assertEqual(jugadores[0].ficha, "W")
        self.assertEqual(jugadores[1].ficha, "B")

    @patch('src.game.dado.Dice.get_dice', return_value=(1, 2))
    def test_tirar_dados__actualiza_dados_restantes_con_lista(self, mock_dice):
        """
        Recibe:
            mock_dice (MagicMock): Mock de `Dice.get_dice`.
        Hace:
            Llama a `tirar_dados()` forzando una tirada (1, 2).
        Devuelve:
            Verifica que `__dados_restantes__` sea una lista `[1, 2]`.
        """
        dados = self.game.tirar_dados()
        self.assertIsInstance(self.game.__dados_restantes__, list)
        self.assertEqual(dados, self.game.__dados_restantes__)
        self.assertEqual(dados, [1, 2])
        mock_dice.assert_called_once()

    @patch('src.game.dado.Dice.get_dice', return_value=(6, 6, 6, 6))
    def test_tirar_dados__con_patch_para_dobles(self, mock_get_dice):
        """
        Recibe:
            mock_get_dice (MagicMock): Mock de `Dice.get_dice`.
        Hace:
            Llama a `tirar_dados()` forzando una tirada doble (6, 6, 6, 6).
        Devuelve:
            Verifica que `__dados_restantes__` sea `[6, 6, 6, 6]`.
        """
        dados = self.game.tirar_dados()
        mock_get_dice.assert_called_once()
        self.assertEqual(dados, [6, 6, 6, 6])
        self.assertEqual(self.game.__dados_restantes__, [6, 6, 6, 6])

    def test_validar_movimiento_desde_barra__es_correcto_para_ambos_colores(self):
        """
        Recibe:
            Nada.
        Hace:
            Prueba la validación de movimientos desde la barra:
            1. 'W' (jugador 0) con dado 3 a punto 21 (válido) y 20 (inválido).
            2. 'B' (jugador 1) con dado 4 a punto 3 (válido) y 5 (inválido).
        Devuelve:
            Verifica que `validar_movimiento` devuelva (True, None) para
            los válidos y (False, ...) para los inválidos.
        """
        self.game.__board__.__bar_blancas__.append(Checker("W"))
        self.game.__dados_restantes__ = [3]
        self.assertTrue(self.game.validar_movimiento(24, 21)[0])
        self.assertFalse(self.game.validar_movimiento(24, 20)[0])
        self.game.__board__.__bar_blancas__ = []
        self.assertFalse(self.game.validar_movimiento(24, 21)[0])

        self.game.__turno__ = 1
        self.game.__board__.__bar_negras__.append(Checker("B"))
        self.game.__dados_restantes__ = [4]
        self.assertTrue(self.game.validar_movimiento(-1, 3)[0])
        self.assertFalse(self.game.validar_movimiento(-1, 5)[0])

    def test_validar_movimiento_bloqueado(self):
        """
        Recibe:
            Nada.
        Hace:
            Configura un punto de destino bloqueado (>=2 fichas oponentes).
            1. 'W' (jugador 0) intentando mover a un punto con 2 'B'.
            2. 'B' (jugador 1) intentando mover a un punto con 3 'W'.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...) en ambos casos.
        """
        self._setup_checkers(18, "B", 2)
        self._setup_checkers(21, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(21, 18)[0])

        self.game.__turno__ = 1
        self._setup_checkers(6, "W", 3)
        self._setup_checkers(3, "B", 1)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(3, 6)[0])

    def test_validar_movimiento_hit_valido(self):
        """
        Recibe:
            Nada.
        Hace:
            Configura un punto de destino con un 'blot' (1 ficha oponente).
            1. 'W' (jugador 0) moviendo a un punto con 1 'B'.
            2. 'B' (jugador 1) moviendo a un punto con 1 'W'.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (True, None) en ambos casos.
        """
        self._setup_checkers(15, "B", 1)
        self._setup_checkers(18, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertTrue(self.game.validar_movimiento(18, 15)[0])

        self.game.__turno__ = 1
        self._setup_checkers(9, "W", 1)
        self._setup_checkers(6, "B", 1)
        self.game.__dados_restantes__ = [3]
        self.assertTrue(self.game.validar_movimiento(6, 9)[0])

    def test_validar_movimiento_basico_fallos(self):
        """
        Recibe:
            Nada.
        Hace:
            Prueba fallos de validación comunes:
            1. Mover desde un punto vacío.
            2. Mover en la dirección incorrecta (hacia atrás).
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...) en ambos casos.
        """
        self.game.__dados_restantes__ = [5]

        self.game.__board__.__puntos__[1] = []
        self.assertFalse(self.game.validar_movimiento(1, 6)[0])

        self._setup_checkers(5, "W", 1)
        self.assertFalse(self.game.validar_movimiento(5, 1)[0])

    def test_validar_movimiento__falla_si_puntos_estan_fuera_del_tablero(self):
        """
        Recibe:
            Nada.
        Hace:
            Llama a `validar_movimiento` con puntos fuera del rango (-1 a 25).
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...).
        """
        self.assertFalse(self.game.validar_movimiento(20, 26)[0])
        self.assertFalse(self.game.validar_movimiento(-2, 5)[0])

    def test_validar_movimiento_bear_off_exacto(self):
        """
        Recibe:
            Nada.
        Hace:
            Simula un escenario de 'bear off' (todas las fichas en casa)
            y prueba un movimiento con dado exacto.
        Devuelve:
            Verifica que `validar_movimiento` (a -1 o 25) devuelva (True, None).
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertTrue(self.game.validar_movimiento(2, -1)[0])

        self.game.__turno__ = 1
        for i in range(0, 18):
            self.game.__board__.__puntos__[i] = []
        self._setup_checkers(21, "B", 1)
        self.game.__dados_restantes__ = [3]
        self.assertTrue(self.game.validar_movimiento(21, 25)[0])

    def test_validar_movimiento_bear_off_dado_mayor_lejana(self):
        """
        Recibe:
            Nada.
        Hace:
            Simula escenario de 'bear off' y prueba mover con un dado
            mayor al necesario, siendo la ficha la MÁS ALEJADA.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (True, None).
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [5]
        self.assertTrue(self.game.validar_movimiento(2, -1)[0])

        self.game.__turno__ = 1
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(21, "B", 1)
        self.game.__dados_restantes__ = [5]
        self.assertTrue(self.game.validar_movimiento(21, 25)[0])

    def test_validar_movimiento_bear_off_dado_mayor_no_lejana(self):
        """
        Recibe:
            Nada.
        Hace:
            Simula 'bear off' y prueba mover con dado mayor, pero
            NO siendo la ficha la más alejada.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...).
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self._setup_checkers(4, "W", 1)
        self.game.__dados_restantes__ = [5]
        self.assertFalse(self.game.validar_movimiento(2, -1)[0])

    def test_validar_movimiento_bear_off_falla_si_no_home_board(self):
        """
        Recibe:
            Nada.
        Hace:
            Intenta un 'bear off' cuando NO todas las fichas están
            en el home board.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...).
        """
        self._setup_checkers(6, "W", 1)
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(2, -1)[0])

    def test_validar_movimiento__falla_si_hay_fichas_en_barra_y_no_es_mov_barra(self):
        """
        Recibe:
            Nada.
        Hace:
            Intenta un movimiento normal O un 'bear off' mientras
            el jugador tiene fichas en la barra.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...).
        """
        self.game.__board__.__bar_blancas__.append(Checker("W"))
        self._setup_checkers(10, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(10, 7)[0])

        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 2)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(2, -1)[0])

    def test_ejecutar_movimiento__saca_fichas_de_la_barra_correctamente(self):
        """
        Recibe:
            Nada.
        Hace:
            Ejecuta un movimiento válido desde la barra (24 a 21).
        Devuelve:
            Verifica que la barra quede vacía, el punto 21 tenga
            1 ficha y el dado [3] se consuma.
        """
        self.game.__board__.__bar_blancas__.append(Checker("W"))
        self.game.__dados_restantes__ = [3, 5]

        self.game.ejecutar_movimiento(24, 21)

        self.assertEqual(len(self.game.__board__.__bar_blancas__), 0)
        self.assertEqual(self.game.__board__.get_point_info(21)[1], 1)
        self.assertEqual(self.game.__dados_restantes__, [5])

    def test_ejecutar_movimiento__lanza_error_si_movimiento_no_es_valido(self):
        """
        Recibe:
            Nada.
        Hace:
            Llama a `ejecutar_movimiento` con un movimiento que
            falla la validación (sin dado 3).
        Devuelve:
            Verifica que se lance un `ValueError` con el mensaje de error
            de la validación.
        """
        self._setup_checkers(20, "W", 1)
        self.game.__dados_restantes__ = [1]
        with self.assertRaisesRegex(ValueError, "No tienes un dado de 3."):
            self.game.ejecutar_movimiento(20, 17)

    def test_ejecutar_movimiento_bear_off(self):
        """
        Recibe:
            Nada.
        Hace:
            Ejecuta un 'bear off' válido con dado exacto (2 a -1).
        Devuelve:
            Verifica que la ficha se elimine del punto 2 y
            el dado [3] se consuma.
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.game.ejecutar_movimiento(2, -1)

        self.assertEqual(self.game.__board__.get_point_info(2)[1], 0)
        self.assertEqual(self.game.__dados_restantes__, [])

    @patch('src.game.backgammon.BackgammonGame.validar_movimiento', return_value=(True, None))
    def test_ejecutar_movimiento__lanza_valueerror_si_logica_bear_off_falla(self, _mock_validar):
        """
        Recibe:
            _mock_validar (MagicMock): Mock para saltar la validación.
        Hace:
            Llama a `ejecutar_movimiento` (bear off) en un estado donde
            la validación pasa (mockeada) pero la ejecución falla
            (no hay dado 3 o mayor, solo dado 1).
        Devuelve:
            Verifica que se lance `ValueError` por "Lógica de dados inconsistente".
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [1]
        with self.assertRaisesRegex(ValueError, "Lógica de dados inconsistente"):
            self.game.ejecutar_movimiento(2, -1)

    def test_ejecutar_movimiento__bear_off_usa_dado_mayor_si_es_ficha_lejana(self):
        """
        Recibe:
            Nada.
        Hace:
            Ejecuta un 'bear off' válido usando un dado mayor (5)
            en la ficha más lejana (punto 2, requiere dado 3).
        Devuelve:
            Verifica que la ficha se elimina y el dado [5] se consume.
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [5]
        self.assertTrue(self.game.validar_movimiento(2, -1)[0])
        self.game.ejecutar_movimiento(2, -1)
        self.assertEqual(self.game.__board__.get_point_info(2)[1], 0)
        self.assertEqual(self.game.__dados_restantes__, [])

    def test_check_victory(self):
        """
        Recibe:
            Nada.
        Hace:
            Prueba `check_victory`:
            1. 'W' (jugador 0) no tiene fichas.
            2. 'B' (jugador 1) todavía tiene fichas.
        Devuelve:
            Verifica que `check_victory` sea True en el turno 0 y
            False en el turno 1.
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self.game.__board__.__bar_blancas__ = []
        self._setup_checkers(20, "B", 1)

        self.assertTrue(self.game.check_victory())

        self.game.__turno__ = 1
        self.assertFalse(self.game.check_victory())

    @patch('src.game.backgammon.BackgammonGame._get_strategy_key', return_value="desconocida")
    def test_validar_movimiento__falla_si_clave_estrategia_no_existe(self, _mock_get_key):
        """
        Recibe:
            _mock_get_key (MagicMock): Mock de `_get_strategy_key`.
        Hace:
            Fuerza a `_get_strategy_key` a devolver una clave inválida.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...).
        """
        self.assertFalse(self.game.validar_movimiento(23, 20)[0])

    def test_validar_bear_off__falla_si_no_hay_dados_disponibles(self):
        """
        Recibe:
            Nada.
        Hace:
            Intenta un 'bear off' desde el punto 4 (requiere 5) pero
            solo tiene un dado 3.
        Devuelve:
            Verifica que `validar_movimiento` devuelva (False, ...).
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(4, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(4, -1)[0])

    def test_ejecutar_movimiento_normal_con_hit(self):
        """
        Recibe:
            Nada.
        Hace:
            Ejecuta un movimiento válido que aterriza en un 'blot' oponente.
        Devuelve:
            Verifica que la ficha oponente ('B') sea movida a la barra y
            la ficha 'W' ocupe el punto.
        """
        self._setup_checkers(18, "W", 1)
        self._setup_checkers(15, "B", 1)
        self.game.__dados_restantes__ = [3]

        self.game.ejecutar_movimiento(18, 15)

        self.assertEqual(self.game.__board__.get_bar_count("B"), 1)
        self.assertEqual(self.game.__board__.get_point_info(15)[0], "W")
        self.assertEqual(self.game.__dados_restantes__, [])

    @patch('src.game.backgammon.BackgammonGame.validar_movimiento', return_value=(True, None))
    def test_ejecutar_movimiento__lanza_valueerror_dado_no_encontrado_normal(self, _mock_validar):
        """
        Recibe:
            _mock_validar (MagicMock): Mock para saltar la validación.
        Hace:
            Llama a `ejecutar_movimiento` (normal) en un estado donde
            la validación pasa (mockeada) pero la ejecución falla
            (no hay dado 3, solo dado 1).
        Devuelve:
            Verifica que se lance `ValueError` por "Dado no encontrado...".
        """
        self._setup_checkers(20, "W", 1)
        self.game.__dados_restantes__ = [1]
        with self.assertRaisesRegex(ValueError, "Dado no encontrado"):
            self.game.ejecutar_movimiento(20, 17)


if __name__ == "__main__":
    unittest.main()