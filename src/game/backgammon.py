"""Núcleo del juego de Backgammon."""

from __future__ import annotations

from typing import List, Optional

from src.game.dado import Dice
from src.game.jugador import Jugador
from src.game.tablero import Tablero


class BackgammonGame:
    """Coordina jugadores, tablero y dados."""

    def __init__(
        self,
        name_p1: str = "Jugador 1",
        name_p2: str = "Jugador 2",
        board: Optional[Tablero] = None,
        dice: Optional[Dice] = None,
    ) -> None:
        """Inicializa la partida base."""
        self.__board__ = board or Tablero()
        self.__dice__ = dice or Dice()
        self.__players__: List[Jugador] = [
            Jugador(name_p1, "B"),
            Jugador(name_p2, "N"),
        ]
        self.__turno__ = 0

    def tablero(self) -> Tablero:
        """Entrega el tablero actual."""
        return self.__board__

    def jugadores(self) -> List[Jugador]:
        """Devuelve la lista de jugadores."""
        return list(self.__players__)

    def dados(self) -> Dice:
        """Devuelve los dados de la partida."""
        return self.__dice__

