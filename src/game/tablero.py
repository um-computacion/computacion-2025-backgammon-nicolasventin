from __future__ import annotations

from typing import Iterator, List, Optional, Sequence, Tuple


class PieceFormatter:
    """Convierte piezas a formatos simples."""

    def format_point(self, value: int) -> str:
        """Devuelve etiqueta breve para un punto."""
        if value > 0:
            return f"{value}B"
        if value < 0:
            return f"{abs(value)}N"
        return "--"

    def owner_and_count(self, value: int) -> Tuple[Optional[str], int]:
        """Calcula dueño y cantidad."""
        if value > 0:
            return ("white", value)
        if value < 0:
            return ("black", -value)
        return (None, 0)


class BoardPositions:
    """Envuelve la colección de puntos."""

    def __init__(self, puntos: List[int], formatter: PieceFormatter):
        """Guarda referencia a puntos y formato."""
        self.__puntos__ = puntos
        self.__formatter__ = formatter
        self.__overrides__: List[Optional[Tuple[Optional[str], int]]] = [None] * len(puntos)
        self.__manual_mode__ = False

    def __len__(self) -> int:
        """Retorna tamaño del tablero."""
        return len(self.__puntos__)

    def __getitem__(self, index: int) -> Tuple[Optional[str], int]:
        """Obtiene dueño y fichas."""
        if self.__manual_mode__:
            override = self.__overrides__[index]
            return override if override is not None else (None, 0)
        value = self.__puntos__[index]
        return self.__formatter__.owner_and_count(value)

    def __setitem__(self, index: int, value: Tuple[Optional[str], int]) -> None:
        """Actualiza el valor del punto."""
        if not self.__manual_mode__:
            self.__manual_mode__ = True
            for position in range(len(self.__puntos__)):
                self.__puntos__[position] = 0
            self.__overrides__ = [(None, 0) for _ in range(len(self.__overrides__))]

        owner, count = value
        self.__overrides__[index] = (owner, count)
        if owner == "white":
            self.__puntos__[index] = count
        elif owner == "black":
            self.__puntos__[index] = -count
        else:
            self.__puntos__[index] = 0

    def __iter__(self) -> Iterator[Tuple[Optional[str], int]]:
        """Itera sobre dueños y fichas."""
        for index in range(len(self)):
            yield self[index]

    @property
    def manual_mode(self) -> bool:
        """Indica si existe modo manual."""
        return self.__manual_mode__


class BoardGridBuilder:
    """Construye la grilla de visualización."""

    def build(self, positions: Sequence[Tuple[Optional[str], int]]) -> List[List[str]]:
        """Genera la grilla 10x12."""
        height, width = 10, 12
        grid = [[" " for _ in range(width)] for _ in range(height)]
        manual_mode = getattr(positions, "manual_mode", False)

        for column in range(12):
            point = 11 - column
            owner, count = positions[point]
            if not owner or count == 0:
                continue
            piece = self._piece(owner)
            if count <= 5:
                for row in range(count):
                    grid[row][column] = piece
            else:
                for row in range(4):
                    grid[row][column] = piece
                grid[4][column] = str(count - 4)

        for column in range(12):
            point = 12 + column
            owner, count = positions[point]
            if not owner or count == 0 or (manual_mode and owner == "black"):
                continue
            piece = self._piece(owner)
            if count <= 5:
                for offset in range(count):
                    grid[9 - offset][column] = piece
            else:
                for offset in range(4):
                    grid[9 - offset][column] = piece
                grid[5][column] = str(count - 4)

        return grid

    def _piece(self, owner: str) -> str:
        """Convierte dueño a símbolo."""
        return "W" if owner == "white" else "B"


class Tablero:
    """Gestiona el estado del tablero."""

    def __init__(
        self,
        formatter: Optional[PieceFormatter] = None,
        grid_builder: Optional[BoardGridBuilder] = None,
    ) -> None:
        """Inicializa el tablero por defecto."""
        self.__turnos__ = 0
        self.__puntos__ = [0] * 24

        self.__puntos__[0] = 2
        self.__puntos__[11] = 5
        self.__puntos__[16] = 3
        self.__puntos__[18] = 5

        self.__puntos__[23] = -2
        self.__puntos__[12] = -5
        self.__puntos__[7] = -3
        self.__puntos__[5] = -5

        self.__formatter__ = formatter or PieceFormatter()
        self.__grid_builder__ = grid_builder or BoardGridBuilder()
        self.__positions__ = BoardPositions(self.__puntos__, self.__formatter__)

    @property
    def pos(self) -> BoardPositions:
        """Entrega acceso a las posiciones."""
        return self.__positions__

    def _format_ficha(self, value: int) -> str:
        """Da formato a un punto."""
        return self.__formatter__.format_point(value)

    def mostrar(self) -> None:
        """Imprime el tablero textual."""
        arriba_idx = list(range(11, -1, -1))
        abajo_idx = list(range(12, 24))

        print("\n=== Tablero de Backgammon ===")
        print(" ".join(f"{i:02}" for i in arriba_idx))
        print(" ".join(self._format_ficha(self.__puntos__[i]) for i in arriba_idx))
        print("-" * 60)
        print(" ".join(self._format_ficha(self.__puntos__[i]) for i in abajo_idx))
        print(" ".join(f"{i:02}" for i in abajo_idx))
        print("=============================\n")

    def draw(self) -> List[List[str]]:
        """Construye una grilla visual."""
        return self.__grid_builder__.build(self.__positions__)

    def _owner_and_count_from_puntos(self, index: int) -> Tuple[Optional[str], int]:
        """Obtiene dueño y fichas desde __puntos__."""
        return self.__positions__[index]

