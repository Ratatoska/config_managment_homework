"""Запустить CLI через stdin и проверить вывод и код завершения."""

import json
import subprocess
import sys
import unittest

from test_translator import ROOT

CASES = {
    "audio": [48000.0, 1024.0, [0.8, 0.75]],
    "greenhouse": [[21.5, 25.5], [45.0, 65.0]],
    "storage": [1024.0, 131072.0, 112.0],
}


def invoke(source):
    """Передать текст процессу и забрать результат в UTF-8."""
    return subprocess.run([sys.executable, "-X", "utf8", "src/main.py"],
                          cwd=ROOT, input=source, capture_output=True,
                          encoding="utf-8", timeout=10)


class ExampleTests(unittest.TestCase):
    """Проверить полные сценарии, включая некорректный ввод."""

    def test_examples(self):
        """Прочитать три независимых конфигурации."""
        for name, expected in CASES.items():
            with self.subTest(name=name):
                path = ROOT / "examples" / f"{name}.cfg"
                result = invoke(path.read_text(encoding="utf-8"))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), expected)

    def test_cli_error(self):
        """Синтаксическая ошибка указывает позицию и не печатает JSON."""
        result = invoke("#(1.,)")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("строка 1, столбец", result.stderr)
        result = invoke("$unknown$")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("неизвестная константа", result.stderr)
