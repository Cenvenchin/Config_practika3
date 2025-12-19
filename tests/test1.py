"""Тест 1: Проверка команды load_const."""

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from assembler.parser import Parser
from assembler.translator import Translator
from assembler.codegen import CodeGenerator


def test_load_const():
    """Тестирует команду load_const."""
    yaml_content = """
instructions:
  - opcode: load_const
    address: 124
    constant: 828
"""
    
    parser = Parser()
    instructions = parser.parse(yaml_content)
    
    translator = Translator()
    intermediate = translator.translate(instructions)
    
    codegen = CodeGenerator()
    machine_code = codegen.generate(intermediate)
    
    # Ожидаемый результат из спецификации
    expected = bytes([0xC2, 0xE7, 0x19, 0x00, 0x00])
    
    print("Тест load_const:")
    print(f"  Ожидается: {[hex(b) for b in expected]}")
    print(f"  Получено:   {[hex(b) for b in machine_code]}")
    
    if machine_code == expected:
        print("  [OK] ТЕСТ ПРОЙДЕН")
        return True
    else:
        print("  [FAIL] ТЕСТ НЕ ПРОЙДЕН")
        return False


if __name__ == '__main__':
    success = test_load_const()
    sys.exit(0 if success else 1)

