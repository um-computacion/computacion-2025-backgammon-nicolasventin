import unittest
from src.game.tablero import Tablero

class TestTablero(unittest.TestCase):
    def test__init__(self):
        self.tablero = Tablero()

    def test__turnos__(self):
        self.assertEqual(self.tablero.__turnos__, 0)

    def test__cantidad_de_posiciones__(self):
        self.assertEqual(self.tablero.__cantidad_de_posiciones__, 24)

    def test_posiciones_iniciales(self):
        posiciones_esperadas = [
            (2, "Blancas"),
            (0, None), 
            (0, None), 
            (0, None), 
            (0, None), 
            (5, "Negras"),
            (0, None), 
            (3, "Negras"), 
            (0, None), 
            (0, None), 
            (0, None), 
            (5, "Blancas"),
            (5, "Negras"), 
            (0, None), 
            (0, None), 
            (0, None), 
            (3, "Blancas"), 
            (0, None),
            (5, "Blancas"), 
            (0, None), 
            (0, None), 
            (0, None), 
            (0, None), 
            (2, "Negras")
        ]
        self.assertEqual(self.tablero._Tablero__posiciones__, posiciones_esperadas)


if __name__ == '__main__':  
    unittest.main()
        