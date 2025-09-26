# Prompts

Que estructura de carpetas me recomendas para este proyecto ? 27/08/2025

backgammon/
│── src/
│   ├── __init__.py
│   ├── game/
│   │   ├── __init__.py
│   │   ├── tablero.py        # Clase Tablero (posiciones, fichas)
│   │   ├── jugador.py        # Clase Jugador
│   │   ├── dado.py           # Lógica de dados
│   │   └── backgammon.py     # Lógica principal: movimientos, reglas, partida
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── cli.py            # Interfaz de consola
│   │   ├── gui.py            # Interfaz gráfica
│   │   └── assets/           # Imágenes, fuentes, sprites
│
│── tests/
│   ├── test_tablero.py
│   ├── test_jugador.py
│   ├── test_dado.py
│   └── test_backgammon.py    # Tests para movimientos, reglas y partida


Necesito que el tabler se muestre de una forma que sea fácil de entender y a la vez que se pueda ver facilmente en consola. 15/08/2025

    def _format_ficha(self, v: int) -> str:
        if v > 0:
            return f"{v}B"
        elif v < 0:
            return f"{abs(v)}N"
        else:
            return "--"
        
    def mostrar(self):
        # Arriba: 11..0
        arriba_idx = list(range(11, -1, -1))
        # Abajo: 12..23
        abajo_idx  = list(range(12, 24))

        print("\n=== Tablero de Backgammon ===")
        # Fichas arriba
        print(" ".join(f"{i:02}" for i in arriba_idx))        
        print(" ".join(self._format_ficha(self.__puntos__[i]) for i in arriba_idx))
        # Separador
        print("-" * 60)
        # Fichas abajo
        print(" ".join(self._format_ficha(self.__puntos__[i]) for i in abajo_idx))
        print(" ".join(f"{i:02}" for i in abajo_idx))

        print("=============================\n")