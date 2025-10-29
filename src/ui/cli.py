from src.game.tablero import Tablero


class CLIRenderer:
    """Lógica de visualización específica para la Interfaz de Línea de Comandos (CLI)."""

    def _format_ficha(self, v: int) -> str:
        """Formatea la ficha (cantidad + color) para impresión en consola."""
        if v > 0:
            return f"{v}B"
        elif v < 0:
            return f"{abs(v)}N"
        else:
            return "--"

    def mostrar_estado_puntos(self, tablero: Tablero):
        """Muestra el estado de los puntos del tablero en consola."""
        puntos = tablero.__puntos__

        # Arriba: 11..0
        arriba_idx = list(range(11, -1, -1))
        # Abajo: 12..23
        abajo_idx = list(range(12, 24))

        print("\n=== Estado de Puntos ===")
        # Puntos arriba
        print(" ".join(f"{i:02}" for i in arriba_idx))
        print(" ".join(self._format_ficha(puntos[i]) for i in arriba_idx))
        # Separador
        print("-" * 60)
        # Puntos abajo
        print(" ".join(self._format_ficha(puntos[i]) for i in abajo_idx))
        print(" ".join(f"{i:02}" for i in abajo_idx))
        print("========================\n")

    def mostrar_tablero(self, tablero: Tablero):
        """Imprime la representación gráfica 10x12 del tablero en consola."""
        grid = tablero.draw()

        print("\n=== Tablero Gráfico ===")
        # Imprimir la grilla fila por fila
        for row in grid:
            print(" | ".join(row))

        print("=======================\n")
