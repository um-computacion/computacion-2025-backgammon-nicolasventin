"""
Tests para el módulo Dice.
"""

from unittest import TestCase
from unittest.mock import patch
import unittest
from src.game.dado import Dice


class TestDice(TestCase):
    """Pruebas para la clase Dice."""

    @patch("random.randint", side_effect=[5, 2])
    def test_simple(self, randint_patched):
        """
        Recibe:
            randint_patched (MagicMock): Mock de 'random.randint'.
        Hace:
            Llama a `Dice.get_dice()` forzando una tirada no-doble (5 y 2).
        Devuelve:
            Verifica que la tupla devuelta sea (5, 2) y tenga longitud 2.
        """
        dice = Dice.get_dice()
        self.assertEqual(len(dice), 2)
        self.assertEqual(dice[0], 5)
        self.assertEqual(dice[1], 2)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch("random.randint", return_value=1)
    def test_complex(self, randint_patched):
        """
        Recibe:
            randint_patched (MagicMock): Mock de 'random.randint'.
        Hace:
            Llama a `Dice.get_dice()` forzando una tirada doble (1 y 1).
        Devuelve:
            Verifica que la tupla devuelta sea (1, 1, 1, 1) y tenga longitud 4.
        """
        dice = Dice.get_dice()
        self.assertEqual(len(dice), 4)
        self.assertEqual(dice[0], 1)
        self.assertEqual(dice[1], 1)
        self.assertEqual(dice[2], 1)
        self.assertEqual(dice[3], 1)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch("random.randint", side_effect=ValueError("error!!"))
    def test_error(self, randint_patched):
        """
        Recibe:
            randint_patched (MagicMock): Mock de 'random.randint'.
        Hace:
            Llama a `Dice.get_dice()` forzando una excepción interna
            (ej. ValueError).
        Devuelve:
            Verifica que `get_dice` capture la excepción y devuelva
            una tupla vacía ().
        """
        dice = Dice.get_dice()
        self.assertEqual(len(dice), 0)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 1)

    def test_double(self):
        """
        Recibe:
            Nada.
        Hace:
            Prueba (de forma duplicada a `test_simple` y `test_complex`)
            ambos escenarios (simple y doble) usando `with patch`.
        Devuelve:
            Verifica los mismos resultados que los tests anteriores.
        """
        with patch("random.randint", side_effect=[5, 2]) as randint_patched:
            dice = Dice.get_dice()
            self.assertEqual(len(dice), 2)
            self.assertEqual(dice[0], 5)
            self.assertEqual(dice[1], 2)
            self.assertTrue(randint_patched.called)
            self.assertEqual(randint_patched.call_count, 2)

        with patch("random.randint", return_value=1) as randint_patched:
            dice = Dice.get_dice()
            self.assertEqual(len(dice), 4)
            self.assertEqual(dice[0], 1)
            self.assertEqual(dice[1], 1)
            self.assertEqual(dice[2], 1)
            self.assertEqual(dice[3], 1)
            self.assertTrue(randint_patched.called)
            self.assertEqual(randint_patched.call_count, 2)


if __name__ == "__main__":
    unittest.main()
