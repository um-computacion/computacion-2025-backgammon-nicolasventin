"""
Modulo de pruebas unitarias para la clase Jugador.
"""
import unittest
from src.game.jugador import Jugador


class TestJugador(unittest.TestCase):
    """Pruebas para la clase Jugador."""

    def test_crear_jugador(self):
        """
        Recibe:
            Nada.
        Hace:
            Crea una instancia de Jugador con nombre "Diego" y ficha "W".
        Devuelve:
            Verifica que las propiedades `nombre` y `ficha` se
            asignen correctamente.
        """
        jugador = Jugador("Diego", "W")
        self.assertEqual(jugador.nombre, "Diego")
        self.assertEqual(jugador.ficha, "W")

    def test_obtener_info(self):
        """
        Recibe:
            Nada.
        Hace:
            Crea un Jugador y llama a `obtener_info()`.
        Devuelve:
            Verifica que el string formateado devuelto sea "Camila (B)".
        """
        jugador = Jugador("Camila", "B")
        resultado = jugador.obtener_info()
        self.assertEqual(resultado, "Camila (B)")

    def test_is_white(self):
        """
        Recibe:
            Nada.
        Hace:
            Crea un jugador Blanco ('W') y un jugador Negro ('B').
            Llama a `is_white()` en ambos.
        Devuelve:
            Verifica que `is_white()` devuelva True para el jugador 'W'
            y False para el jugador 'B'.
        """
        jugador_blanco = Jugador("Player 1", "W")
        jugador_negro = Jugador("Player 2", "B")
        self.assertTrue(jugador_blanco.is_white())
        self.assertFalse(jugador_negro.is_white())


if __name__ == "__main__":
    unittest.main()
