"""Тест 4: Проверка команды bswap."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from assembler.parser import Parser
from assembler.translator import Translator
from assembler.codegen import CodeGenerator


def test_bswap():
    """Тестирует команду bswap."""
    yaml_content = """
instructions:
  - opcode: bswap
    result_addr: 82
    result_offset: 796
    operand_offset: 735
    operand_addr: 5
"""
    
    parser = Parser()
    instructions = parser.parse(yaml_content)
    
    translator = Translator()
    intermediate = translator.translate(instructions)
    
    codegen = CodeGenerator()
    machine_code = codegen.generate(intermediate)
    
    # Ожидаемый результат из спецификации
    expected = bytes([0x2D, 0xFD, 0x16, 0x8E, 0x29, 0x00])
    
    print("Тест bswap:")
    print(f"  Ожидается: {[hex(b) for b in expected]}")
    print(f"  Получено:   {[hex(b) for b in machine_code]}")
    
    if machine_code == expected:
        print("  [OK] ТЕСТ ПРОЙДЕН")
        return True
    else:
        print("  [FAIL] ТЕСТ НЕ ПРОЙДЕН")
        return False


if __name__ == '__main__':
    success = test_bswap()
    sys.exit(0 if success else 1)

