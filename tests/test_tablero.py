"""
Modulo de pruebas unitarias para la clase Tablero.
"""
import unittest
from src.game.tablero import Tablero
from src.game.checker import Checker


class TestTablero(unittest.TestCase):
    """Pruebas para la clase Tablero."""
    def setUp(self):
        """Configura un tablero nuevo antes de cada método de prueba."""
        self.tablero = Tablero()

    def _setup_checkers(self, point, color, count):
        """Helper para configurar un punto con objetos Checker."""
        self.tablero.__puntos__[point] = [Checker(color) for _ in range(count)]

    def test__turnos__(self):
        """Verifica que el contador de turnos se inicializa en 0."""
        self.assertEqual(self.tablero.__turnos__, 0)

    def test__cantidad_de_posiciones__(self):
        """Verifica que el tablero tenga las 24 posiciones (puntos) estándar."""
        self.assertEqual(len(self.tablero.__puntos__), 24)

    def test_posiciones_iniciales(self):
        """Verifica la configuración inicial estándar de las fichas en el tablero."""
        self.assertEqual(len(self.tablero.__puntos__[23]), 2)
        self.assertEqual(self.tablero.__puntos__[23][0].color, "W")
        self.assertEqual(len(self.tablero.__puntos__[12]), 5)
        self.assertEqual(self.tablero.__puntos__[12][0].color, "W")
        self.assertEqual(len(self.tablero.__puntos__[7]), 3)
        self.assertEqual(self.tablero.__puntos__[7][0].color, "W")
        self.assertEqual(len(self.tablero.__puntos__[5]), 5)
        self.assertEqual(self.tablero.__puntos__[5][0].color, "W")

        self.assertEqual(len(self.tablero.__puntos__[0]), 2)
        self.assertEqual(self.tablero.__puntos__[0][0].color, "B")
        self.assertEqual(len(self.tablero.__puntos__[11]), 5)
        self.assertEqual(self.tablero.__puntos__[11][0].color, "B")
        self.assertEqual(len(self.tablero.__puntos__[16]), 3)
        self.assertEqual(self.tablero.__puntos__[16][0].color, "B")
        self.assertEqual(len(self.tablero.__puntos__[18]), 5)
        self.assertEqual(self.tablero.__puntos__[18][0].color, "B")

        self.assertEqual(len(self.tablero.__bar_blancas__), 0)
        self.assertEqual(len(self.tablero.__bar_negras__), 0)

    def test_hit_opponent(self):
        """Verifica la lógica de 'comer' (hit) una ficha oponente (blot) y moverla a la barra."""
        self.tablero.__puntos__[10] = [Checker("B")]
        self.tablero.hit_opponent(10)

        self.assertEqual(len(self.tablero.__puntos__[10]), 0)
        self.assertEqual(len(self.tablero.__bar_negras__), 1)
        self.assertTrue(self.tablero.__bar_negras__[0].comida)

        self.tablero.__puntos__[15] = [Checker("W")]
        self.tablero.hit_opponent(15)

        self.assertEqual(len(self.tablero.__puntos__[15]), 0)
        self.assertEqual(len(self.tablero.__bar_blancas__), 1)
        self.assertTrue(self.tablero.__bar_blancas__[0].comida)

        self.tablero.__puntos__[5] = [Checker("B"), Checker("B")]
        self.assertFalse(self.tablero.hit_opponent(5))

    def test_mover_ficha_blanca(self):
        """Prueba un movimiento simple y válido de una ficha blanca."""
        start_point, end_point = 23, 22

        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].color, "W")

    def test_mover_ficha_negra(self):
        """Prueba un movimiento simple y válido de una ficha negra."""
        start_point, end_point = 0, 1
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].color, "B")

    def test_mover_ficha_errores(self):
        """Prueba que se lancen excepciones al intentar movimientos inválidos."""
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(25, 23)
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(-2, 1)
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(2, 3)
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(24, 18)
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(-1, 6)

    def test_get_piece_count(self):
        """Verifica que el conteo total de fichas en el tablero y barra sea correcto."""
        self.assertEqual(self.tablero.get_piece_count("W"), 15)
        self.assertEqual(self.tablero.get_piece_count("B"), 15)
        if self.tablero.__puntos__[23]:
            self.tablero.__puntos__[23].pop()
            self.assertEqual(self.tablero.get_piece_count("W"), 14)
        self.setUp()
        removed_checker = None
        while len(self.tablero.__puntos__[0]) > 1:
            removed_checker = self.tablero.__puntos__[0].pop()
        hit_occurred = self.tablero.hit_opponent(0)
        if removed_checker:
            self.tablero.__puntos__[11].append(removed_checker)
        self.assertTrue(hit_occurred)
        self.assertEqual(len(self.tablero.__bar_negras__), 1)
        self.assertEqual(self.tablero.get_piece_count("B"), 15)

    def test_is_home_board_ready(self):
        """Verifica la precondición de Bearing Off: todas las fichas en Home Board."""
        self.assertFalse(self.tablero.is_home_board_ready("W"))
        self.assertFalse(self.tablero.is_home_board_ready("B"))

        self.tablero.__bar_blancas__.append(Checker("W"))
        self.assertFalse(self.tablero.is_home_board_ready("W"))
        self.tablero.__bar_blancas__ = []

        self._setup_checkers(17, "W", 1)
        self.assertFalse(self.tablero.is_home_board_ready("W"))
        
        self.setUp()
        self._setup_checkers(6, "B", 1)
        self.assertFalse(self.tablero.is_home_board_ready("B"))

        self.setUp()
        for i in range(6, 24):
            self.tablero.__puntos__[i] = []
        self.assertTrue(self.tablero.is_home_board_ready("W"))

        self.setUp()
        for i in range(0, 18):
            self.tablero.__puntos__[i] = []
        self.assertTrue(self.tablero.is_home_board_ready("B"))


if __name__ == "__main__":
    unittest.main()
