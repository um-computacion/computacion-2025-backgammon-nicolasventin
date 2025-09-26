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

    def test_blancas(self):
        self.assertEqual(self.tablero._format_ficha(2), "2B")
        self.assertEqual(self.tablero._format_ficha(5), "5B")

    def test_negras(self):
        self.assertEqual(self.tablero._format_ficha(-1), "1N")
        self.assertEqual(self.tablero._format_ficha(-4), "4N")

    def test_vacio(self):
        self.assertEqual(self.tablero._format_ficha(0), "--")

    def test_draw(self):
        board = Tablero()
        board.pos[0] = ('white', 3)
        board.pos[1] = ('white', 8)
        board.pos[23] = ('black', 1)
        board.pos[22] = ('black', 3)
        print(board.draw())
        board_draw = board.draw()
        print(f"board 0, 11: {board_draw[11][0]}")
        self.assertEqual(
            board.draw(),
            [ # 10
                [ # 1
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', 
                ],
                [ # 2
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', 
                ],
                [ # 3
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', 
                ],
                [ # 4
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 
                ],
                [ # 5
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', 
                ],
                [ # 6
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 
                ],
                [ # 7
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 
                ],
                [ # 8
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 
                ],
                [ # 9
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 
                ],
                [ # 10
                    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 
                ],
            ]
        )


if __name__ == '__main__':  
    unittest.main()
