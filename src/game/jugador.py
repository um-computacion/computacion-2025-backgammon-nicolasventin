"""
Módulo que define la clase Jugador.
"""


class Jugador:
    """
    Clase que representa a un jugador de Backgammon.
    """

    def __init__(self, nombre, ficha):
        """
        Recibe:
            nombre (str): El nombre del jugador.
            ficha (str): El color de ficha que usa ('W' o 'B').
        Hace:
            Inicializa al jugador con su nombre y color de ficha.
        Devuelve:
            Nada.
        """
        self.__nombre__ = nombre
        self.__ficha__ = ficha

    @property
    def nombre(self) -> str:
        """
        Recibe:
            Nada.
        Hace:
            Consulta el nombre del jugador.
        Devuelve:
            (str): El nombre del jugador.
        """
        return self.__nombre__

    @property
    def ficha(self) -> str:
        """
        Recibe:
            Nada.
        Hace:
            Consulta el color de ficha del jugador.
        Devuelve:
            (str): El color de la ficha ('W' o 'B').
        """
        return self.__ficha__

    def obtener_info(self):
        """
        Recibe:
            Nada.
        Hace:
            Formatea un string con el nombre y la ficha del jugador.
        Devuelve:
            (str): La información formateada (ej: "Jugador 1 (W)").
        """
        return f"{self.__nombre__} ({self.__ficha__})"

    def is_white(self) -> bool:
        """
        Recibe:
            Nada.
        Hace:
            Verifica si el color de la ficha del jugador es 'W'.
        Devuelve:
            (bool): True si el jugador es 'W' (Blancas), False en caso contrario.
        """
        return self.__ficha__ == "W"
