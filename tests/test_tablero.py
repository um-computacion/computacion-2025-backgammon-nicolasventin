import unittest
from src.game.tablero import Tablero

class TestTablero(unittest.TestCase):
    def test__init__(self):
        self.tablero = Tablero()

    def test__turnos__(self):
        self.assertEqual(self.tablero.__turnos__, 0)


if __name__ == '__main__':  
    unittest.main()
        