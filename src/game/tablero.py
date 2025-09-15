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