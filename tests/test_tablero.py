import unittest
from src.game.tablero import Tablero

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()

    def test__turnos__(self):
        self.assertEqual(self.tablero.__turnos__, 0)

    def test__cantidad_de_posiciones__(self):
        self.assertEqual(len(self.tablero.__puntos__), 24)

    def test_posiciones_iniciales(self):
        posiciones_esperadas = [0] * 24
        posiciones_esperadas[0]  =  2
        posiciones_esperadas[11] =  5
        posiciones_esperadas[16] =  3
        posiciones_esperadas[18] =  5
        posiciones_esperadas[23] = -2
        posiciones_esperadas[12] = -5
        posiciones_esperadas[7]  = -3
        posiciones_esperadas[5]  = -5

        self.assertEqual(self.tablero.__puntos__, posiciones_esperadas)

    def test_owner_and_count_from_puntos(self):
        """Prueba si el método interpreta correctamente el valor del punto."""
        self.assertEqual(self.tablero._owner_and_count_from_puntos(0), ('white', 2))
        self.assertEqual(self.tablero._owner_and_count_from_puntos(23), ('black', 2))
        self.assertEqual(self.tablero._owner_and_count_from_puntos(1), (None, 0))

    def test_piece(self):
        """Prueba el mapeo de dueño a símbolo de ficha de datos."""
        self.assertEqual(self.tablero._piece('white'), "W")
        self.assertEqual(self.tablero._piece('black'), "B")

    def test_draw(self):
        """Verifica que la estructura de datos 10x12 sea correcta."""
        board = Tablero()
        board_draw = board.draw()
        
        # Punto 0 (2 blancas) -> Columna 11 superior
        self.assertEqual(board_draw[0][11], 'W')
        self.assertEqual(board_draw[1][11], 'W') 
        
        # Prueba la lógica de conteo (>5) en el punto 11 (columna 0 superior)
        board.__puntos__[11] = 8 
        board_draw_over_5 = board.draw()
        self.assertEqual(board_draw_over_5[0][0], 'W')
        self.assertEqual(board_draw_over_5[3][0], 'W')
        self.assertEqual(board_draw_over_5[4][0], '4') # Contador

    def test_mover_ficha_blanca(self):
        """Verifica el movimiento de una ficha blanca (0 -> 1)."""
        start_point, end_point = 0, 1
        
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(self.tablero.__puntos__[start_point], 1)
        self.assertEqual(self.tablero.__puntos__[end_point], 1)

    def test_mover_ficha_negra(self):
        """Verifica el movimiento de una ficha negra (23 -> 22)."""
        start_point, end_point = 23, 22
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(self.tablero.__puntos__[start_point], -1)
        self.assertEqual(self.tablero.__puntos__[end_point], -1)

    def test_mover_ficha_errores(self):
        """Verifica que se lancen las excepciones esperadas (rango y vacío)."""
        with self.assertRaises(ValueError, msg="Debería lanzar ValueError para índice fuera de rango (24)."):
            self.tablero.mover_ficha(24, 23)
        with self.assertRaises(Exception, msg="Debería lanzar Exception al intentar mover ficha desde punto vacío (índice 2)."):
            self.tablero.mover_ficha(2, 3)

if __name__ == '__main__':  
    unittest.main()