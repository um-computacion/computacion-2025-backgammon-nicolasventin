class Tablero:
    """Clase que maneja el estado del tablero de Backgammon."""
    def __init__(self):
        """Inicializa el tablero con posiciones y el estado del juego."""
        self.__turnos__ = 0
        self.__puntos__ = [0] * 24

        # Posiciones iniciales
        self.__puntos__[0] =  2    # 2 blancas
        self.__puntos__[11] = 5    # 5 blancas
        self.__puntos__[16] = 3    # 3 blancas
        self.__puntos__[18] = 5    # 5 blancas

        self.__puntos__[23] = -2   # 2 negras
        self.__puntos__[12] = -5   # 5 negras
        self.__puntos__[7]  = -3   # 3 negras
        self.__puntos__[5]  = -5   # 5 negras

    def draw(self):
        """Devuelve la grilla del tablero (matriz 10x12) como estructura de datos."""
        height, width = 10, 12
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        # Mitad superior: columnas 0..11 representan puntos 11..0 (izq -> der)
        for c in range(12):
            point = 11 - c
            owner, n = self._owner_and_count_from_puntos(point)
            if not owner or n == 0:
                continue
            piece = self._piece(owner)
            if n <= 5:
                for r in range(n):         # apilar desde arriba
                    grid[r][c] = piece
            else:
                for r in range(4):
                    grid[r][c] = piece
                grid[4][c] = str(n - 4)   # contador en fila 5 (índice 4)

        # Mitad inferior: columnas 0..11 representan puntos 12..23 (izq -> der)
        for c in range(12):
            point = 12 + c
            owner, n = self._owner_and_count_from_puntos(point)
            if not owner or n == 0:
                continue
            piece = self._piece(owner)
            if n <= 5:
                for k in range(n):         # apilar desde abajo
                    grid[9 - k][c] = piece
            else:
                for k in range(4):
                    grid[9 - k][c] = piece
                grid[5][c] = str(n - 4)    # contador en fila 6 (índice 5)

        return grid
    
    def mover_ficha(self, start_point: int, end_point: int):
        """Mueve una ficha de start_point a end_point. Asume que el movimiento es válido."""
        if start_point < 0 or start_point > 23:
             raise ValueError("Punto de inicio fuera de rango (0-23).")
        if self.__puntos__[start_point] > 0:
            checker_value = 1
        elif self.__puntos__[start_point] < 0:
            checker_value = -1
        else:
            raise ValueError("No hay fichas para mover en el punto de inicio.")

    def _owner_and_count_from_puntos(self, idx: int):
        """Retorna el dueño ('white'/'black') y la cantidad de fichas en un punto."""
        v = self.__puntos__[idx]
        if v > 0:  return ('white', v)
        if v < 0:  return ('black', -v)
        return (None, 0)
    
    def _piece(self, owner: str) -> str:
        """Retorna el símbolo 'W' o 'B' para la representación de datos (no visual)."""
        return 'W' if owner == 'white' else 'B'


