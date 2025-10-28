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
    
    def test_validar_movimiento_bear_off_exacto(self):
        """Verifica que se permita salir con dado exacto si está en Home Board."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self.game.__board__.__bar_blancas__ = []
        self.game.__board__.__bar_negras__ = []
        self._setup_checkers(2, 'B', 1)
        self.game.__dados_restantes__ = [3]

        self.assertTrue(self.game.validar_movimiento(2, -1))

        self.game.__turno__ = 1
        for i in range(0, 18): self.game.__board__.__puntos__[i] = []
        self.game.__board__.__bar_blancas__ = []
        self.game.__board__.__bar_negras__ = []
        self._setup_checkers(21, 'N', 1)
        self.game.__dados_restantes__ = [3]

        self.assertTrue(self.game.validar_movimiento(21, 25))

    def test_validar_movimiento_bear_off_dado_mayor_lejana(self):
        """Verifica que se permita salir con dado mayor si es la ficha más lejana."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self.game.__board__.__bar_blancas__ = []
        self.game.__board__.__bar_negras__ = []
        self._setup_checkers(2, 'B', 1)
        self.game.__dados_restantes__ = [5]

        self.assertTrue(self.game.validar_movimiento(2, -1))

        self.game.__turno__ = 1
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self.game.__board__.__bar_blancas__ = []
        self.game.__board__.__bar_negras__ = []
        self._setup_checkers(21, 'N', 1)
        self.game.__dados_restantes__ = [5]

        self.assertTrue(self.game.validar_movimiento(21, 25))

    def test_validar_movimiento_bear_off_dado_mayor_no_lejana(self):
        """Verifica que NO se permita salir con dado mayor si NO es la ficha más lejana."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, 'B', 1)
        self._setup_checkers(4, 'B', 1)
        self.game.__dados_restantes__ = [5]

        self.assertFalse(self.game.validar_movimiento(2, -1))

    def test_validar_movimiento_bear_off_falla_si_no_home_board(self):
        """Verifica que Bear Off falle si no todas las fichas están en Home Board."""
        self._setup_checkers(6, 'B', 1)
        self._setup_checkers(2, 'B', 1)
        self.game.__dados_restantes__ = [3]

        self.assertFalse(self.game.validar_movimiento(2, -1))

    def test_ejecutar_movimiento_bear_off(self):
        """Verifica que ejecutar_movimiento quite la ficha al hacer Bear Off."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self._setup_checkers(2, 'B', 1)
        self.game.__dados_restantes__ = [3]
        self.game.ejecutar_movimiento(2, -1)

        self.assertEqual(len(self.game.__board__.__puntos__[2]), 0)
        self.assertEqual(self.game.__dados_restantes__, [])

    def test_check_victory(self):
        """Verifica la condición de victoria."""
        self.game.__board__.__puntos__ = [[] for _ in range(24)]
        self.game.__board__.__bar_blancas__ = []

        self._setup_checkers(20, 'N', 1)

        self.assertTrue(self.game.check_victory())

        self.game.__turno__ = 1
        self.assertFalse(self.game.check_victory())

if __name__ == '__main__':
    unittest.main()