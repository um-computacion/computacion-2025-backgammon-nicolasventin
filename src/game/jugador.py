class Jugador:
    """Clase que representa a un jugador de Backgammon."""
    def __init__(self, nombre, ficha):
        """Inicializa al jugador con nombre y color de ficha."""
        self.__nombre__ = nombre
        self.__ficha__ = ficha

    def obtener_info(self):
        """Retorna la información del jugador (Nombre (Ficha))."""
        return f"{self.__nombre__} ({self.__ficha__})"