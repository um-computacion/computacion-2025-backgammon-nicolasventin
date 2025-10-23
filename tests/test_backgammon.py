import unittest
from src.game.backgammon import BackgammonGame

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.game = BackgammonGame()

    def test_turno_inicial(self):
        self.assertEqual(self.game.__turno__, 0)

    def test_jugadores_iniciales(self):
        jugadores = self.game.__players__
        self.assertEqual(len(jugadores), 2)
        self.assertEqual(jugadores[0].__ficha__, "B")
        self.assertEqual(jugadores[1].__ficha__, "N")

if __name__ == '__main__':
    unittest.main()