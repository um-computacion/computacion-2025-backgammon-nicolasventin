"""
Módulo que define la clase Jugador.
"""
class Jugador:
    """
    Clase que representa a un jugador de Backgammon.
    """
    def __init__(self, nombre, ficha):
        """Inicializa al jugador con nombre y color de ficha."""
        self.__nombre__ = nombre
        self.__ficha__ = ficha

    @property
    def nombre(self) -> str:
        """Retorna el nombre del jugador."""
        return self.__nombre__

    @property
    def ficha(self) -> str:
        """Retorna el color de la ficha ('W' o 'B')."""
        return self.__ficha__

    def obtener_info(self):
        """Retorna la información del jugador (Nombre (Ficha))."""
        return f"{self.__nombre__} ({self.__ficha__})"
    
    def is_white(self) -> bool:
        """
        Verifica si el jugador usa las fichas 'W' (Blancas).
        """
        return self.__ficha__ == "W"
