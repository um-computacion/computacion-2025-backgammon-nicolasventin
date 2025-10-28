# Prompts testing

# Prompt 1

Modelo de IA:  chatgpt 5.0

Quiero saber porque me esta fallando estos tests de mi tablero. 29/08/2025

➜ computacion-2025-backgammon-nicolasventin git:(14-logica-de-empate-en-board) ✗ python3 -m unittest tests/test_tablero.py ...[[' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], ['W', 'W', 'W', 'W', '4'], ['W', 'W', 'W', ' ', ' ']] board 0, 11: W F... ====================================================================== FAIL: test_draw (tests.test_tablero.TestTablero) ---------------------------------------------------------------------- Traceback (most recent call last): File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/tests/test_tablero.py", line 47, in test_draw self.assertEqual( AssertionError: Lists differ: [[' '[15 chars], ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', [253 chars]' ']] != [[' '[15 chars], ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W'], [' [549 chars]' ']] First differing element 0: [' ', ' ', ' ', ' ', ' '] [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W'] First list contains 2 additional elements. First extra element 10: ['W', 'W', 'W', 'W', '4'] Diff is 1010 characters long. Set self.maxDiff to None to see it. ---------------------------------------------------------------------- Ran 7 tests in 0.001s FAILED (failures=1)

Respuesta:

¡Lo tengo! El test falla porque tu draw() está devolviendo la matriz transpuesta: estás creando 12 filas × 5 columnas (una fila por punto y 5 “alturas”), pero el test espera 10 filas × 12 columnas (10 alturas —5 arriba + 5 abajo— por 12 puntos).

Acá va tu draw() con el mínimo cambio posible: agrego 6 líneas al final.

    height, width = 10, 12
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for r in range(5):          # solo la mitad superior
        for c in range(12):
            grid[r][c] = result_board[c][r]  # transponer 12x5 -> 5x12 (arriba)

    return grid

La salida fue utilizada por completo

En el archivo 
src/tests/test_tablero.py

# Prompt 2

Modelo de IA:  gemini pro 2.5 flash

Prompt Utilizado:

Necesito refactorizar los test de tablero, test de backgammon y crear los test de checker para que empiece a usar la clase checker en su logica del juego

Respuesta:

Has dado un paso importante al introducir la clase Checker. Ahora que el core (Tablero y BackgammonGame) se está reestructurando para usar listas de objetos Checker en lugar de enteros, debemos adaptar todos los tests.

Aquí tienes el código necesario para crear las pruebas de Checker y refactorizar test_tablero.py y test_backgammon.py.

1. 🧪 tests/test_checker.py (Nuevo Archivo)
Python

import unittest
from src.game.checker import Checker

class TestChecker(unittest.TestCase):
    def test_creacion_blanca(self):
        checker = Checker('B')
        self.assertEqual(checker.get_color(), 'B')
        self.assertFalse(checker.comida)

    def test_creacion_negra(self):
        checker = Checker('N')
        self.assertEqual(checker.get_color(), 'N')
        self.assertFalse(checker.comida)
        
    def test_propiedad_comida_setter(self):
        checker = Checker('B')
        
        checker.comida = True
        self.assertTrue(checker.comida)
        
        checker.comida = False
        self.assertFalse(checker.comida)
2. 🧪 tests/test_tablero.py (Refactorizado)
Python

import unittest
from src.game.tablero import Tablero
from src.game.checker import Checker

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()

    def test__turnos__(self):
        self.assertEqual(self.tablero.__turnos__, 0)

    def test__cantidad_de_posiciones__(self):
        self.assertEqual(len(self.tablero.__puntos__), 24)

    def test_posiciones_iniciales(self):
        self.assertEqual(len(self.tablero.__puntos__[0]), 2)
        self.assertEqual(self.tablero.__puntos__[0][0].get_color(), 'B')
        self.assertEqual(len(self.tablero.__puntos__[11]), 5)
        self.assertEqual(self.tablero.__puntos__[11][0].get_color(), 'B')
        self.assertEqual(len(self.tablero.__puntos__[16]), 3)
        self.assertEqual(self.tablero.__puntos__[16][0].get_color(), 'B')
        self.assertEqual(len(self.tablero.__puntos__[18]), 5)
        self.assertEqual(self.tablero.__puntos__[18][0].get_color(), 'B')

        self.assertEqual(len(self.tablero.__puntos__[23]), 2)
        self.assertEqual(self.tablero.__puntos__[23][0].get_color(), 'N')
        self.assertEqual(len(self.tablero.__puntos__[12]), 5)
        self.assertEqual(self.tablero.__puntos__[12][0].get_color(), 'N')
        self.assertEqual(len(self.tablero.__puntos__[7]), 3)
        self.assertEqual(self.tablero.__puntos__[7][0].get_color(), 'N')
        self.assertEqual(len(self.tablero.__puntos__[5]), 5)
        self.assertEqual(self.tablero.__puntos__[5][0].get_color(), 'N')

        self.assertEqual(len(self.tablero.__bar_blancas__), 0)
        self.assertEqual(len(self.tablero.__bar_negras__), 0)

    def test_owner_and_count_from_puntos(self):
        owner, count = self.tablero._owner_and_count_from_puntos(0)
        self.assertEqual(owner, 'white')
        self.assertEqual(count, 2)
        
        owner, count = self.tablero._owner_and_count_from_puntos(23)
        self.assertEqual(owner, 'black')
        self.assertEqual(count, 2)
        
        self.assertEqual(self.tablero._owner_and_count_from_puntos(1), (None, 0))

    def test_piece(self):
        self.assertEqual(self.tablero._piece('white'), "W")
        self.assertEqual(self.tablero._piece('black'), "B")

    def test_draw(self):
        board = Tablero()
        board_draw = board.draw()
        
        self.assertEqual(board_draw[0][11], 'W')
        self.assertEqual(board_draw[1][11], 'W') 
        
        for _ in range(3):
            board.__puntos__[11].append(Checker('B'))
            
        board_draw_over_5 = board.draw()
        self.assertEqual(board_draw_over_5[0][0], 'W')
        self.assertEqual(board_draw_over_5[3][0], 'W')
        self.assertEqual(board_draw_over_5[4][0], '4') 
    
    def test_hit_opponent(self):
        self.tablero.__puntos__[10] = [Checker('N')]
        self.tablero.hit_opponent(10)
        
        self.assertEqual(len(self.tablero.__puntos__[10]), 0)
        self.assertEqual(len(self.tablero.__bar_negras__), 1)
        self.assertTrue(self.tablero.__bar_negras__[0].comida)
        
        self.tablero.__puntos__[15] = [Checker('B')]
        self.tablero.hit_opponent(15)
        
        self.assertEqual(len(self.tablero.__puntos__[15]), 0)
        self.assertEqual(len(self.tablero.__bar_blancas__), 1)
        self.assertTrue(self.tablero.__bar_blancas__[0].comida)
        
        self.tablero.__puntos__[5] = [Checker('N'), Checker('N')]
        self.assertFalse(self.tablero.hit_opponent(5))

    def test_mover_ficha_blanca(self):
        start_point, end_point = 0, 1
        
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].get_color(), 'B')

    def test_mover_ficha_negra(self):
        start_point, end_point = 23, 22
        self.tablero.mover_ficha(start_point, end_point)
        self.assertEqual(len(self.tablero.__puntos__[start_point]), 1)
        self.assertEqual(len(self.tablero.__puntos__[end_point]), 1)
        self.assertEqual(self.tablero.__puntos__[end_point][0].get_color(), 'N')

    def test_mover_ficha_errores(self):
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha(24, 23)
        with self.assertRaises(Exception):
            self.tablero.mover_ficha(2, 3)


