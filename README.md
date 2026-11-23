# ДКР. Конфигурационный язык → JSON

Комаров В.Ю., ИКБО-41-25, вариант 8.

Этап 1. Программа читает числа, массивы и комментарии по грамматике Lark.

```text
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Пример: `#(1., #(2.5, 3.))` выдаёт JSON `[1.0, [2.5, 3.0]]`.
