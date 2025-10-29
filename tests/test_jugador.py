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
        jugador = Jugador("Diego", "Blancas")
        self.assertEqual(jugador.__nombre__, "Diego")
        self.assertEqual(jugador.__ficha__, "Blancas")

    def test_obtener_info(self):
        """Prueba que el método obtener_info devuelva el string formateado esperado."""
        jugador = Jugador("Camila", "Negras")
        resultado = jugador.obtener_info()
        self.assertEqual(resultado, "Camila (Negras)")


if __name__ == "__main__":
    unittest.main()
