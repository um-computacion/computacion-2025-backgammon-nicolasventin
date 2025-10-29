import random


class Dice:
    """Clase para la lógica de tirada de dados."""

    def __init__(self):
        """Inicializa la lista de valores de la tirada."""
        self.__values__ = []

    @staticmethod
    def get_dice():
        """Realiza la tirada de dados."""
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
            else:
                return (
                    dice_0,
                    dice_1,
                )
        except Exception:
            # Captura la excepción para retornar una tupla vacía en caso de error
            return ()
