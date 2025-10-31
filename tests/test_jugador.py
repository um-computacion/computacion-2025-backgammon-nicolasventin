"""
Modulo de pruebas unitarias para la clase Jugador.
"""
import unittest
from src.game.jugador import Jugador


class TestJugador(unittest.TestCase):
    """Pruebas para la clase Jugador."""
    def test_crear_jugador(self):
        """
        Verifica que el constructor de Jugador asigne el nombre 
        y el color de ficha correctamente.
        """
        jugador = Jugador("Diego", "W")
        self.assertEqual(jugador.nombre, "Diego")
        self.assertEqual(jugador.ficha, "W")

    def test_obtener_info(self):
        """Prueba que el método obtener_info devuelva el string formateado esperado."""
        jugador = Jugador("Camila", "B")
        resultado = jugador.obtener_info()
        self.assertEqual(resultado, "Camila (B)")

    def test_is_white(self):
        """Prueba que el helper is_white() devuelva el booleano correcto."""
        jugador_blanco = Jugador("Player 1", "W")
        jugador_negro = Jugador("Player 2", "B")
        self.assertTrue(jugador_blanco.is_white())
        self.assertFalse(jugador_negro.is_white())


if __name__ == "__main__":
    unittest.main()
