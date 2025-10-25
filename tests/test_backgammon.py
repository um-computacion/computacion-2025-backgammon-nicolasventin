import unittest
from src.game.backgammon import BackgammonGame
from src.game.checker import Checker

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.game = BackgammonGame()
        self.game.__dados_restantes__ = [3, 5]

    def _setup_checkers(self, point, color, count):
        self.game.__board__.__puntos__[point] = [Checker(color) for _ in range(count)]
    
    def test_turno_inicial(self):
        self.assertEqual(self.game.__turno__, 0)

    def test_jugadores_iniciales(self):
        jugadores = self.game.__players__
        self.assertEqual(len(jugadores), 2)
        self.assertEqual(jugadores[0].__ficha__, "B")
        self.assertEqual(jugadores[1].__ficha__, "N")

    def test_validar_movimiento_bloqueado(self):
        
        self._setup_checkers(18, 'N', 2) 
        self._setup_checkers(21, 'B', 1) 
        self.game.__dados_restantes__ = [3] 

        self.assertFalse(self.game.validar_movimiento(21, 18))

        self.game.__turno__ = 1 
        self._setup_checkers(6, 'B', 3) 
        self._setup_checkers(3, 'N', 1) 
        self.game.__dados_restantes__ = [3] 

        self.assertFalse(self.game.validar_movimiento(3, 6))


    def test_validar_movimiento_hit_valido(self):
        
        self._setup_checkers(15, 'N', 1) 
        self._setup_checkers(18, 'B', 1) 
        self.game.__dados_restantes__ = [3] 

        self.assertTrue(self.game.validar_movimiento(18, 15))

        self.game.__turno__ = 1 
        self._setup_checkers(9, 'B', 1) 
        self._setup_checkers(6, 'N', 1) 
        self.game.__dados_restantes__ = [3]

        self.assertTrue(self.game.validar_movimiento(6, 9))


    def test_validar_movimiento_basico_fallos(self):
        
        self.game.__dados_restantes__ = [5]
        
        self.game.__board__.__puntos__[1] = []
        self.assertFalse(self.game.validar_movimiento(1, 6))
                         
        self._setup_checkers(23, 'B', 1) 
        self.assertFalse(self.game.validar_movimiento(23, 24))

        self._setup_checkers(5, 'B', 1) 
        self.assertFalse(self.game.validar_movimiento(5, 1))

if __name__ == '__main__':
    unittest.main()