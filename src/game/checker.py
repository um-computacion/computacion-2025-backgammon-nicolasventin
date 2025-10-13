class Checker:
    def __init__(self, color: str) -> None:
        self.__color: str = color
        self.__esta_comida = False

    def get_color(self) -> str:
        return self.__color

    @property
    def comida(self):
        return self.__esta_comida
    
    @comida.setter
    def set_comida(self, esta_comida: bool) -> None:
        self.__esta_comida = esta_comida
