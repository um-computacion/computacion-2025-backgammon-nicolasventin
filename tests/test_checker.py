"""Pruebas unitarias para la clase Checker."""
import unittest
from src.game.checker import Checker


class TestChecker(unittest.TestCase):
    """Pruebas para la clase Checker."""
    def test_creacion_blanca(self):
        """Verifica la creación de una ficha 'W' (Blanca)."""
        checker = Checker("W")
        self.assertEqual(checker.color, "W")
        self.assertFalse(checker.comida)

    def test_creacion_negra(self):
        """Verifica la creación de una ficha 'B' (Negra)."""
        checker = Checker("B")
        self.assertEqual(checker.color, "B")
        self.assertFalse(checker.comida)

    def test_propiedad_comida_setter(self):
        """Prueba que la propiedad 'comida' (para la barra) se pueda modificar."""
        checker = Checker("w")

        checker.comida = True
        self.assertTrue(checker.comida)

        checker.comida = False
        self.assertFalse(checker.comida)


if __name__ == "__main__":
    unittest.main()
