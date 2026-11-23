"""Преобразовать учебную конфигурацию в данные для JSON."""

import math
from pathlib import Path

from lark import Lark, Transformer, v_args

GRAMMAR = Path(__file__).with_name("language.lark")
PARSER = Lark(GRAMMAR.read_text(encoding="utf-8"), parser="lalr",
              maybe_placeholders=False)
SINGLE_VALUE = 1


@v_args(inline=True)
class Evaluate(Transformer):
    """Собрать числа и массивы из синтаксического дерева."""

    def number(self, text):
        """Преобразовать десятичное число и проверить диапазон."""
        value = float(text)
        if not math.isfinite(value):
            raise ValueError("число вне диапазона JSON")
        return value

    def array(self, *items):
        """Собрать элементы массива в исходном порядке."""
        return list(items)

    def start(self, *values):
        """Вернуть одно значение или массив верхнего уровня."""
        return values[0] if len(values) == SINGLE_VALUE else list(values)


def translate(source):
    """Разобрать текст по грамматике Lark и вычислить результат."""
    return Evaluate().transform(PARSER.parse(source))
