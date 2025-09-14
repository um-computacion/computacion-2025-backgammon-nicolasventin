import unittest
from src.game.tablero import Tablero

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()

    def test__turnos__(self):
        self.assertEqual(self.tablero.__turnos__, 0)

    def test__cantidad_de_posiciones__(self):
        self.assertEqual(len(self.tablero._Tablero__puntos__), 24)

    def test_posiciones_iniciales(self):
        posiciones_esperadas = [0] * 24
        posiciones_esperadas[0]  =  2
        posiciones_esperadas[11] =  5
        posiciones_esperadas[16] =  3
        posiciones_esperadas[18] =  5
        posiciones_esperadas[23] = -2
        posiciones_esperadas[12] = -5
        posiciones_esperadas[7]  = -3
        posiciones_esperadas[5]  = -5

        self.assertEqual(self.tablero._Tablero__puntos__, posiciones_esperadas)


if __name__ == '__main__':  
    unittest.main()
        