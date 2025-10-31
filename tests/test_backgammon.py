"""
Pruebas unitarias para la clase BackgammonGame.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.game.backgammon import BackgammonGame
from src.game.checker import Checker


class TestBackgammonGame(unittest.TestCase):
    """Conjunto de pruebas para la clase BackgammonGame."""

    def setUp(self):
        """
        Configura un entorno de prueba nuevo antes de cada método de test.
        """
        self.game = BackgammonGame()
        # Los dados se definen en cada test para mayor aislamiento

    def _setup_checkers(self, point, color, count):
        """
        Método auxiliar para colocar un número específico de fichas de un
        color en un punto del tablero para configurar escenarios de prueba.
        """
        self.game.__board__.__puntos__[point] = [Checker(color) for _ in range(count)]

    def test_turno_inicial(self):
        """Verifica que el juego comience en el turno 0."""
        self.assertEqual(self.game.__turno__, 0)

    def test_jugadores_iniciales(self):
        """
        Verifica que el juego se inicialice con dos jugadores
        y que sus colores (fichas) sean 'W' (Blancas) y 'B' (Negras).
        """
        jugadores = self.game.__players__
        self.assertEqual(len(jugadores), 2)
        # --- CORREGIDO (Cumple DIP) ---
        self.assertEqual(jugadores[0].ficha, "W")
        self.assertEqual(jugadores[1].ficha, "B")

    @patch('src.game.dado.Dice.get_dice', return_value=(1, 2))
    def test_tirar_dados__actualiza_dados_restantes_con_lista(self, mock_dice):
        """
        Verifica que tirar_dados() retorna una lista (de 2 o 4 dados)
        y la almacena correctamente en self.__dados_restantes__.
        """
        dados = self.game.tirar_dados()
        self.assertIsInstance(self.game.__dados_restantes__, list)
        self.assertEqual(dados, self.game.__dados_restantes__)
        self.assertEqual(dados, [1, 2])
        mock_dice.assert_called_once()

    @patch('src.game.dado.Dice.get_dice', return_value=(6, 6, 6, 6))
    def test_tirar_dados__con_patch_para_dobles(self, mock_get_dice):
        """
        Prueba que tirar_dados() maneja correctamente los dobles
        usando @patch.
        """
        dados = self.game.tirar_dados()
        mock_get_dice.assert_called_once()
        self.assertEqual(dados, [6, 6, 6, 6])
        self.assertEqual(self.game.__dados_restantes__, [6, 6, 6, 6])

    def test_validar_movimiento_desde_barra__es_correcto_para_ambos_colores(self):
        """
        Prueba la validación de movimientos para sacar fichas de la barra
        (inicio 24 para Blancas, -1 para Negras).
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
        Prueba que validar_movimiento devuelva False si el punto de destino
        está bloqueado por dos o más fichas del oponente.
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
        Prueba que validar_movimiento devuelva True si el punto de destino
        contiene exactamente una ficha oponente (un 'blot').
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
        Prueba validaciones de movimientos básicos incorrectos, como
        mover desde un punto vacío, o moverse en la dirección incorrecta (hacia atrás).
        """
        self.game.__dados_restantes__ = [5]

        self.game.__board__.__puntos__[1] = []
        self.assertFalse(self.game.validar_movimiento(1, 6)[0])

        self._setup_checkers(5, "W", 1)
        self.assertFalse(self.game.validar_movimiento(5, 1)[0])

    def test_validar_movimiento__falla_si_puntos_estan_fuera_del_tablero(self):
        """
        Prueba que la validación falla si el punto de inicio o
        fin está fuera del rango legal (-1 a 25).
        """
        self.assertFalse(self.game.validar_movimiento(20, 26)[0])
        self.assertFalse(self.game.validar_movimiento(-2, 5)[0])

    def test_validar_movimiento_bear_off_exacto(self):
        """Verifica que se permita salir con dado exacto si está en Home Board."""
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
        """Verifica que se permita salir con dado mayor si es la ficha más lejana."""
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
        """Verifica que NO se permita salir con dado mayor si NO es la ficha más lejana."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self._setup_checkers(4, "W", 1)
        self.game.__dados_restantes__ = [5]
        self.assertFalse(self.game.validar_movimiento(2, -1)[0])

    def test_validar_movimiento_bear_off_falla_si_no_home_board(self):
        """Verifica que Bear Off falle si no todas las fichas están en Home Board."""
        self._setup_checkers(6, "W", 1)
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(2, -1)[0])

    def test_validar_movimiento__falla_si_hay_fichas_en_barra_y_no_es_mov_barra(self):
        """
        Prueba que no se permite mover fichas del tablero (normal o bear off)
        si el jugador tiene fichas pendientes en la barra.
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
        """Prueba que la ejecución de un movimiento desde la barra la vacía."""
        self.game.__board__.__bar_blancas__.append(Checker("W"))
        self.game.__dados_restantes__ = [3, 5]

        self.game.ejecutar_movimiento(24, 21)

        self.assertEqual(len(self.game.__board__.__bar_blancas__), 0)
        self.assertEqual(self.game.__board__.get_point_info(21)[1], 1)
        self.assertEqual(self.game.__dados_restantes__, [5])

    def test_ejecutar_movimiento__lanza_error_si_movimiento_no_es_valido(self):
        """
        Prueba que ejecutar_movimiento lanza un ValueError si se intenta
        ejecutar un movimiento que no pasó la validación.
        """
        self._setup_checkers(20, "W", 1)
        self.game.__dados_restantes__ = [1]
        with self.assertRaisesRegex(ValueError, "No tienes un dado de 3."):
            self.game.ejecutar_movimiento(20, 17)

    def test_ejecutar_movimiento_bear_off(self):
        """Verifica que ejecutar_movimiento quite la ficha al hacer Bear Off."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.game.ejecutar_movimiento(2, -1)

        self.assertEqual(self.game.__board__.get_point_info(2)[1], 0)
        self.assertEqual(self.game.__dados_restantes__, [])

    @patch('src.game.backgammon.BackgammonGame.validar_movimiento', return_value=(True, None))
    def test_ejecutar_movimiento__lanza_valueerror_si_logica_bear_off_falla(self, mock_validar):
        """
        Prueba que se lanza un error si la lógica de bear off falla internamente,
        usando un mock para saltar la validación principal.
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [1]
        with self.assertRaisesRegex(ValueError, "Lógica de dados inconsistente"):
            self.game.ejecutar_movimiento(2, -1)

    def test_ejecutar_movimiento__bear_off_usa_dado_mayor_si_es_ficha_lejana(self):
        """
        Prueba que el bear off (con un dado más alto que el necesario)
        usa el dado más alto si la ficha es la más lejana a la salida.
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, "W", 1)
        self.game.__dados_restantes__ = [5]
        self.assertTrue(self.game.validar_movimiento(2, -1)[0])
        self.game.ejecutar_movimiento(2, -1)
        self.assertEqual(self.game.__board__.get_point_info(2)[1], 0)
        self.assertEqual(self.game.__dados_restantes__, [])

    def test_check_victory(self):
        """Verifica la condición de victoria."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self.game.__board__.__bar_blancas__ = []
        self._setup_checkers(20, "B", 1)

        self.assertTrue(self.game.check_victory())

        self.game.__turno__ = 1
        self.assertFalse(self.game.check_victory())

    @patch('src.game.backgammon.BackgammonGame._get_strategy_key', return_value="desconocida")
    def test_validar_movimiento__falla_si_clave_estrategia_no_existe(self, mock_get_key):
        """
        Cubre el branch 'if clave_estrategia not in self.__estrategias_validacion__'.
        """
        self.assertFalse(self.game.validar_movimiento(23, 20)[0])

    def test_validar_bear_off__falla_si_no_hay_dados_disponibles(self):
        """
        Cubre el branch 'if not available_dice' en _validar_bear_off.
        """
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(4, "W", 1)
        self.game.__dados_restantes__ = [3]
        self.assertFalse(self.game.validar_movimiento(4, -1)[0])

    def test_ejecutar_movimiento_normal_con_hit(self):
        """
        Prueba la ejecución de un movimiento que resulta en un 'hit'.
        Cubre el branch 'if end_color is not None...' en _ejecutar_movimiento_tablero.
        """
        self._setup_checkers(18, "W", 1)
        self._setup_checkers(15, "B", 1)
        self.game.__dados_restantes__ = [3]

        self.game.ejecutar_movimiento(18, 15)

        self.assertEqual(self.game.__board__.get_bar_count("B"), 1)
        self.assertEqual(self.game.__board__.get_point_info(15)[0], "W")
        self.assertEqual(self.game.__dados_restantes__, [])

    @patch('src.game.backgammon.BackgammonGame.validar_movimiento', return_value=(True, None))
    def test_ejecutar_movimiento__lanza_valueerror_dado_no_encontrado_normal(self, mock_validar):
        """
        Cubre el branch 'else: raise ValueError("Dado no encontrado...")'
        en usar_dado_para_movimiento.
        """
        self._setup_checkers(20, "W", 1)
        self.game.__dados_restantes__ = [1]
        with self.assertRaisesRegex(ValueError, "Dado no encontrado"):
            self.game.ejecutar_movimiento(20, 17)


if __name__ == "__main__":
    unittest.main()