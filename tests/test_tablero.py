import unittest
from src.game.tablero import Tablero
from src.game.checker import Checker

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()
    
    def _setup_checkers(self, point, color, count):
        """Helper para configurar un punto con objetos Checker."""
        from src.game.checker import Checker
        self.tablero.__puntos__[point] = [Checker(color) for _ in range(count)]

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
            self.tablero.mover_ficha(25, 23)
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(-2, 1)
        with self.assertRaises(Exception):
            self.tablero.mover_ficha(2, 3)
        with self.assertRaises(Exception):
            self.tablero.mover_ficha(24, 18)
        with self.assertRaises(Exception):
            self.tablero.mover_ficha(-1, 6)
    
    def test_get_piece_count(self):
        """Verifica que el conteo total de fichas en el tablero y barra sea correcto."""
        self.assertEqual(self.tablero.get_piece_count('B'), 15)
        self.assertEqual(self.tablero.get_piece_count('N'), 15)
        if self.tablero.__puntos__[0]:
            self.tablero.__puntos__[0].pop()
            self.assertEqual(self.tablero.get_piece_count('B'), 14)
        self.setUp() 
        removed_checker = None
        while len(self.tablero.__puntos__[23]) > 1:
             removed_checker = self.tablero.__puntos__[23].pop() 
        hit_occurred = self.tablero.hit_opponent(23)
        if removed_checker:
             self.tablero.__puntos__[7].append(removed_checker)
        self.assertTrue(hit_occurred)
        self.assertEqual(len(self.tablero.__bar_negras__), 1)
        self.assertEqual(self.tablero.get_piece_count('N'), 15)


    def test_is_home_board_ready(self):
        """Verifica la precondición de Bearing Off: todas las fichas en Home Board."""       
        self.assertFalse(self.tablero._is_home_board_ready('B'))
        self.assertFalse(self.tablero._is_home_board_ready('N'))

        self.tablero.__bar_blancas__.append(self.tablero.__puntos__[0].pop())
        self.assertFalse(self.tablero._is_home_board_ready('B'))
        self.tablero.__bar_blancas__ = []

        self.tablero.__puntos__[18].pop()
        self._setup_checkers(17, 'B', 1)
        self.assertFalse(self.tablero._is_home_board_ready('B'))
        
        self.tablero.__puntos__[5].pop()
        self._setup_checkers(6, 'N', 1)
        self.assertFalse(self.tablero._is_home_board_ready('N'))

        self.setUp()
        for i in range(6, 24): 
            self.tablero.__puntos__[i] = []
        self.assertTrue(self.tablero._is_home_board_ready('B'))

        self.setUp()
        for i in range(0, 18):
            self.tablero.__puntos__[i] = []
        self.assertTrue(self.tablero._is_home_board_ready('N'))   

if __name__ == '__main__':
    unittest.main()