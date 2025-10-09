import unittest
from src.game.backgammon import BackgammonGame

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.game = BackgammonGame()

    def test_turno_inicial(self):
        self.assertEqual(self.game.__turno__, 0)

if __name__ == '__main__':
    unittest.main()