# Prompts

MODELO: CHAT GPT 5.0

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
│   └── test_backgammon.py    # Tests para movimientos, reglas y 


Use el modelo que me mando y le agrego checkers.py.