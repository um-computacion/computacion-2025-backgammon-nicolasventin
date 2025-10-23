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

if __name__ == '__main__':  
    unittest.main()