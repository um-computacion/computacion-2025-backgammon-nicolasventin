"""
Tests para el módulo Dice.
"""

from unittest import TestCase
from unittest.mock import patch
import unittest
from src.game.dado import Dice


class TestDice(TestCase):
    """Pruebas para la clase Dice."""
    # @patch.object(Clase, 'metodo', side_effect=[5, 2])
    # def test_method(self, randint_patched):
    #     ...

    @patch("random.randint", side_effect=[5, 2])
    def test_simple(self, randint_patched):
        """Prueba una tirada simple (no doble)."""
        dice = Dice.get_dice()
        self.assertEqual(len(dice), 2)
        self.assertEqual(dice[0], 5)
        self.assertEqual(dice[1], 2)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch("random.randint", return_value=1)
    def test_complex(self, randint_patched):
        """Prueba una tirada doble."""
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
        """Prueba que se lanza un error si se produce un error."""
        dice = Dice.get_dice()
        self.assertEqual(len(dice), 0)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 1)

    def test_double(self):
        """Prueba que la tiradas de dados dobles devuelven 4 valores."""
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
