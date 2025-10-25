import unittest
from src.game.tablero import Tablero
from src.game.checker import Checker

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()

    def test__turnos__(self):
        self.assertEqual(self.tablero.__turnos__, 0)

    def test__cantidad_de_posiciones__(self):
        self.assertEqual(len(self.tablero.__puntos__), 24)

    def test_posiciones_iniciales(self):
        self.assertEqual(len(self.tablero.__puntos__[0]), 2)
        self.assertEqual(self.tablero.__puntos__[0][0].get_color(), 'B')
        self.assertEqual(len(self.tablero.__puntos__[11]), 5)
        self.assertEqual(self.tablero.__puntos__[11][0].get_color(), 'B')
        self.assertEqual(len(self.tablero.__puntos__[16]), 3)
        self.assertEqual(self.tablero.__puntos__[16][0].get_color(), 'B')
        self.assertEqual(len(self.tablero.__puntos__[18]), 5)
        self.assertEqual(self.tablero.__puntos__[18][0].get_color(), 'B')

        self.assertEqual(len(self.tablero.__puntos__[23]), 2)
        self.assertEqual(self.tablero.__puntos__[23][0].get_color(), 'N')
        self.assertEqual(len(self.tablero.__puntos__[12]), 5)
        self.assertEqual(self.tablero.__puntos__[12][0].get_color(), 'N')
        self.assertEqual(len(self.tablero.__puntos__[7]), 3)
        self.assertEqual(self.tablero.__puntos__[7][0].get_color(), 'N')
        self.assertEqual(len(self.tablero.__puntos__[5]), 5)
        self.assertEqual(self.tablero.__puntos__[5][0].get_color(), 'N')

        self.assertEqual(len(self.tablero.__bar_blancas__), 0)
        self.assertEqual(len(self.tablero.__bar_negras__), 0)

    def test_owner_and_count_from_puntos(self):
        owner, count = self.tablero._owner_and_count_from_puntos(0)
        self.assertEqual(owner, 'white')
        self.assertEqual(count, 2)
        
        owner, count = self.tablero._owner_and_count_from_puntos(23)
        self.assertEqual(owner, 'black')
        self.assertEqual(count, 2)
        
        self.assertEqual(self.tablero._owner_and_count_from_puntos(1), (None, 0))

    def test_piece(self):
        self.assertEqual(self.tablero._piece('white'), "W")
        self.assertEqual(self.tablero._piece('black'), "B")

    def test_draw(self):
        board = Tablero()
        board_draw = board.draw()
        
        self.assertEqual(board_draw[0][11], 'W')
        self.assertEqual(board_draw[1][11], 'W') 
        
        for _ in range(3):
            board.__puntos__[11].append(Checker('B'))
            
        board_draw_over_5 = board.draw()
        self.assertEqual(board_draw_over_5[0][0], 'W')
        self.assertEqual(board_draw_over_5[3][0], 'W')
        self.assertEqual(board_draw_over_5[4][0], '4') 
    
    def test_hit_opponent(self):
        self.tablero.__puntos__[10] = [Checker('N')]
        self.tablero.hit_opponent(10)
        
        self.assertEqual(len(self.tablero.__puntos__[10]), 0)
        self.assertEqual(len(self.tablero.__bar_negras__), 1)
        self.assertTrue(self.tablero.__bar_negras__[0].comida)
        
        self.tablero.__puntos__[15] = [Checker('B')]
        self.tablero.hit_opponent(15)
        
        self.assertEqual(len(self.tablero.__puntos__[15]), 0)
        self.assertEqual(len(self.tablero.__bar_blancas__), 1)
        self.assertTrue(self.tablero.__bar_blancas__[0].comida)
        
        self.tablero.__puntos__[5] = [Checker('N'), Checker('N')]
        self.assertFalse(self.tablero.hit_opponent(5))

    def test_mover_ficha_blanca(self):
        start_point, end_point = 0, 1
        
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].get_color(), 'B')

    def test_mover_ficha_negra(self):
        start_point, end_point = 23, 22
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].get_color(), 'N')

    def test_mover_ficha_errores(self):
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(24, 23)
        with self.assertRaises(Exception):
            self.tablero.mover_ficha(2, 3)