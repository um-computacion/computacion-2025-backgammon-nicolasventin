class Checker:
    """Representa una ficha individual de Backgammon."""
    
    def __init__(self, color: str) -> None:
        """Inicializa la ficha con su color ('B' o 'N') y estado."""
        self.__color__: str = color
        self.__esta_comida: bool = False

    def get_color(self) -> str:
        """Retorna el color de la ficha."""
        return self.__color__

    @property
    def comida(self) -> bool:
        """Retorna el estado de la ficha (si fue golpeada y está en la barra)."""
        return self.__esta_comida

    @comida.setter
    def comida(self, estado: bool) -> None:
        """Establece si la ficha ha sido golpeada."""
        self.__esta_comida = estado