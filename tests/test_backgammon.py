import unittest
from src.game.backgammon import BackgammonGame

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.game = BackgammonGame()


if __name__ == '__main__':
    unittest.main()