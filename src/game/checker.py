"""
Módulo que define la clase Checker (ficha).
"""


class Checker:
    """Representa una ficha individual de Backgammon."""

    def __init__(self, color: str) -> None:
        """
        Recibe:
            color (str): El color de la ficha ('W' o 'B').
        Hace:
            Inicializa la ficha con su color y su estado 'comida' en Falso.
        Devuelve:
            Nada.
        """
        self.__color__: str = color
        self.__esta_comida: bool = False

    @property
    def color(self) -> str:
        """
        Recibe:
            Nada.
        Hace:
            Consulta el color de la ficha.
        Devuelve:
            (str): El color de la ficha ('W' o 'B').
        """
        return self.__color__

    @property
    def comida(self) -> bool:
        """
        Recibe:
            Nada.
        Hace:
            Consulta el estado 'comida' de la ficha.
        Devuelve:
            (bool): True si la ficha está en la barra, False en caso contrario.
        """
        return self.__esta_comida

    @comida.setter
    def comida(self, estado: bool) -> None:
        """
        Recibe:
            estado (bool): El nuevo estado 'comida' (True o False).
        Hace:
            Actualiza el estado 'comida' de la ficha.
        Devuelve:
            Nada.
        """
        self.__esta_comida = estado
