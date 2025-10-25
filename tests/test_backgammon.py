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

    def test_validar_movimiento_bloqueado(self):
        """Verifica que el movimiento sea inválido si el destino está bloqueado (2+ fichas rivales)."""       
        self.game.__board__.__puntos__[18] = -2        
        self.game.__board__.__puntos__[21] = 1 
        self.game.__dados_restantes__ = [3] 
        self.assertFalse(self.game.validar_movimiento(21, 18), 
                         "Error: Movimiento a punto bloqueado (-2) debe ser inválido.")
        self.game.__turno__ = 1 
        self.game.__board__.__puntos__[6] = 3         
        self.game.__board__.__puntos__[3] = -1 
        self.game.__dados_restantes__ = [3] 
        self.assertFalse(self.game.validar_movimiento(3, 6),
                         "Error: Movimiento a punto bloqueado (+3) debe ser inválido.")


    def test_validar_movimiento_hit_valido(self):
        """Verifica que el movimiento sea válido si el destino tiene 1 ficha rival (HIT)."""        
        self.game.__board__.__puntos__[15] = -1         
        self.game.__board__.__puntos__[18] = 1 
        self.game.__dados_restantes__ = [3] 
        self.assertTrue(self.game.validar_movimiento(18, 15),
                        "Error: Movimiento a punto HIT (-1) debe ser válido.")
        self.game.__turno__ = 1 
        self.game.__board__.__puntos__[9] = 1         
        self.game.__board__.__puntos__[6] = -1 
        self.game.__dados_restantes__ = [3] 
        self.assertTrue(self.game.validar_movimiento(6, 9),
                        "Error: Movimiento a punto HIT (+1) debe ser válido.")


    def test_validar_movimiento_basico_fallos(self):
        """Verifica fallos en origen, dirección y dado."""        
        self.game.__dados_restantes__ = [5]
        self.game.__board__.__puntos__[1] = 0
        self.assertFalse(self.game.validar_movimiento(1, 6),
                         "Falla: Mover desde origen vacío.")                         
        self.game.__board__.__puntos__[23] = 1 
        self.assertFalse(self.game.validar_movimiento(23, 24),
                         "Falla: Mover en dirección positiva (incorrecta para blancas).")
        self.assertFalse(self.game.validar_movimiento(5, 1), 
                         "Falla: Mover con dado no disponible.")

if __name__ == '__main__':
    unittest.main()