"""Преобразовать учебную конфигурацию в данные для JSON."""

import math
import operator
from pathlib import Path

from lark import Lark, Transformer, v_args

GRAMMAR = Path(__file__).with_name("language.lark")
PARSER = Lark(GRAMMAR.read_text(encoding="utf-8"), parser="lalr",
              maybe_placeholders=False)
SINGLE_VALUE = 1
OPERAND_COUNT = 2
OPERATIONS = {"+": operator.add, "-": operator.sub, "*": operator.mul,
              "pow": math.pow, "pow()": math.pow}
DECLARATION = object()


@v_args(inline=True)
class Evaluate(Transformer):
    """Собрать числа и массивы из синтаксического дерева."""

    def __init__(self):
        """Начать трансляцию с пустой таблицей имён."""
        super().__init__()
        self.constants = {}

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
        items = [value for value in values if value is not DECLARATION]
        return items[0] if len(items) == SINGLE_VALUE else items

    def constant(self, name, value):
        """Объявить константу, доступную в следующих выражениях."""
        if name in self.constants:
            raise ValueError(f"константа {name!r} уже объявлена")
        self.constants[name] = value
        return DECLARATION

    def reference(self, name):
        """Подставить значение ранее объявленной константы."""
        if name not in self.constants:
            raise ValueError(f"неизвестная константа {name!r}")
        return self.constants[name]

    def expression(self, *items):
        """Вычислить постфиксное выражение стеком операндов."""
        stack = []
        for item in items:
            if isinstance(item, str):
                stack.append(calculate(stack, item))
            else:
                stack.append(item)
        if len(stack) != SINGLE_VALUE:
            raise ValueError("выражение должно давать ровно одно значение")
        return stack.pop()


def calculate(stack, operation):
    """Снять два числа со стека и применить оператор."""
    if len(stack) < OPERAND_COUNT:
        raise ValueError(f"{operation}: нужно два операнда")
    right, left = stack.pop(), stack.pop()
    if not isinstance(left, float) or not isinstance(right, float):
        raise ValueError(f"{operation}: операнды должны быть числами")
    result = OPERATIONS[operation](left, right)
    if not math.isfinite(result):
        raise ValueError("результат вне диапазона JSON")
    return result


def translate(source):
    """Разобрать текст по грамматике Lark и вычислить результат."""
    return Evaluate().transform(PARSER.parse(source))
