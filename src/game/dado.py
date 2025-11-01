"""
Módulo para la lógica de tirada de dados en Backgammon.
"""

import random


class Dice:
    """
    Clase de utilidad para la lógica de tirada de dados.
    Provee métodos estáticos para obtener resultados de dados.
    """

    @staticmethod
    def get_dice():
        """
        Recibe:
            Nada.
        Hace:
            Simula una tirada de dos dados de 6 caras. Si los valores son
            iguales (dobles), genera cuatro valores idénticos.
        Devuelve:
            (tuple): Una tupla de 2 enteros (ej: (5, 2)) o 4 enteros
                     si es doble (ej: (3, 3, 3, 3)). Retorna una tupla
                     vacía si ocurre un error.
        """
        try:
            dice_0 = random.randint(1, 6)
            dice_1 = random.randint(1, 6)
            if dice_0 == dice_1:
                return (
                    dice_0,
                    dice_1,
                    dice_0,
                    dice_1,
                )
            return (
                dice_0,
                dice_1,
            )
        except (ValueError, TypeError):
            # Captura la excepción para retornar una tupla vacía en caso de error
            return ()
