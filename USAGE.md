# Инструкция по использованию

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск тестов

```bash
python run_all_tests.py
```

Или отдельные тесты:
```bash
python tests/test1.py  # Тест load_const
python tests/test2.py  # Тест read_mem
python tests/test3.py  # Тест write_mem
python tests/test4.py  # Тест bswap
```

### 3. Ассемблирование программы

```bash
python -m assembler.cli examples/test_load_constant.yaml output/test.bin --test
```

### 4. Выполнение программы

```bash
python -m interpreter.cli output/test.bin output/memory.xml --start 0 --end 1024
```

## Примеры использования

### Пример 1: Тестовая команда load_const

```bash
# Ассемблирование
python -m assembler.cli examples/test_load_constant.yaml output/load_const.bin --test

# Выполнение
python -m interpreter.cli output/load_const.bin output/load_const_memory.xml
```

### Пример 2: Копирование массива

```bash
# Ассемблирование
python -m assembler.cli examples/test_array_copy.yaml output/array_copy.bin

# Выполнение
python -m interpreter.cli output/array_copy.bin output/array_copy_memory.xml --start 0x1000 --end 0x2100
```

### Пример 3: Операция bswap над вектором

```bash
# Ассемблирование
python -m assembler.cli examples/test_vector_operations.yaml output/vector.bin

# Выполнение
python -m interpreter.cli output/vector.bin output/vector_memory.xml --start 0x1000 --end 0x2100
```

## Структура проекта

- `assembler/` - модуль ассемблера
- `interpreter/` - модуль интерпретатора
- `examples/` - примеры YAML программ
- `tests/` - тесты
- `output/` - выходные файлы

## Формат YAML программы

```yaml
instructions:
  - opcode: load_const
    address: 124
    constant: 828
  - opcode: read_mem
    result_addr: 116
    source_addr: 68
```

Подробнее см. `Readme.md`.