3. 🧪 tests/test_backgammon.py (Refactorizado)
Python

import unittest
from src.game.backgammon import BackgammonGame
from src.game.checker import Checker

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.game = BackgammonGame()
        self.game.__dados_restantes__ = [3, 5]

    def _setup_checkers(self, point, color, count):
        self.game.__board__.__puntos__[point] = [Checker(color) for _ in range(count)]
    
    def test_turno_inicial(self):
        self.assertEqual(self.game.__turno__, 0)

    def test_jugadores_iniciales(self):
        jugadores = self.game.__players__
        self.assertEqual(len(jugadores), 2)
        self.assertEqual(jugadores[0].__ficha__, "B")
        self.assertEqual(jugadores[1].__ficha__, "N")

    def test_validar_movimiento_bloqueado(self):
        
        self._setup_checkers(18, 'N', 2) 
        self._setup_checkers(21, 'B', 1) 
        self.game.__dados_restantes__ = [3] 

        self.assertFalse(self.game.validar_movimiento(21, 18))

        self.game.__turno__ = 1 
        self._setup_checkers(6, 'B', 3) 
        self._setup_checkers(3, 'N', 1) 
        self.game.__dados_restantes__ = [3] 

        self.assertFalse(self.game.validar_movimiento(3, 6))


    def test_validar_movimiento_hit_valido(self):
        
        self._setup_checkers(15, 'N', 1) 
        self._setup_checkers(18, 'B', 1) 
        self.game.__dados_restantes__ = [3] 

        self.assertTrue(self.game.validar_movimiento(18, 15))

        self.game.__turno__ = 1 
        self._setup_checkers(9, 'B', 1) 
        self._setup_checkers(6, 'N', 1) 
        self.game.__dados_restantes__ = [3]

        self.assertTrue(self.game.validar_movimiento(6, 9))


    def test_validar_movimiento_basico_fallos(self):
        
        self.game.__dados_restantes__ = [5]
        
        self.game.__board__.__puntos__[1] = []
        self.assertFalse(self.game.validar_movimiento(1, 6))
                         
        self._setup_checkers(23, 'B', 1) 
        self.assertFalse(self.game.validar_movimiento(23, 24))

        self._setup_checkers(5, 'B', 1) 
        self.assertFalse(self.game.validar_movimiento(5, 1))


