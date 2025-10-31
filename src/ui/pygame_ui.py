import pygame
import sys
from typing import Optional, Tuple

import pygame.gfxdraw

from ..game.backgammon import BackgammonGame
from ..game.jugador import Jugador

# --- Constantes de Configuración de Pygame ---

# Pantalla
SCREEN_WIDTH = 800
BOARD_HEIGHT = 600
UI_AREA_HEIGHT = 180
SCREEN_HEIGHT = BOARD_HEIGHT + UI_AREA_HEIGHT
BOARD_FRAME_WIDTH = 10

# --- Constantes de Juego ---
TOTAL_PIECES_PER_PLAYER = 15

# --- Colores ---
BOARD_COLOR = (120, 80, 50)
BACKGROUND_COLOR = (244, 226, 198)
UI_COLOR = (200, 180, 160)
POINT_COLOR_A = (118, 54, 38)
POINT_COLOR_B = (210, 180, 140)
PIECE_WHITE = (255, 255, 255)
PIECE_BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0, 150)
TEXT_COLOR = (40, 40, 40)
BUTTON_COLOR = (0, 150, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
TEXT_COLOR_WHITE = (255, 255, 255)
BORDER_COLOR_BLACK = (0, 0, 0)

# --- Colores de Resaltado de Movimiento ---
MOVE_HIGHLIGHT_VALID = (0, 200, 0)
DICE_ROLL_HIGHLIGHT_COLOR = (0, 150, 0)
INPUT_BOX_COLOR = (255, 255, 255)
INPUT_BOX_ACTIVE_COLOR = (200, 255, 200)

# --- Colores NUEVOS ---
BUTTON_PASS_COLOR = (200, 100, 0)

# --- Geometría del Tablero ---
POINT_WIDTH = 50
POINT_HEIGHT = 200
BAR_WIDTH = 40
BEAR_OFF_TRAY_WIDTH = 45
TOTAL_BOARD_WIDTH = (POINT_WIDTH * 12) + BAR_WIDTH
MARGIN_X = (SCREEN_WIDTH - TOTAL_BOARD_WIDTH) / 2
MARGIN_Y = 40 + BOARD_FRAME_WIDTH

BEAR_OFF_TRAY_X = SCREEN_WIDTH - MARGIN_X + 10

PIECE_RADIUS = 20

# --- Constantes de UI (Panel de Juego) ---
UI_AREA_Y_START = BOARD_HEIGHT
DICE_BUTTON_X = 110
DICE_BUTTON_Y = UI_AREA_Y_START + 75
MSG_AREA_X = 250
MSG_AREA_Y = UI_AREA_Y_START + 45
PLAYER_AREA_X = 25
PLAYER_AREA_Y = UI_AREA_Y_START + 120


# --- Constantes de Dados Gráficos ---
DICE_SIZE = 40
DICE_PADDING = 10
DICE_COLOR = (255, 255, 255)
PIP_COLOR = (0, 0, 0)
PIP_RADIUS = 4


class PygameUI:
    """
    Maneja el bucle del juego, el renderizado y la entrada de Pygame.

    Recibe: Nada al inicializarse.
    Hace: Inicializa Pygame, configura la ventana, fuentes y el estado inicial del juego.
    Devuelve: Una instancia de PygameUI.
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.__screen__ = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon - Computación 2025")

        FONT_NAME = "Comic Sans MS"
        self.__font_small__ = pygame.font.SysFont(FONT_NAME, 18)
        self.__font_medium__ = pygame.font.SysFont(FONT_NAME, 24)
        self.__font_large__ = pygame.font.SysFont(FONT_NAME, 50)

        self.__clock__ = pygame.time.Clock()

        self.__game__: Optional[BackgammonGame] = None
        self.__current_scene__ = "MAIN_MENU"
        self.__board_state__: str = "ROLL_DICE"
        self.__selected_point__: Optional[int] = None
        self.__message__: str = "¡Bienvenido!"
        self.__possible_moves__: list[int] = []

        self.__player1_name__: str = "Jugador 1"
        self.__player2_name__: str = "Jugador 2"
        self.__active_input_box__: Optional[int] = None

        self._init_dice_pip_coords()
        self._define_click_rects()

    def _define_click_rects(self):
        """
        Define todas las áreas clickeables para menús y juego.

        Recibe: self (la instancia de PygameUI).
        Hace: Calcula y asigna objetos pygame.Rect a atributos privados para representar
              botones, cajas de texto, puntos del tablero y áreas de bear-off/barra.
        Devuelve: Nada.
        """

        btn_width, btn_height = 300, 60
        center_x = SCREEN_WIDTH // 2
        self.__btn_rect_jugar__ = pygame.Rect(center_x - btn_width // 2, 300, btn_width, btn_height)
        self.__btn_rect_instrucciones__ = pygame.Rect(center_x - btn_width // 2, 400, btn_width, btn_height)

        input_width, input_height = 400, 50
        self.__input_rect_j1__ = pygame.Rect(center_x - input_width // 2, 200, input_width, input_height)
        self.__input_rect_j2__ = pygame.Rect(center_x - input_width // 2, 300, input_width, input_height)

        start_btn_width = 350
        self.__btn_start_j1__ = pygame.Rect(center_x - start_btn_width // 2, 400, start_btn_width, btn_height)
        self.__btn_start_j2__ = pygame.Rect(center_x - start_btn_width // 2, 480, start_btn_width, btn_height)

        self.__btn_rect_volver__ = pygame.Rect(30, SCREEN_HEIGHT - 70, 150, 50)
        self.__btn_rect_salir__ = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 70, 150, 50)

        self.__point_rects__: list[pygame.Rect] = self._calculate_point_rects()

        self.__bar_white_rect__: pygame.Rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BAR_WIDTH // 2, MARGIN_Y, BAR_WIDTH, POINT_HEIGHT
        )
        self.__bar_black_rect__: pygame.Rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BAR_WIDTH // 2, BOARD_HEIGHT - MARGIN_Y - POINT_HEIGHT, BAR_WIDTH, POINT_HEIGHT
        )

        self.__dice_roll_rect__: pygame.Rect = pygame.Rect(DICE_BUTTON_X - 60, DICE_BUTTON_Y - 25, 140, 50)

        tray_margin_y = 10
        tray_height = (BOARD_HEIGHT / 2) - MARGIN_Y - tray_margin_y
        self.__off_white_rect__: pygame.Rect = pygame.Rect(BEAR_OFF_TRAY_X, MARGIN_Y, BEAR_OFF_TRAY_WIDTH, tray_height)
        self.__off_black_rect__: pygame.Rect = pygame.Rect(BEAR_OFF_TRAY_X, (BOARD_HEIGHT / 2) + tray_margin_y, BEAR_OFF_TRAY_WIDTH, tray_height)

        self.__btn_rect_game_to_menu__ = pygame.Rect(SCREEN_WIDTH - 200, UI_AREA_Y_START + 50, 180, 50)

        self.__btn_pass_turn__ = pygame.Rect(PLAYER_AREA_X, UI_AREA_Y_START + 120, 160, 40)


    def _init_dice_pip_coords(self):
        """
        Inicializa las coordenadas relativas (0.0 a 1.0) para los puntos (pips)
        en las caras de los dados.

        Recibe: self (la instancia de PygameUI).
        Hace: Define el diccionario `__dice_pip_coords__` para el dibujo de los dados.
        Devuelve: Nada.
        """
        c = 0.5; q = 0.25; t = 0.75
        self.__dice_pip_coords__ = {
            1: [(c, c)], 2: [(q, q), (t, t)], 3: [(q, q), (c, c), (t, t)],
            4: [(q, q), (t, q), (q, t), (t, t)],
            5: [(q, q), (t, q), (c, c), (q, t), (t, t)],
            6: [(q, q), (t, q), (q, c), (t, c), (q, t), (t, t)],
        }

    def _calculate_point_rects(self) -> list[pygame.Rect]:
        """
        Crea 24 Rects (áreas clickeables) para los puntos del tablero.

        Recibe: self (la instancia de PygameUI).
        Hace: Calcula las posiciones y dimensiones para los 24 triángulos del tablero.
        Devuelve: Una lista de 24 objetos `pygame.Rect` representando los puntos.
        """

        bar_center_x = SCREEN_WIDTH / 2
        bar_left_edge = bar_center_x - (BAR_WIDTH / 2)
        bar_right_edge = bar_center_x + (BAR_WIDTH / 2)

        rects_top, rects_bottom = [], []
        rects_top_right, rects_top_left = [], []
        rects_bottom_left, rects_bottom_right = [], []

        for i in range(6):
            x_left_tr = bar_right_edge + i * POINT_WIDTH
            rects_top_right.append(pygame.Rect(x_left_tr, MARGIN_Y, POINT_WIDTH, POINT_HEIGHT))

            x_left_tl = bar_left_edge - (i + 1) * POINT_WIDTH
            rects_top_left.append(pygame.Rect(x_left_tl, MARGIN_Y, POINT_WIDTH, POINT_HEIGHT))

            x_left_bl = bar_left_edge - (6 - i) * POINT_WIDTH
            rects_bottom_left.append(pygame.Rect(x_left_bl, BOARD_HEIGHT - MARGIN_Y - POINT_HEIGHT, POINT_WIDTH, POINT_HEIGHT))

            x_left_br = bar_right_edge + i * POINT_WIDTH
            rects_bottom_right.append(pygame.Rect(x_left_br, BOARD_HEIGHT - MARGIN_Y - POINT_HEIGHT, POINT_WIDTH, POINT_HEIGHT))

        rects_top.extend(rects_top_right[::-1])
        rects_top.extend(rects_top_left)
        rects_bottom.extend(rects_bottom_left)
        rects_bottom.extend(rects_bottom_right)

        return rects_top + rects_bottom

    def _get_piece_center_pos(self, point_index: int, piece_num: int, total_pieces: int) -> Tuple[int, int]:
        """
        Calcula la posición central de una ficha en un punto dado.

        Recibe:
            point_index (int): Índice del punto (0-23).
            piece_num (int): Posición de la ficha en la pila (0 es la de abajo).
            total_pieces (int): Número total de fichas en ese punto.
        Hace: Calcula las coordenadas (x, y) para dibujar la ficha, ajustando el espaciado
              si hay muchas fichas para crear una pila.
        Devuelve: Una tupla `(x, y)` con las coordenadas centrales.
        """
        rect = self.__point_rects__[point_index]
        is_top_row = point_index < 12
        y_direction = 1 if is_top_row else -1
        y_base = rect.top if is_top_row else rect.bottom

        x = rect.centerx

        if total_pieces > 5:
            max_y_offset = POINT_HEIGHT - PIECE_RADIUS
            y_spacing = max_y_offset / (total_pieces -1) if total_pieces > 1 else 0
            if y_spacing < PIECE_RADIUS * 1.5:
                y_spacing = PIECE_RADIUS * 1.5
            if y_spacing > PIECE_RADIUS * 2:
                y_spacing = PIECE_RADIUS * 2
        else:
            y_spacing = PIECE_RADIUS * 2

        y_offset = piece_num * y_spacing + PIECE_RADIUS
        y = y_base + y_direction * y_offset

        return (x, y)

    def _get_bar_center_pos(self, is_white: bool, piece_num: int) -> Tuple[int, int]:
        """
        Calcula la posición central de una ficha en la barra.

        Recibe:
            is_white (bool): Indica si la ficha es blanca (True) o negra (False).
            piece_num (int): Posición de la ficha en la pila (0 es la de abajo).
        Hace: Calcula las coordenadas (x, y) para dibujar la ficha en la barra.
        Devuelve: Una tupla `(x, y)` con las coordenadas centrales.
        """
        rect = self.__bar_white_rect__ if is_white else self.__bar_black_rect__
        x = rect.centerx
        y_direction = 1 if is_white else -1
        y_base = rect.top if is_white else rect.bottom

        y = y_base + y_direction * (piece_num * (PIECE_RADIUS * 2) + PIECE_RADIUS)
        return (x, y)

    def _map_pos_to_point(self, pos: Tuple[int, int]) -> Tuple[Optional[str], Optional[int]]:
        """
        Mapea las coordenadas de un clic del ratón a una acción o punto del tablero.

        Recibe:
            pos (Tuple[int, int]): La posición (x, y) del clic del ratón.
        Hace: Comprueba si la posición colisiona con el botón de dados, los 24 puntos,
              la barra o las bandejas de bear-off.
        Devuelve: Una tupla `(target_type, point_index)` donde `target_type` es una
                  cadena ("DICE_ROLL", "POINT", "BAR", "OFF", None) y `point_index` es
                  el índice del punto (0-23, 24 para barra W, -1 para barra B o bear-off W, 25 para bear-off B)
                  o None.
        """
        if self.__dice_roll_rect__.collidepoint(pos):
            return ("DICE_ROLL", None)
        for i, rect in enumerate(self.__point_rects__):
            if rect.collidepoint(pos):
                return ("POINT", i)
        if self.__bar_white_rect__.collidepoint(pos):
            return ("BAR", 24)
        if self.__bar_black_rect__.collidepoint(pos):
            return ("BAR", -1)
        if self.__off_white_rect__.collidepoint(pos):
            return ("OFF", -1)
        if self.__off_black_rect__.collidepoint(pos):
            return ("OFF", 25)
        return (None, None)

    def _check_if_can_move(self) -> bool:
        """
        Verifica si el jugador actual tiene AL MENOS UN movimiento válido con los dados restantes.

        Recibe: self (la instancia de PygameUI).
        Hace: Itera sobre los dados restantes y las posiciones de las fichas del jugador
              actual (incluida la barra) para verificar si existe algún movimiento legal
              (normal, desde la barra o bear-off).
        Devuelve: `True` si existe al menos un movimiento válido, `False` en caso contrario.
        """
        if not self.__game__ or not self.__game__.__dados_restantes__:
            return False

        player = self.__game__.obtener_jugador_actual()
        player_color = player.ficha
        is_white = player.is_white()

        dados = self.__game__.__dados_restantes__

        # 1. Comprobar movimientos desde la BARRA
        if self.__game__.__board__.get_bar_count(player_color) > 0:
            start_point_bar = 24 if is_white else -1
            for dado in dados:
                end_point = start_point_bar - dado if is_white else start_point_bar + dado
                if 0 <= end_point <= 23 and self.__game__.validar_movimiento(start_point_bar, end_point)[0]:
                    return True
            return False

        # 2. Comprobar movimientos NORMALES y BEAR-OFF desde el tablero
        for start_point in range(24):
            color, count = self.__game__.__board__.get_point_info(start_point)

            if color == player_color and count > 0:

                for dado in dados:
                    end_point = start_point - dado if is_white else start_point + dado
                    if 0 <= end_point <= 23 and self.__game__.validar_movimiento(start_point, end_point)[0]:
                        return True

                off_point = -1 if is_white else 25
                if self.__game__.validar_movimiento(start_point, off_point)[0]:
                    return True

        return False

    def _calculate_possible_moves(self, start_point: int):
        """
        Calcula y almacena todos los puntos de destino válidos desde un punto de inicio
        basado en los dados restantes.

        Recibe:
            start_point (int): El índice del punto de inicio (0-23 para el tablero, 24 o -1 para la barra).
        Hace: Utiliza los dados restantes para verificar qué puntos (o bandejas de bear-off)
              son destinos válidos para un movimiento desde `start_point` y los almacena
              en `__possible_moves__`.
        Devuelve: Nada.
        """
        self.__possible_moves__ = []
        if not self.__game__:
            return

        player = self.__game__.obtener_jugador_actual()
        is_white = player.is_white()

        unique_dice = set(self.__game__.__dados_restantes__)

        for die_val in unique_dice:
            end_point = start_point - die_val if is_white else start_point + die_val

            if start_point in (-1, 24):
                if self.__game__.validar_movimiento(start_point, end_point)[0]:
                    self.__possible_moves__.append(end_point)
            elif 0 <= end_point <= 23:
                is_valid, _ = self.__game__.validar_movimiento(start_point, end_point)
                if is_valid:
                    self.__possible_moves__.append(end_point)

        off_point_target = -1 if is_white else 25
        if self.__game__.validar_movimiento(start_point, off_point_target)[0]:
            if off_point_target not in self.__possible_moves__:
                self.__possible_moves__.append(off_point_target)

    def run(self):
        """
        Bucle principal del juego que despacha escenas.

        Recibe: self (la instancia de PygameUI).
        Hace: Contiene el bucle principal de Pygame: maneja eventos, redibuja la escena
              actual y controla la velocidad de fotogramas.
        Devuelve: Nada (termina la ejecución de Pygame al salir del bucle).
        """
        while True:
            self._handle_events()
            self._draw_scene()
            pygame.display.flip()
            self.__clock__.tick(30)

    def _handle_events(self):
        """
        Procesa todos los eventos de Pygame (QUIT, MOUSEBUTTONDOWN, KEYDOWN).

        Recibe: self (la instancia de PygameUI).
        Hace: Lee la cola de eventos de Pygame y despacha el manejo a funciones específicas
              según la escena actual y el tipo de evento. También maneja la entrada de texto
              para la selección de jugadores.
        Devuelve: Nada.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.__current_scene__ == "MAIN_MENU":
                    self._handle_click_main_menu(event.pos)
                elif self.__current_scene__ == "PLAYER_SELECT":
                    self._handle_click_player_select(event.pos)
                elif self.__current_scene__ == "INSTRUCTIONS":
                    self._handle_click_instructions(event.pos)
                elif self.__current_scene__ == "GAME_BOARD":
                    self._handle_click_game_board(event.pos)

            if event.type == pygame.KEYDOWN:
                if self.__current_scene__ == "PLAYER_SELECT":

                    if event.key == pygame.K_TAB:
                        self.__active_input_box__ = 2 if self.__active_input_box__ == 1 else 1
                        return

                    current_name_attr = None
                    if self.__active_input_box__ == 1:
                        current_name_attr = '__player1_name__'
                    elif self.__active_input_box__ == 2:
                        current_name_attr = '__player2_name__'

                    if current_name_attr is None:
                        return

                    current_name = getattr(self, current_name_attr)

                    if event.key == pygame.K_BACKSPACE:
                        setattr(self, current_name_attr, current_name[:-1])

                    elif event.unicode.isprintable() and len(current_name) < 20:
                        setattr(self, current_name_attr, current_name + event.unicode)

    def _start_game(self, player_index: int):
        """
        Inicializa la lógica del juego Backgammon y cambia a la escena del tablero.

        Recibe:
            player_index (int): 0 para empezar como Jugador 1 (Blancas), 1 para Jugador 2 (Negras).
        Hace: Crea una instancia de `BackgammonGame`, establece el turno inicial,
              inicializa el estado del tablero y cambia la escena a "GAME_BOARD".
        Devuelve: Nada.
        """

        name1 = self.__player1_name__.strip() if self.__player1_name__.strip() else "Jugador 1"
        name2 = self.__player2_name__.strip() if self.__player2_name__.strip() else "Jugador 2"

        self.__game__ = BackgammonGame(name1, name2)
        self.__game__.__turno__ = player_index

        self.__board_state__ = "ROLL_DICE"
        self.__current_scene__ = "GAME_BOARD"
        self.__selected_point__ = None
        self.__possible_moves__ = []

        player = self.__game__.obtener_jugador_actual()

        self.__message__ = f"Turno de: {player.nombre} ({'Blancas' if player.is_white() else 'Negras'})\n¡Haz clic en 'Tirar Dados'!"

    def _handle_click_main_menu(self, pos: Tuple[int, int]):
        """
        Maneja los clics del ratón en la escena del menú principal.

        Recibe:
            pos (Tuple[int, int]): La posición (x, y) del clic del ratón.
        Hace: Cambia la escena a "PLAYER_SELECT", "INSTRUCTIONS" o sale del juego.
        Devuelve: Nada.
        """
        if self.__btn_rect_jugar__.collidepoint(pos):
            self.__current_scene__ = "PLAYER_SELECT"
        elif self.__btn_rect_instrucciones__.collidepoint(pos):
            self.__current_scene__ = "INSTRUCTIONS"
        elif self.__btn_rect_salir__.collidepoint(pos):
            pygame.quit()
            sys.exit()

    def _handle_click_player_select(self, pos: Tuple[int, int]):
        """
        Maneja clics en la escena de selección de jugador para activar cajas de texto o empezar el juego.

        Recibe:
            pos (Tuple[int, int]): La posición (x, y) del clic del ratón.
        Hace: Activa la caja de texto correspondiente, inicia el juego como Jugador 1 o 2,
              o vuelve al menú principal.
        Devuelve: Nada.
        """

        if self.__input_rect_j1__.collidepoint(pos):
            self.__active_input_box__ = 1
        elif self.__input_rect_j2__.collidepoint(pos):
            self.__active_input_box__ = 2

        elif self.__btn_start_j1__.collidepoint(pos):
            self._start_game(player_index=0)
        elif self.__btn_start_j2__.collidepoint(pos):
            self._start_game(player_index=1)

        elif self.__btn_rect_volver__.collidepoint(pos):
            self.__current_scene__ = "MAIN_MENU"
        else:
            self.__active_input_box__ = None

    def _handle_click_instructions(self, pos: Tuple[int, int]):
        """
        Maneja clics en la escena de instrucciones.

        Recibe:
            pos (Tuple[int, int]): La posición (x, y) del clic del ratón.
        Hace: Vuelve a la escena del menú principal.
        Devuelve: Nada.
        """
        if self.__btn_rect_volver__.collidepoint(pos):
            self.__current_scene__ = "MAIN_MENU"

    def _handle_click_game_board(self, pos: Tuple[int, int]):
        """
        Lógica de clics para la escena del tablero de juego.

        Recibe:
            pos (Tuple[int, int]): La posición (x, y) del clic del ratón.
        Hace: Dependiendo del `__board_state__`, maneja: tirar dados, seleccionar/deseleccionar
              un punto (o barra), intentar un movimiento o pasar el turno.
        Devuelve: Nada.
        """

        if self.__btn_rect_game_to_menu__.collidepoint(pos):
            self.__current_scene__ = "MAIN_MENU"
            self.__game__ = None
            self.__possible_moves__ = []
            self.__selected_point__ = None
            return

        if self.__btn_pass_turn__.collidepoint(pos) and self.__board_state__ == "PLAYER_MOVE":
            if not self._check_if_can_move():
                self.__game__.__dados_restantes__ = []
                self.__selected_point__ = None
                self.__possible_moves__ = []
                self.__game__.__turno__ += 1
                self.__board_state__ = "ROLL_DICE"
                player = self.__game__.obtener_jugador_actual()
                self.__message__ = f"Turno de: {player.nombre} ({'Blancas' if player.is_white() else 'Negras'})\n¡Haz clic en 'Tirar Dados'!"
                return
            else:
                self.__message__ = "¡Todavía tienes movimientos válidos pendientes!"
                return

        target_type, point_index = self._map_pos_to_point(pos)

        if self.__board_state__ == "ROLL_DICE":
            if target_type == "DICE_ROLL":
                self.__game__.tirar_dados()
                player = self.__game__.obtener_jugador_actual()
                self.__message__ = f"Turno de: {player.nombre} ({'Blancas' if player.is_white() else 'Negras'})\n¡Mueve tus fichas!"
                self.__board_state__ = "PLAYER_MOVE"

                if not self._check_if_can_move():
                    self.__message__ = f"¡No puedes mover con estos dados, {player.nombre}!\nPulsa 'Pasar Turno'."
            else:
                self.__message__ = "Debes tirar los dados primero."
            return

        if self.__board_state__ == "PLAYER_MOVE":
            if target_type in ("POINT", "BAR"):
                if self.__selected_point__ is None:
                    if target_type == "BAR":
                        player_color = self.__game__.obtener_jugador_actual().ficha
                        bar_count = self.__game__.__board__.get_bar_count(player_color)
                        if bar_count > 0:
                            self.__selected_point__ = point_index
                            self.__message__ = "Seleccionado desde la BARRA."
                            self._calculate_possible_moves(start_point=point_index)
                        else:
                            self.__message__ = "No tienes fichas en la barra para mover."
                            self.__possible_moves__ = []
                    else:
                        color, count = self.__game__.__board__.get_point_info(point_index)
                        player_color = self.__game__.obtener_jugador_actual().ficha
                        if color == player_color and count > 0:
                            if self.__game__.__board__.get_bar_count(player_color) > 0:
                                self.__message__ = "Debes mover las fichas de la barra primero."
                                self.__possible_moves__ = []
                            else:
                                self.__selected_point__ = point_index
                                self.__message__ = f"Punto {point_index} seleccionado."
                                self._calculate_possible_moves(start_point=point_index)
                        else:
                            self.__message__ = f"¡No tienes fichas en el punto {point_index}!"
                            self.__possible_moves__ = []
                else:
                    self._try_move(self.__selected_point__, point_index)

            elif target_type == "OFF":
                if self.__selected_point__ is not None:
                    self._try_move(self.__selected_point__, point_index)

            elif target_type == "DICE_ROLL":
                self.__message__ = "Ya has tirado los dados."

            else:
                self.__selected_point__ = None
                self.__possible_moves__ = []
                player = self.__game__.obtener_jugador_actual()
                self.__message__ = f"Turno de: {player.nombre} ({'Blancas' if player.is_white() else 'Negras'})\n¡Mueve tus fichas!"

    def _try_move(self, start: int, end: int):
        """
        Intenta validar y ejecutar un movimiento de backgammon.

        Recibe:
            start (int): El punto de inicio del movimiento (0-24).
            end (int): El punto de destino del movimiento (-1 a 25).
        Hace: Llama a `validar_movimiento` y `ejecutar_movimiento` del objeto `BackgammonGame`.
              Actualiza el estado del juego (`__board_state__`) y el mensaje (`__message__`).
              Cambia al siguiente turno si no quedan dados y el juego no ha terminado.
        Devuelve: Nada.
        """
        if not self.__game__: return

        is_valid, error_msg = self.__game__.validar_movimiento(start, end)

        if is_valid:
            try:
                self.__game__.ejecutar_movimiento(start, end)
                player = self.__game__.obtener_jugador_actual()

                if not self.__game__.check_victory():
                    self.__message__ = f"Movimiento {start} -> {end} exitoso.\nTurno de: {player.nombre}."

                if self.__game__.check_victory():
                    self.__board_state__ = "GAME_OVER"
                    winning_player_name = self.__game__.obtener_jugador_actual().nombre
                    self.__message__ = f"¡¡¡ {winning_player_name} GANA !!!"
                    self.__selected_point__ = None
                    self.__possible_moves__ = []
                    return
            except ValueError as e:
                self.__message__ = f"Error de ejecución: {e}"
        else:
            self.__message__ = error_msg

        self.__selected_point__ = None
        self.__possible_moves__ = []

        if not self.__game__.__dados_restantes__ and self.__board_state__ != "GAME_OVER":
            self.__game__.__turno__ += 1
            self.__board_state__ = "ROLL_DICE"
            player = self.__game__.obtener_jugador_actual()
            self.__message__ = f"Turno de: {player.nombre} ({'Blancas' if player.is_white() else 'Negras'})\n¡Haz clic en 'Tirar Dados'!"

    def _draw_scene(self):
        """
        Despacha el dibujado a la función de la escena actual.

        Recibe: self (la instancia de PygameUI).
        Hace: Llama al método de dibujo (_draw_...) correspondiente al valor de `__current_scene__`.
        Devuelve: Nada.
        """
        if self.__current_scene__ == "MAIN_MENU":
            self._draw_main_menu()
        elif self.__current_scene__ == "PLAYER_SELECT":
            self._draw_player_select()
        elif self.__current_scene__ == "INSTRUCTIONS":
            self._draw_instructions()
        elif self.__current_scene__ == "GAME_BOARD":
            self._draw_game_board()

    def _draw_button(self, rect: pygame.Rect, text: str, bg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, special_highlight=False):
        """
        Dibuja un botón y lo resalta si el mouse está encima.

        Recibe:
            rect (pygame.Rect): El rectángulo que define la posición y tamaño del botón.
            text (str): El texto a mostrar en el botón.
            bg_color (Tuple): Color de fondo normal.
            hover_color (Tuple): Color de fondo al pasar el ratón.
            special_highlight (bool): Si es True, añade un borde de resaltado extra.
        Hace: Dibuja el rectángulo del botón, el borde y el texto centrado.
        Devuelve: Nada.
        """
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)

        color = hover_color if is_hovered else bg_color
        pygame.draw.rect(self.__screen__, color, rect, border_radius=10)

        pygame.draw.rect(self.__screen__, BORDER_COLOR_BLACK, rect, 2, border_radius=10)

        if special_highlight:
            pygame.draw.rect(self.__screen__, DICE_ROLL_HIGHLIGHT_COLOR, rect, 4, border_radius=10)

        text_surf = self.__font_medium__.render(text, True, TEXT_COLOR_WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        self.__screen__.blit(text_surf, text_rect)

    def _draw_main_menu(self):
        """
        Dibuja la escena del menú principal.

        Recibe: self (la instancia de PygameUI).
        Hace: Rellena la pantalla y dibuja el título y los botones "Jugar",
              "Instrucciones" y "Salir".
        Devuelve: Nada.
        """
        self.__screen__.fill(BOARD_COLOR)

        title_surf = self.__font_large__.render("Backgammon", True, TEXT_COLOR_WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.__screen__.blit(title_surf, title_rect)

        self._draw_button(self.__btn_rect_jugar__, "Jugar")
        self._draw_button(self.__btn_rect_instrucciones__, "Instrucciones")

        self._draw_button(self.__btn_rect_salir__, "Salir", bg_color=(180, 50, 50), hover_color=(220, 60, 60))

    def _draw_player_select(self):
        """
        Dibuja la escena de selección de jugador con cajas de texto.

        Recibe: self (la instancia de PygameUI).
        Hace: Dibuja el título, las cajas de entrada de texto para los nombres de los jugadores
              y los botones para iniciar el juego como Jugador 1 o Jugador 2.
        Devuelve: Nada.
        """
        self.__screen__.fill(BOARD_COLOR)

        title_surf = self.__font_large__.render("Configurar Jugadores", True, TEXT_COLOR_WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.__screen__.blit(title_surf, title_rect)

        self._draw_text_input_box(
            self.__input_rect_j1__,
            "Jugador 1 (W):",
            self.__player1_name__,
            is_active=(self.__active_input_box__ == 1)
        )
        self._draw_text_input_box(
            self.__input_rect_j2__,
            "Jugador 2 (B):",
            self.__player2_name__,
            is_active=(self.__active_input_box__ == 2)
        )

        self._draw_button(self.__btn_start_j1__, "Empezar como Jugador 1 (W)")
        self._draw_button(self.__btn_start_j2__, "Empezar como Jugador 2 (B)")
        self._draw_button(self.__btn_rect_volver__, "Volver")

    def _draw_text_input_box(self, rect: pygame.Rect, label: str, text: str, is_active: bool):
        """
        Función auxiliar para dibujar una caja de texto con etiqueta y cursor.

        Recibe:
            rect (pygame.Rect): Rectángulo de la caja de texto.
            label (str): Etiqueta descriptiva (ej. "Jugador 1 (W):").
            text (str): El contenido actual de la caja de texto.
            is_active (bool): Si es True, resalta la caja y muestra el cursor.
        Hace: Dibuja el fondo de la caja, el borde, la etiqueta y el texto. Muestra un cursor
              parpadeante si la caja está activa.
        Devuelve: Nada.
        """

        label_surf = self.__font_medium__.render(label, True, TEXT_COLOR_WHITE)
        label_rect = label_surf.get_rect(bottomleft=(rect.left, rect.top - 5))
        self.__screen__.blit(label_surf, label_rect)

        bg_color = INPUT_BOX_ACTIVE_COLOR if is_active else INPUT_BOX_COLOR
        pygame.draw.rect(self.__screen__, bg_color, rect, border_radius=5)

        border_color = BORDER_COLOR_BLACK
        pygame.draw.rect(self.__screen__, border_color, rect, 2, border_radius=5)

        display_text = text if text else " "
        text_surf = self.__font_medium__.render(display_text, True, PIECE_BLACK)
        text_rect = text_surf.get_rect(midleft=(rect.left + 10, rect.centery))
        self.__screen__.blit(text_surf, text_rect)

        if is_active and (pygame.time.get_ticks() % 1000 < 500):
            cursor_x = text_rect.right + 2
            cursor_y_start = rect.top + 10
            cursor_y_end = rect.bottom - 10
            pygame.draw.line(self.__screen__, BORDER_COLOR_BLACK, (cursor_x, cursor_y_start), (cursor_x, cursor_y_end), 2)

    def _draw_instructions(self):
        """
        Dibuja la escena de instrucciones del juego.

        Recibe: self (la instancia de PygameUI).
        Hace: Dibuja el título de "Instrucciones", el texto explicativo del juego
              (con envoltura de texto y sombra) y el botón "Volver".
        Devuelve: Nada.
        """
        self.__screen__.fill(BOARD_COLOR)

        title_surf = self.__font_large__.render("Instrucciones", True, TEXT_COLOR_WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.__screen__.blit(title_surf, title_rect)

        texto = (
            "Objetivo: Ser el primer jugador en sacar (bear off) todas sus 15 fichas del tablero.\n\n"
            "Movimiento: Los jugadores mueven sus fichas según los números de dos dados. Las fichas blancas (W) se mueven en sentido antihorario (de 23 a 0). Las fichas negras (B) se mueven en sentido horario (de 0 a 23).\n\n"
            "Comer Fichas (Hit): Si aterrizas en un punto con una sola ficha oponente (un 'blot'), esa ficha es 'comida' y movida a la barra.\n\n"
            "Barra: Si tienes fichas en la barra, debes meterlas de nuevo al tablero antes de mover cualquier otra ficha.\n\n"
            "Sacar Fichas (Bear Off): Solo puedes empezar a sacar tus fichas una vez que todas tus 15 fichas estén en tu 'home board' (puntos 0-5 para Blancas, 18-23 para Negras)."
        )
        text_rect = pygame.Rect(MARGIN_X, 150, SCREEN_WIDTH - (2 * MARGIN_X), 400)

        self._draw_wrapped_text_shadowed(texto, text_rect, self.__font_medium__, TEXT_COLOR_WHITE, BORDER_COLOR_BLACK, paragraph_spacing=10)

        self._draw_button(self.__btn_rect_volver__, "Volver")

    def _draw_game_board(self):
        """
        Dibuja todos los componentes de la escena del tablero de juego.

        Recibe: self (la instancia de PygameUI).
        Hace: Dibuja el marco, el área de juego, los puntos, la barra, las bandejas
              de bear-off, las fichas y el panel de interfaz de usuario (UI).
              Si el juego ha terminado, superpone el mensaje de fin de juego.
        Devuelve: Nada.
        """

        self.__screen__.fill(BOARD_COLOR)

        pygame.draw.rect(self.__screen__, BORDER_COLOR_BLACK, (0, 0, SCREEN_WIDTH, BOARD_HEIGHT), 3)

        inner_frame_rect = pygame.Rect(MARGIN_X - 1, MARGIN_Y - 1, TOTAL_BOARD_WIDTH + 2, BOARD_HEIGHT - 2 * MARGIN_Y + 2)
        pygame.draw.rect(self.__screen__, BORDER_COLOR_BLACK, inner_frame_rect, 5)

        game_area_rect = pygame.Rect(MARGIN_X, MARGIN_Y, SCREEN_WIDTH - 2*MARGIN_X, BOARD_HEIGHT - 2*MARGIN_Y)
        pygame.draw.rect(self.__screen__, BACKGROUND_COLOR, game_area_rect)

        self._draw_board_layout()
        self._draw_bear_off_trays()
        self._draw_pieces()
        self._draw_bar_pieces()
        self._draw_ui_area()
        self._draw_dice()
        if self.__board_state__ == "GAME_OVER":
            self._draw_game_over()

    def _draw_board_layout(self):
        """
        Dibuja los triángulos (picos) del tablero y la barra central, resaltando movimientos posibles.

        Recibe: self (la instancia de PygameUI).
        Hace: Itera sobre los 24 puntos para dibujar los triángulos con colores alternados
              y bordes. Utiliza anti-aliasing. Resalta los picos si son destinos posibles.
              Dibuja la barra central.
        Devuelve: Nada.
        """

        for i, rect in enumerate(self.__point_rects__):

            color = POINT_COLOR_A if (i % 2 == 0) else POINT_COLOR_B

            if i < 12:
                p1, p2, p3 = (rect.left, rect.top), (rect.right, rect.top), (rect.centerx, rect.bottom)
            else:
                p1, p2, p3 = (rect.left, rect.bottom), (rect.right, rect.bottom), (rect.centerx, rect.top)

            pygame.gfxdraw.filled_polygon(self.__screen__, [p1, p2, p3], color)
            pygame.gfxdraw.aapolygon(self.__screen__, [p1, p2, p3], color)

            pygame.draw.aalines(self.__screen__, BORDER_COLOR_BLACK, True, [p1, p2, p3], 1)

            if i in self.__possible_moves__:
                pygame.draw.aalines(self.__screen__, MOVE_HIGHLIGHT_VALID, True, [p1, p2, p3], 1)
                if i < 12:
                     p1_in, p2_in, p3_in = (p1[0]+1, p1[1]+1), (p2[0]-1, p2[1]+1), (p3[0], p3[1]-1)
                else:
                     p1_in, p2_in, p3_in = (p1[0]+1, p1[1]-1), (p2[0]-1, p2[1]-1), (p3[0], p3[1]+1)
                pygame.draw.aalines(self.__screen__, MOVE_HIGHLIGHT_VALID, True, [p1_in, p2_in, p3_in], 1)


        bar_x = self.__bar_white_rect__.left
        bar_total_height = (BOARD_HEIGHT - 2 * MARGIN_Y)
        full_bar_rect = pygame.Rect(bar_x, MARGIN_Y, BAR_WIDTH, bar_total_height)

        pygame.draw.rect(self.__screen__, UI_COLOR, full_bar_rect)


    def _draw_bear_off_trays(self):
        """
        Dibuja las bandejas de bear-off (sacar fichas) y muestra la cuenta de fichas sacadas.

        Recibe: self (la instancia de PygameUI).
        Hace: Dibuja los rectángulos de las bandejas, sus bordes y el texto con el número
              de fichas que cada jugador ha sacado. Resalta si la bandeja es un destino
              posible para un movimiento.
        Devuelve: Nada.
        """

        pygame.draw.rect(self.__screen__, UI_COLOR, self.__off_white_rect__, 0, 5)
        pygame.draw.rect(self.__screen__, UI_COLOR, self.__off_black_rect__, 0, 5)

        pygame.draw.rect(self.__screen__, BORDER_COLOR_BLACK, self.__off_white_rect__, 2, 5)
        pygame.draw.rect(self.__screen__, BORDER_COLOR_BLACK, self.__off_black_rect__, 2, 5)

        mouse_pos = pygame.mouse.get_pos()

        is_hovered_w = self.__off_white_rect__.collidepoint(mouse_pos)
        is_possible_w = -1 in self.__possible_moves__

        if is_possible_w:
            pygame.draw.rect(self.__screen__, MOVE_HIGHLIGHT_VALID, self.__off_white_rect__, 4, 5)
        elif self.__selected_point__ is None and is_hovered_w:
             pygame.draw.rect(self.__screen__, HIGHLIGHT_COLOR, self.__off_white_rect__, 4, 5)

        is_hovered_b = self.__off_black_rect__.collidepoint(mouse_pos)
        is_possible_b = 25 in self.__possible_moves__

        if is_possible_b:
            pygame.draw.rect(self.__screen__, MOVE_HIGHLIGHT_VALID, self.__off_black_rect__, 4, 5)
        elif self.__selected_point__ is None and is_hovered_b:
             pygame.draw.rect(self.__screen__, HIGHLIGHT_COLOR, self.__off_black_rect__, 4, 5)

        pieces_w_off = (TOTAL_PIECES_PER_PLAYER - self.__game__.__board__.get_piece_count("W")) if self.__game__ else 0
        pieces_b_off = (TOTAL_PIECES_PER_PLAYER - self.__game__.__board__.get_piece_count("B")) if self.__game__ else 0

        if pieces_w_off > 0:
            text = self.__font_medium__.render(f"{pieces_w_off}", True, PIECE_WHITE)
            text_rect = text.get_rect(center=self.__off_white_rect__.center)
            self.__screen__.blit(text, text_rect)

        if pieces_b_off > 0:
            text = self.__font_medium__.render(f"{pieces_b_off}", True, PIECE_BLACK)
            text_rect = text.get_rect(center=self.__off_black_rect__.center)
            self.__screen__.blit(text, text_rect)

    def _draw_pieces(self):
        """
        Dibuja todas las fichas en los 24 puntos del tablero.

        Recibe: self (la instancia de PygameUI).
        Hace: Itera sobre los 24 puntos, calcula la posición de apilamiento de cada ficha
              y la dibuja como un círculo con borde. Resalta la ficha superior si el
              punto está seleccionado para movimiento.
        Devuelve: Nada.
        """
        if not self.__game__: return

        for i in range(24):
            color_str, count = self.__game__.__board__.get_point_info(i)
            if color_str is None or count == 0: continue

            piece_color = PIECE_WHITE if color_str == "W" else PIECE_BLACK

            for piece_num in range(count):
                pos = self._get_piece_center_pos(i, piece_num, count)
                pygame.draw.circle(self.__screen__, piece_color, pos, PIECE_RADIUS)
                pygame.draw.circle(self.__screen__, BORDER_COLOR_BLACK, pos, PIECE_RADIUS, 1)


        if self.__selected_point__ is not None and self.__selected_point__ in range(24):
            color, count = self.__game__.__board__.get_point_info(self.__selected_point__)
            if count > 0:
                piece_to_highlight_index = count - 1
                pos = self._get_piece_center_pos(self.__selected_point__, piece_to_highlight_index, count)

                highlight_surf = pygame.Surface((PIECE_RADIUS*2, PIECE_RADIUS*2), pygame.SRCALPHA)
                pygame.draw.circle(highlight_surf, HIGHLIGHT_COLOR, (PIECE_RADIUS, PIECE_RADIUS), PIECE_RADIUS)
                self.__screen__.blit(highlight_surf, (pos[0] - PIECE_RADIUS, pos[1] - PIECE_RADIUS))

    def _draw_bar_pieces(self):
        """
        Dibuja las fichas que se encuentran en la barra central.

        Recibe: self (la instancia de PygameUI).
        Hace: Calcula la posición de apilamiento para las fichas blancas y negras
              en la barra y las dibuja. Resalta la ficha superior si la barra está
              seleccionada para un movimiento.
        Devuelve: Nada.
        """
        if not self.__game__: return

        count_w = self.__game__.__board__.get_bar_count("W")
        for i in range(count_w):
            pos = self._get_bar_center_pos(True, i)
            pygame.draw.circle(self.__screen__, PIECE_WHITE, pos, PIECE_RADIUS)
            pygame.draw.circle(self.__screen__, BORDER_COLOR_BLACK, pos, PIECE_RADIUS, 1)

        count_b = self.__game__.__board__.get_bar_count("B")
        for i in range(count_b):
            pos = self._get_bar_center_pos(False, i)
            pygame.draw.circle(self.__screen__, PIECE_BLACK, pos, PIECE_RADIUS)
            pygame.draw.circle(self.__screen__, BORDER_COLOR_BLACK, pos, PIECE_RADIUS, 1)

        if self.__selected_point__ == 24 and count_w > 0:
            pos = self._get_bar_center_pos(True, count_w - 1)
            highlight_surf = pygame.Surface((PIECE_RADIUS*2, PIECE_RADIUS*2), pygame.SRCALPHA)
            pygame.draw.circle(highlight_surf, HIGHLIGHT_COLOR, (PIECE_RADIUS, PIECE_RADIUS), PIECE_RADIUS)
            self.__screen__.blit(highlight_surf, (pos[0] - PIECE_RADIUS, pos[1] - PIECE_RADIUS))
        elif self.__selected_point__ == -1 and count_b > 0:
            pos = self._get_bar_center_pos(False, count_b - 1)
            highlight_surf = pygame.Surface((PIECE_RADIUS*2, PIECE_RADIUS*2), pygame.SRCALPHA)
            pygame.draw.circle(highlight_surf, HIGHLIGHT_COLOR, (PIECE_RADIUS, PIECE_RADIUS), PIECE_RADIUS)
            self.__screen__.blit(highlight_surf, (pos[0] - PIECE_RADIUS, pos[1] - PIECE_RADIUS))

    def _draw_ui_area(self):
        """
        Dibuja el panel de interfaz de usuario inferior con información de turno y acciones.

        Recibe: self (la instancia de PygameUI).
        Hace: Dibuja el fondo del panel de UI, el botón "Menú Principal", el botón
              "Tirar Dados" (o los dados si ya se tiraron), el botón "Pasar Turno"
              (si no hay movimientos válidos) y el mensaje de estado del juego.
        Devuelve: Nada.
        """
        pygame.draw.rect(self.__screen__, UI_COLOR, (0, UI_AREA_Y_START, SCREEN_WIDTH, UI_AREA_HEIGHT), 0)
        pygame.draw.rect(self.__screen__, BORDER_COLOR_BLACK, (0, UI_AREA_Y_START, SCREEN_WIDTH, UI_AREA_HEIGHT), 2)

        self._draw_button(self.__btn_rect_game_to_menu__, "Menú Principal", bg_color=(180, 50, 50), hover_color=(220, 60, 60))

        if not self.__game__: return

        if self.__board_state__ == "ROLL_DICE":
            self._draw_button(self.__dice_roll_rect__, "Tirar Dados", special_highlight=True)
        else:
            self._draw_dice()
            if not self._check_if_can_move():
                self._draw_button(
                    self.__btn_pass_turn__,
                    "Pasar Turno",
                    bg_color=BUTTON_PASS_COLOR,
                    hover_color=(255, 120, 0)
                )

        msg_color = (255, 100, 100) if "Error" in self.__message__ or "¡No" in self.__message__ or "bloqueado" in self.__message__ else TEXT_COLOR_WHITE

        msg_rect = pygame.Rect(MSG_AREA_X, MSG_AREA_Y, SCREEN_WIDTH - MSG_AREA_X - 220, 80)
        self._draw_wrapped_text_shadowed(self.__message__, msg_rect, self.__font_medium__, msg_color, BORDER_COLOR_BLACK)

    def _draw_dice_face(self, surface, x, y, size, num):
        """
        Dibuja una sola cara de dado con sus pips (puntos).

        Recibe:
            surface (pygame.Surface): La superficie donde dibujar el dado.
            x (int): Coordenada X de la esquina superior izquierda del dado.
            y (int): Coordenada Y de la esquina superior izquierda del dado.
            size (int): Ancho y alto del dado.
            num (int): El valor del dado (1 a 6).
        Hace: Dibuja el cuadrado del dado y los círculos (pips) correspondientes a su valor.
        Devuelve: Nada.
        """
        die_rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(surface, DICE_COLOR, die_rect, border_radius=5)
        pygame.draw.rect(surface, BORDER_COLOR_BLACK, die_rect, 1, border_radius=5)

        if num in self.__dice_pip_coords__:
            for rel_x, rel_y in self.__dice_pip_coords__[num]:
                pip_pos = (int(x + rel_x * size), int(y + rel_y * size))
                pygame.draw.circle(surface, PIP_COLOR, pip_pos, PIP_RADIUS)

    def _draw_wrapped_text_shadowed(self, text: str, rect: pygame.Rect, font: pygame.font.Font, color: Tuple[int, int, int], shadow_color: Tuple[int, int, int], paragraph_spacing: int = 0):
        """
        Dibuja texto envuelto con sombra (borde) y maneja saltos de línea y espaciado entre párrafos.

        Recibe:
            text (str): El texto a dibujar, puede contener '\n' o '\n\n'.
            rect (pygame.Rect): El área donde se debe dibujar el texto (utilizado para el ancho máximo).
            font (pygame.font.Font): La fuente a utilizar.
            color (Tuple): Color principal del texto.
            shadow_color (Tuple): Color de la sombra/borde.
            paragraph_spacing (int): Espaciado vertical extra entre párrafos.
        Hace: Divide el texto en párrafos y líneas, y dibuja cada línea con un ligero
              desplazamiento para crear un efecto de sombra.
        Devuelve: Nada.
        """
        paragraphs = text.split('\n\n')
        y_offset = 0

        for para_idx, paragraph in enumerate(paragraphs):
            words = paragraph.split(' ')
            lines = []
            current_line = []

            for word in words:
                if "\n" in word:
                    parts = word.split("\n")
                    for i, part in enumerate(parts):
                        if i > 0:
                            lines.append(' '.join(current_line))
                            current_line = [part] if part else []
                        else:
                            current_line.append(part)
                    continue

                current_line.append(word)
                line_test = ' '.join(current_line)
                if font.size(line_test)[0] > rect.width and len(current_line) > 1:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            lines.append(' '.join(current_line))

            for line in lines:
                shadow_surf = font.render(line, True, shadow_color)
                line_surf = font.render(line, True, color)

                self.__screen__.blit(shadow_surf, (rect.x + 1, rect.y + y_offset + 1))
                self.__screen__.blit(line_surf, (rect.x, rect.y + y_offset))
                y_offset += font.get_linesize()

            if para_idx < len(paragraphs) - 1:
                y_offset += paragraph_spacing

    def _draw_dice(self):
        """
        Dibuja los dados restantes gráficamente en el panel de UI.

        Recibe: self (la instancia de PygameUI).
        Hace: Calcula la posición para centrar los dados restantes en el área de UI
              y llama a `_draw_dice_face` para cada valor de dado.
        Devuelve: Nada.
        """
        if not self.__game__ or self.__board_state__ != "PLAYER_MOVE":
             return

        dados = self.__game__.__dados_restantes__
        y_pos = DICE_BUTTON_Y - (DICE_SIZE / 2)
        total_width = len(dados) * DICE_SIZE + (len(dados) - 1) * DICE_PADDING
        start_x = DICE_BUTTON_X - (total_width / 2)
        for i, num in enumerate(dados):
            x_pos = start_x + i * (DICE_SIZE + DICE_PADDING)
            self._draw_dice_face(self.__screen__, x_pos, y_pos, DICE_SIZE, num)

    def _draw_game_over(self):
        """
        Muestra un mensaje superpuesto de fin de juego en el centro del tablero.

        Recibe: self (la instancia de PygameUI).
        Hace: Dibuja un rectángulo de fondo para el mensaje y superpone el mensaje
              de victoria (`__message__`) para indicar el fin del juego.
        Devuelve: Nada.
        """
        end_surf = self.__font_large__.render(self.__message__, True, (200, 0, 0))
        end_rect = end_surf.get_rect(center=(SCREEN_WIDTH // 2, BOARD_HEIGHT // 2))

        bg_rect = end_rect.inflate(40, 40)
        pygame.draw.rect(self.__screen__, PIECE_WHITE, bg_rect, border_radius=10)
        pygame.draw.rect(self.__screen__, BORDER_COLOR_BLACK, bg_rect, 3, border_radius=10)

        self.__screen__.blit(end_surf, end_rect)


if __name__ == "__main__":
    try:
        ui = PygameUI()
        ui.run()
    except Exception as e:
        print(f"Error al iniciar Pygame UI: {e}")
        pygame.quit()
        sys.exit()