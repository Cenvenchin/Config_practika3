"""Быстрый тест для проверки работоспособности."""

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

print("Тест 1: Импорт модулей...")
try:
    from assembler.parser import Parser
    from assembler.translator import Translator
    from assembler.codegen import CodeGenerator
    print("  ✓ Модули ассемблера импортированы")
except Exception as e:
    print(f"  ✗ Ошибка импорта ассемблера: {e}")
    sys.exit(1)

try:
    from interpreter.memory import Memory
    from interpreter.cpu import CPU
    print("  ✓ Модули интерпретатора импортированы")
except Exception as e:
    print(f"  ✗ Ошибка импорта интерпретатора: {e}")
    sys.exit(1)

print("\nТест 2: Парсинг YAML...")
yaml_content = """
instructions:
  - opcode: load_const
    address: 124
    constant: 828
"""

try:
    parser = Parser()
    instructions = parser.parse(yaml_content)
    print(f"  ✓ Парсинг успешен, получено инструкций: {len(instructions)}")
except Exception as e:
    print(f"  ✗ Ошибка парсинга: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nТест 3: Трансляция...")
try:
    translator = Translator()
    intermediate = translator.translate(instructions)
    print(f"  ✓ Трансляция успешна, получено команд: {len(intermediate)}")
    print(f"  Первая команда: {intermediate[0]}")
except Exception as e:
    print(f"  ✗ Ошибка трансляции: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nТест 4: Генерация кода...")
try:
    codegen = CodeGenerator()
    machine_code = codegen.generate(intermediate)
    print(f"  ✓ Генерация успешна, получено байт: {len(machine_code)}")
    print(f"  Байты: {[hex(b) for b in machine_code]}")
except Exception as e:
    print(f"  ✗ Ошибка генерации: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nТест 5: Проверка соответствия тестовым данным...")
expected = bytes([0xC2, 0xE7, 0x19, 0x00, 0x00])
if machine_code == expected:
    print("  ✓ Код соответствует ожидаемому!")
else:
    print(f"  ✗ Несоответствие!")
    print(f"    Ожидается: {[hex(b) for b in expected]}")
    print(f"    Получено:   {[hex(b) for b in machine_code]}")

print("\n" + "="*60)
print("Все базовые тесты пройдены!")
print("="*60)

