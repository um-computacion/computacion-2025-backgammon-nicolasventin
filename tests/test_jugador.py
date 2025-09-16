import unittest
from src.game.jugador import Jugador

class TestJugador(unittest.TestCase):
    
    def test_crear_jugador(self):
        jugador = Jugador("Diego", "Blanca")
        self.assertEqual(jugador.nombre, "Diego")
        self.assertEqual(jugador.ficha, "Blanca")