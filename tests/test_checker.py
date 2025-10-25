import unittest
from src.game.checker import Checker

class TestChecker(unittest.TestCase):
    def test_creacion_blanca(self):
        checker = Checker('B')
        self.assertEqual(checker.get_color(), 'B')
        self.assertFalse(checker.comida)

    def test_creacion_negra(self):
        checker = Checker('N')
        self.assertEqual(checker.get_color(), 'N')
        self.assertFalse(checker.comida)
        
    def test_propiedad_comida_setter(self):
        checker = Checker('B')
        
        checker.comida = True
        self.assertTrue(checker.comida)
        
        checker.comida = False
        self.assertFalse(checker.comida)

if __name__ == '__main__':
    unittest.main()