"""
Modulo de pruebas unitarias para la clase Tablero.
"""
import unittest
from src.game.tablero import Tablero
from src.game.checker import Checker


class TestTablero(unittest.TestCase):
    """Pruebas para la clase Tablero."""

    def setUp(self):
        """
        Recibe:
            Nada.
        Hace:
            Se ejecuta antes de cada método de prueba. Crea una
            instancia nueva de `Tablero` (self.tablero).
        Devuelve:
            Nada.
        """
        self.tablero = Tablero()

    def _setup_checkers(self, point, color, count):
        """
        Recibe:
            point (int): El índice del punto a modificar.
            color (str): 'W' o 'B'.
            count (int): Número de fichas a colocar.
        Hace:
            Helper interno para configurar escenarios de prueba. Sobrescribe
            un punto del tablero con un número específico de fichas.
        Devuelve:
            Nada.
        """
        self.tablero.__puntos__[point] = [Checker(color) for _ in range(count)]

    def test__turnos__(self):
        """
        Recibe:
            Nada.
        Hace:
            Comprueba el valor inicial del atributo `__turnos__`.
        Devuelve:
            Verifica que `self.tablero.__turnos__` sea 0.
        """
        self.assertEqual(self.tablero.__turnos__, 0)

    def test__cantidad_de_posiciones__(self):
        """
        Recibe:
            Nada.
        Hace:
            Comprueba la longitud de la lista `__puntos__`.
        Devuelve:
            Verifica que `len(self.tablero.__puntos__)` sea 24.
        """
        self.assertEqual(len(self.tablero.__puntos__), 24)

    def test_posiciones_iniciales(self):
        """
        Recibe:
            Nada.
        Hace:
            Verifica la configuración estándar del tablero al inicializarse.
        Devuelve:
            Comprueba el conteo y color de las fichas en todos los
            puntos iniciales (23, 12, 7, 5, 0, 11, 16, 18) y
            que las barras estén vacías.
        """
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
        """
        Recibe:
            Nada.
        Hace:
            Prueba la lógica de "comer" una ficha (hit).
            1. Simula un 'blot' (ficha única) 'B' en el punto 10 y lo golpea.
            2. Simula un 'blot' 'W' en el punto 15 y lo golpea.
            3. Simula un punto bloqueado ('B', 'B') en 5 e intenta golpearlo.
        Devuelve:
            Verifica que en 1 y 2, la ficha se mueva a la barra
            correspondiente y `comida` sea True.
            Verifica que en 3, `hit_opponent` devuelva False.
        """
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
        """
        Recibe:
            Nada.
        Hace:
            Ejecuta `mover_ficha` para una ficha Blanca ('W') de 23 a 22.
        Devuelve:
            Verifica que el conteo en el origen (23) decremente y
            el conteo en el destino (22) incremente.
        """
        start_point, end_point = 23, 22

        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].color, "W")

    def test_mover_ficha_negra(self):
        """
        Recibe:
            Nada.
        Hace:
            Ejecuta `mover_ficha` para una ficha Negra ('B') de 0 a 1.
        Devuelve:
            Verifica que el conteo en el origen (0) decremente y
            el conteo en el destino (1) incremente.
        """
        start_point, end_point = 0, 1
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].color, "B")

    def test_mover_ficha_errores(self):
        """
        Recibe:
            Nada.
        Hace:
            Intenta llamar a `mover_ficha` con parámetros inválidos:
            - Origen fuera de rango (25, -2).
            - Mover desde un punto vacío (2).
            - Mover desde barras vacías (24, -1).
        Devuelve:
            Verifica que `ValueError` se lance en todos los casos.
        """
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
        """
        Recibe:
            Nada.
        Hace:
            Prueba `get_piece_count` en varios escenarios:
            1. Estado inicial.
            2. Después de quitar una ficha 'W' (simula bear off).
            3. Después de golpear una ficha 'B' (debe seguir contando 15).
        Devuelve:
            Verifica que el conteo sea 15 (Caso 1 y 3) y 14 (Caso 2).
        """
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
        """
        Recibe:
            Nada.
        Hace:
            Prueba `is_home_board_ready` en múltiples escenarios:
            1. Estado inicial (Debe ser False).
            2. Con fichas en la barra (Debe ser False).
            3. Con fichas fuera del home board (Debe ser False).
            4. Con todas las fichas 'W' en 0-5 (Debe ser True).
            5. Con todas las fichas 'B' en 18-23 (Debe ser True).
        Devuelve:
            Verifica el booleano esperado para cada escenario.
        """
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