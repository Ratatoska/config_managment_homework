# ДКР. Конфигурационный язык → JSON

Комаров В.Ю., ИКБО-41-25, вариант 8.

Этап 2. К числам и массивам добавлены константы и постфиксные выражения.

```text
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Пример: `const a = 4. #($a 1 +$, $a 2 pow()$)` выдаёт JSON `[5.0, 16.0]`.
