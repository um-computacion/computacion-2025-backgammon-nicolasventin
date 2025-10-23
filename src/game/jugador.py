"""Definición de la entidad Jugador."""


class Jugador:
    """Representa a un jugador con su ficha."""

    def __init__(self, nombre: str, ficha: str) -> None:
        """Guarda el nombre y la ficha."""
        self.__nombre__ = nombre
        self.__ficha__ = ficha

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del jugador."""
        return self.__nombre__

    @property
    def ficha(self) -> str:
        """Devuelve la ficha asignada."""
        return self.__ficha__

    def obtener_info(self) -> str:
        """Genera descripción breve."""
        return f"{self.__nombre__} ({self.__ficha__})"