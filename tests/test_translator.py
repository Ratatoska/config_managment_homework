"""Проверки грамматики Lark."""

from pathlib import Path
import sys
import unittest

from lark.exceptions import UnexpectedInput

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from translator import translate


class TranslatorTests(unittest.TestCase):
    """Разбор значений и обработка неверного ввода."""

    def test_comments_and_nested_arrays(self):
        """Комментарии пропускаются, вложенность и пустой массив сохраняются."""
        source = "; строка\n { две\n строки } #(42., #(1.5, #()), 0.)"
        self.assertEqual(translate(source), [42.0, [1.5, []], 0.0])

    def test_value_and_document(self):
        """Отдельное число идёт в JSON как число, список значений как массив."""
        self.assertEqual(translate("5."), 5.0)
        self.assertEqual(translate("5. 6."), [5.0, 6.0])

    def test_syntax_errors(self):
        """Ошибки числа, массива и незакрытого комментария обнаруживаются."""
        for source in ("5", "#(2. 4.)", "#(1.,)", "{ комментарий"):
            with self.subTest(source=source):
                with self.assertRaises(UnexpectedInput):
                    translate(source)
