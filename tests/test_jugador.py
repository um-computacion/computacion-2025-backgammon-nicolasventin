import unittest
from src.game.jugador import Jugador


class TestJugador(unittest.TestCase):

    def test_crear_jugador(self):
        jugador = Jugador("Diego", "Blancas")
        self.assertEqual(jugador.__nombre__, "Diego")
        self.assertEqual(jugador.__ficha__, "Blancas")

    def test_obtener_info(self):
        jugador = Jugador("Camila", "Negras")
        resultado = jugador.obtener_info()
        self.assertEqual(resultado, "Camila (Negras)")


if __name__ == "__main__":
    unittest.main()
