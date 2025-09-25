import unittest
from src.game.jugador import Jugador

class TestJugador(unittest.TestCase):
    
    def test_crear_jugador(self):
        jugador = Jugador("Diego", "Blancas")
        self.assertEqual(jugador.nombre, "Diego")
        self.assertEqual(jugador.ficha, "Blancas")

    def test_obtener_info(self):
        jugador = Jugador("Camila", "Negras")
        resultado = jugador.obtener_info()
        self.assertEqual(resultado, "Camila (Negras)")