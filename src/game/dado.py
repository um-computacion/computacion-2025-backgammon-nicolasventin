"""Módulo para gestionar los dados."""

from __future__ import annotations

import random
from typing import Callable, Tuple


class Dice:
    """Simula un par de dados."""

    def __init__(self, rand_func: Callable[[int, int], int] | None = None) -> None:
        """Configura el generador aleatorio."""
        self.__rand_func__ = rand_func or random.randint
        self.__values__: Tuple[int, ...] = tuple()

    def roll(self) -> Tuple[int, ...]:
        """Lanza los dados y guarda el resultado."""
        try:
            first = self.__rand_func__(1, 6)
            second = self.__rand_func__(1, 6)
        except Exception:
            self.__values__ = tuple()
            return self.__values__

        if first == second:
            self.__values__ = (first, second, first, second)
        else:
            self.__values__ = (first, second)
        return self.__values__

    def values(self) -> Tuple[int, ...]:
        """Devuelve el último lanzamiento."""
        return self.__values__


def get_dice() -> Tuple[int, ...]:
    """Función auxiliar para lanzar dados."""
    dice = Dice()
    return dice.roll()

