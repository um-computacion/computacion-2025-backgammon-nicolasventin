# Backgammon (Computación 2025)

### Nombre y apellido: Nicolas Ventin

Este repositorio contiene una implementación del juego Backgammon en Python, con soporte tanto para una interfaz de línea de comandos (CLI) como para una interfaz gráfica de usuario (GUI) usando Pygame.

## Requisitos y Configuración del Entorno

El proyecto utiliza **Python 3.10**.

Se recomienda encarecidamente utilizar un entorno virtual (`venv`) para gestionar las dependencias del proyecto.

1.  **Crear el entorno virtual:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activar el entorno virtual:**

      * En macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
      * En Windows (PowerShell/Cmd):
        ```bash
        .\venv\Scripts\activate
        ```

3.  **Instalar dependencias:**

      * **Para jugar (GUI):** La interfaz gráfica requiere `pygame`.
        ```bash
        pip install pygame
        ```
      * **Para desarrollo (Testing/Linting):** Para ejecutar las pruebas unitarias y el análisis de código, instala las dependencias de desarrollo desde `requirements.txt`.
        ```bash
        pip install -r requirements.txt
        ```

*Nota: La versión CLI no requiere ninguna biblioteca externa más allá de las estándar de Python.*

-----

## Cómo Ejecutar el Juego

*Asegúrate de tener el entorno virtual activado si instalaste las dependencias allí.*

### 1\. Interfaz Gráfica (Pygame)

Para iniciar la versión con interfaz gráfica, ejecuta el archivo `pygame_ui.py`:

```bash
python3 -m src.ui.pygame_ui
```

### 2\. Interfaz de Línea de Comandos (CLI)

Para iniciar la versión de consola, ejecuta el archivo `cli.py`:

```bash
python3 -m src.ui.cli
```

-----

## Cómo Jugar

### 1\. Instrucciones (Pygame)

La interfaz gráfica se maneja completamente con el ratón.

1.  **Menú Principal:** Serás recibido por el menú principal.
      * Haz clic en **"Jugar"** para ir a la configuración de la partida.
      * Haz clic en **"Instrucciones"** para leer las reglas.
      * Haz clic en **"Salir"** para cerrar el juego.
2.  **Selección de Jugador:**
      * Haz clic en las cajas de texto para escribir los nombres de "Jugador 1 (W)" y "Jugador 2 (B)".
      * Haz clic en el botón correspondiente para decidir quién empieza.
3.  **En el Tablero:**
      * **Tirar Dados:** Haz clic en el botón **"Tirar Dados"** al inicio de tu turno.
      * **Mover Fichas:**
        1.  Haz clic en una de tus fichas (en un punto o en la barra). La ficha se resaltará.
        2.  Los destinos válidos (puntos o la bandeja de "bear off") se iluminarán de color verde.
        3.  Haz clic en uno de los destinos iluminados para completar el movimiento.
      * **Pasar Turno:** Si no tienes movimientos válidos, aparecerá el botón **"Pasar Turno"**.

### 2\. Instrucciones (CLI)

La interfaz de consola se maneja con comandos de texto.

1.  **Inicio del Turno:** El juego te mostrará el tablero y te pedirá que tires los dados (esto es automático al inicio del turno en la CLI).
2.  **Ingresar Movimientos:** El juego te pedirá que ingreses tu movimiento. Los formatos válidos son:
      * **Movimiento normal:** `[punto_inicio] [punto_fin]` (Ej: `23 18`)
      * **Mover desde la barra:** `BAR [punto_fin]` (Ej: `BAR 20`)
      * **Sacar ficha (Bear Off):** `[punto_inicio] OFF` (Ej: `3 OFF`)
3.  **Pasar el Turno:** Si no tienes más movimientos o no puedes mover, escribe `PASAR` para ceder el turno al oponente.
4.  **Fin del Juego:** El juego se detendrá automáticamente cuando un jugador haya sacado todas sus fichas.