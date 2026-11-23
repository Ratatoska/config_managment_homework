"""Читать конфигурацию из stdin, писать JSON в stdout."""

import json
import sys

from lark.exceptions import UnexpectedInput, VisitError

from translator import translate


def main():
    """Печатать JSON только при успешном разборе."""
    source = sys.stdin.read()
    try:
        data = translate(source)
    except UnexpectedInput as error:
        print(f"Синтаксическая ошибка: строка {error.line}, столбец "
              f"{error.column}", file=sys.stderr)
        print(error.get_context(source).rstrip(), file=sys.stderr)
        return 1
    except VisitError as error:
        print(f"Ошибка: {error.orig_exc}", file=sys.stderr)
        return 1
    print(json.dumps(data, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
