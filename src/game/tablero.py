class Tablero:
    def __init__(self):
        self.__turnos__ = 0
        self.__puntos__ = [0] * 24

        self.__puntos__[0] =  2    # 2 blancas
        self.__puntos__[11] = 5    # 5 blancas
        self.__puntos__[16] = 3    # 3 blancas
        self.__puntos__[18] = 5    # 5 blancas

        self.__puntos__[23] = -2   # 2 negras
        self.__puntos__[12] = -5   # 5 negras
        self.__puntos__[7]  = -3   # 3 negras
        self.__puntos__[5]  = -5   # 5 negras

    def _format_ficha(self, v: int) -> str:
        if v > 0:
            return f"{v}B"
        elif v < 0:
            return f"{abs(v)}N"
        else:
            return "--"
        
    def mostrar(self):
        # Arriba: 11..0
        arriba_idx = list(range(11, -1, -1))
        # Abajo: 12..23
        abajo_idx  = list(range(12, 24))

        print("\n=== Tablero de Backgammon ===")
        # Fichas arriba
        print(" ".join(f"{i:02}" for i in arriba_idx))        
        print(" ".join(self._format_ficha(self.__puntos__[i]) for i in arriba_idx))
        # Separador
        print("-" * 60)
        # Fichas abajo
        print(" ".join(self._format_ficha(self.__puntos__[i]) for i in abajo_idx))
        print(" ".join(f"{i:02}" for i in abajo_idx))

        print("=============================\n")

    def draw(self):
        result_board = [] 
        for col in range(11, -1, -1):
            result_row = []
            result_board.append(result_row)
            for row in range(0, 5):
                if self.pos[col] is not None:
                    if self.pos[col][1] > row:
                        if row < 4:
                            piece = self.get_piece(col)
                        else:
                            if self.pos[col][1] <= 5:
                                piece = self.get_piece(col)
                            else:
                                piece = str(self.pos[col][1] - 4)
                        result_row.append(piece)
                    else:
                        result_row.append(' ')    
                else:
                    result_row.append(' ')

        height, width = 10, 12
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        for r in range(5):          # solo la mitad superior
            for c in range(12):
                grid[r][c] = result_board[c][r]  # transponer 12x5 -> 5x12 (arriba)

        return grid

    def _owner_and_count_from_puntos(self, idx: int):
        v = self.__puntos__[idx]
        if v > 0:  return ('white', v)
        if v < 0:  return ('black', -v)
        return (None, 0)

