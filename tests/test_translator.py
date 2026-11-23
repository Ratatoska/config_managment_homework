"""Проверки грамматики Lark."""

from pathlib import Path
import sys
import unittest

from lark.exceptions import UnexpectedInput, VisitError

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

    def test_const_and_postfix(self):
        """Константы, четыре операции и порядок операндов."""
        source = "const a = 4. #($a 1 +$, $a 1 -$, $a 2 *$, $a 3 pow()$)"
        self.assertEqual(translate(source), [5.0, 3.0, 8.0, 64.0])
        self.assertEqual(translate("$10 3 - 2 *$"), 14.0)

    def test_nested_constant_values(self):
        """Массив и вычисленное значение доступны в следующих выражениях."""
        source = "const a = #(1., #(2.)) const b = $2 3 pow$ #($a$, $b$)"
        self.assertEqual(translate(source), [[1.0, [2.0]], 8.0])
        self.assertEqual(translate("const a = 2."), [])

    def test_expression_errors(self):
        """Не хватает операндов, лишнее значение, имена и неверный тип."""
        cases = {
            "$1 +$": "два операнда",
            "$1 2$": "ровно одно",
            "$absent$": "неизвестная",
            "const a = 1. const a = 2.": "уже объявлена",
            "$#() 1 +$": "должны быть числами",
        }
        for source, message in cases.items():
            with self.subTest(source=source):
                with self.assertRaisesRegex(VisitError, message):
                    translate(source)