Cambios realizados:

Utilice la totalidad de la respuesta anterior 

en los archivos 
src/tests/test_tablero.py
src/tests/test_backgammon.py

creacion de tests/test_checker.py

# Prompt 3

Modelo de IA:  Gemini Pro 2.5 Flash

Prompt Utilizado:

Necesito hacer los test para _is_home_board_ready y para get_piece_count de una forma sencilla y legible sin anotaciones extras

Respuesta:


Aquí tienes los tests unitarios para _is_home_board_ready y get_piece_count, diseñados para ser sencillos y sin anotaciones extra.Esa función auxiliar (_setup_checkers) es un método de ayuda (helper) diseñado exclusivamente para simplificar la creación de escenarios complejos dentro de tus pruebas unitarias.

    #Nota: El helper _setup_checkers se debe definir en tests/test_backgammon.py y replicarse aquí si es necesario, o usar la importación de Checker para la inicialización manual.

    def _setup_checkers(self, point, color, count):
        """Helper para configurar un punto con objetos Checker."""
        from src.game.checker import Checker
        self.tablero.__puntos__[point] = [Checker(color) for _ in range(count)]

    def test_get_piece_count(self):
        """Verifica que el conteo total de fichas en el tablero y barra sea correcto (debe ser 15)."""
        # Estado Inicial
        self.assertEqual(self.tablero.get_piece_count('B'), 15)
        self.assertEqual(self.tablero.get_piece_count('N'), 15)
        
        # Quitar una ficha blanca del punto 0 (simula Bear Off)
        self.tablero.__puntos__[0].pop()
        self.assertEqual(self.tablero.get_piece_count('B'), 14)
        
        # Simular una ficha negra golpeada (el conteo total debe seguir siendo 15)
        self.tablero.hit_opponent(23)
        self.assertEqual(self.tablero.get_piece_count('N'), 15)
        self.assertEqual(len(self.tablero.__bar_negras__), 1)


    def test_is_home_board_ready(self):
        """Verifica la precondición de Bearing Off: todas las fichas en Home Board."""
        
        # 1. ESTADO INICIAL (Falla, fichas en puntos exteriores)
        self.assertFalse(self.tablero._is_home_board_ready('B'))
        self.assertFalse(self.tablero._is_home_board_ready('N'))

        # 2. FALLA por Ficha en la Barra
        self.tablero.__bar_blancas__.append(self.tablero.__puntos__[0].pop())
        self.assertFalse(self.tablero._is_home_board_ready('B'))
        self.tablero.__bar_blancas__ = [] # Limpieza

        # 3. FALLA por Ficha Fuera de Casa (White: punto 17)
        self.tablero.__puntos__[18].pop()
        self._setup_checkers(17, 'B', 1)
        self.assertFalse(self.tablero._is_home_board_ready('B'))
        
        # 4. FALLA por Ficha Fuera de Casa (Black: punto 6)
        self.tablero.__puntos__[5].pop()
        self._setup_checkers(6, 'N', 1)
        self.assertFalse(self.tablero._is_home_board_ready('N'))

        # 5. ESTADO LISTO (Pasa, simulando que todas las fichas están en el Home Board 18-23)
        self.setUp() 
        for i in range(0, 18):
            self.tablero.__puntos__[i] = []
        # Si las fichas restantes están en 18-23, debe pasar.
        self.assertTrue(self.tablero._is_home_board_ready('B'))

        # 6. ESTADO LISTO (Pasa, simulando que todas las fichas están en el Home Board 0-5)
        self.setUp()
        for i in range(6, 24):
            self.tablero.__puntos__[i] = []
        # Si las fichas restantes están en 0-5, debe pasar.
        self.assertTrue(self.tablero._is_home_board_ready('N'))

Cambios realizados:

Utilice el setup_checkers() y el test_is_home_board_ready() , para hacere el test_get_piece_count() me guie nomas pero le hice un par de modificaciones debido a que fallaban los tests.

Archivos utilizados:

src/tests/test_tablero.py
src/tests/test_backgammon.py

# Prompt 4

Modelo de IA:  gemini pro 2.5 flash

Prompt Utilizado:

(venv) ➜  computacion-2025-backgammon-nicolasventin git:(45-logica-bearing-off) ✗ python3 -m unittest tests/test_backgammon.py

.E...F.F...

======================================================================

ERROR: test_ejecutar_movimiento_bear_off (tests.test_backgammon.TestBackgammonGame)

Verifica que ejecutar_movimiento quite la ficha al hacer Bear Off.

----------------------------------------------------------------------

Traceback (most recent call last):

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/tests/test_backgammon.py", line 119, in test_ejecutar_movimiento_bear_off

    self.game.ejecutar_movimiento(2, -1)

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/src/game/backgammon.py", line 161, in ejecutar_movimiento

    raise ValueError("Movimiento inválido según las reglas del Backgammon.")

ValueError: Movimiento inválido según las reglas del Backgammon.



======================================================================

FAIL: test_validar_movimiento_bear_off_dado_mayor_farthest (tests.test_backgammon.TestBackgammonGame)

Verifica que se permita salir con dado mayor si es la ficha más lejana.

----------------------------------------------------------------------

Traceback (most recent call last):

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/tests/test_backgammon.py", line 88, in test_validar_movimiento_bear_off_dado_mayor_farthest

    self.assertTrue(self.game.validar_movimiento(2, -1))

AssertionError: False is not true



======================================================================

FAIL: test_validar_movimiento_bear_off_exacto (tests.test_backgammon.TestBackgammonGame)

Verifica que se permita salir con dado exacto si está en Home Board.

----------------------------------------------------------------------

Traceback (most recent call last):

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/tests/test_backgammon.py", line 73, in test_validar_movimiento_bear_off_exacto

    self.assertTrue(self.game.validar_movimiento(2, -1))

AssertionError: False is not true



----------------------------------------------------------------------

Ran 11 tests in 0.001s



FAILED (failures=2, errors=1)

(venv) ➜  computacion-2025-backgammon-nicolasventin git:(45-logica-bearing-off) ✗ python3 -m unittest tests/test_backgammon.py

.E...F.F...

======================================================================

ERROR: test_ejecutar_movimiento_bear_off (tests.test_backgammon.TestBackgammonGame)

Verifica que ejecutar_movimiento quite la ficha al hacer Bear Off.

----------------------------------------------------------------------

Traceback (most recent call last):

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/tests/test_backgammon.py", line 127, in test_ejecutar_movimiento_bear_off

    self.game.ejecutar_movimiento(2, -1)

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/src/game/backgammon.py", line 161, in ejecutar_movimiento

    raise ValueError("Movimiento inválido según las reglas del Backgammon.")

ValueError: Movimiento inválido según las reglas del Backgammon.



======================================================================

FAIL: test_validar_movimiento_bear_off_dado_mayor_lejana (tests.test_backgammon.TestBackgammonGame)

Verifica que se permita salir con dado mayor si es la ficha más lejana.

----------------------------------------------------------------------

Traceback (most recent call last):

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/tests/test_backgammon.py", line 94, in test_validar_movimiento_bear_off_dado_mayor_lejana

    self.assertTrue(self.game.validar_movimiento(2, -1))

AssertionError: False is not true



======================================================================

FAIL: test_validar_movimiento_bear_off_exacto (tests.test_backgammon.TestBackgammonGame)

Verifica que se permita salir con dado exacto si está en Home Board.

----------------------------------------------------------------------

Traceback (most recent call last):

  File "/home/nico/Documents/computacion-2025-backgammon-nicolasventin/tests/test_backgammon.py", line 75, in test_validar_movimiento_bear_off_exacto

    self.assertTrue(self.game.validar_movimiento(2, -1))

AssertionError: False is not true



----------------------------------------------------------------------

Ran 11 tests in 0.001s



FAILED (failures=2, errors=1)

No se realmente porque pueden estar fallando estos tests, podes verificar que esta mal?

Respuesta:

Este es un problema frustrante, porque tus tests demuestran que partes de tu lógica son correctas, pero siguen fallando.

El test que pasa (test_validar_movimiento_bear_off_falla_si_no_home_board) demuestra que tu función self.__board__._is_home_board_ready(player_color) funciona correctamente. Detecta fichas fuera del home board y devuelve False como debe ser.

Los tests que fallan (...exacto y ...dado_mayor_farthest) fallan porque _is_home_board_ready también está devolviendo False, a pesar de que tú crees que has limpiado el tablero.

La única conclusión lógica es que el tablero no se está limpiando correctamente en la configuración de tus tests.

El hecho de que _is_home_board_ready (que vive en Tablero) siga devolviendo False significa que debe estar leyendo el estado de otro lugar.

Verifica que _is_home_board_ready está leyendo el estado de la barra y el tablero debería resolver el problema.

Cambios realizados:

Fui a buscar el problema en tabler y efectivamente el problema estaba en el método _is_home_board_ready que me equivoque y estaba puesto al revez. 

En el archivo 
src/game/tablero.py
src/game/backgammon.py
tests/test_backgammon.py
tests/test_tablero.py
