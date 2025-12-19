"""Тест 2: Проверка команды read_mem."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from assembler.parser import Parser
from assembler.translator import Translator
from assembler.codegen import CodeGenerator


def test_read_mem():
    """Тестирует команду read_mem."""
    yaml_content = """
instructions:
  - opcode: read_mem
    result_addr: 116
    source_addr: 68
"""
    
    parser = Parser()
    instructions = parser.parse(yaml_content)
    
    translator = Translator()
    intermediate = translator.translate(instructions)
    
    codegen = CodeGenerator()
    machine_code = codegen.generate(intermediate)
    
    # Ожидаемый результат из спецификации
    expected = bytes([0x47, 0x27, 0x02])
    
    print("Тест read_mem:")
    print(f"  Ожидается: {[hex(b) for b in expected]}")
    print(f"  Получено:   {[hex(b) for b in machine_code]}")
    
    if machine_code == expected:
        print("  [OK] ТЕСТ ПРОЙДЕН")
        return True
    else:
        print("  [FAIL] ТЕСТ НЕ ПРОЙДЕН")
        return False


if __name__ == '__main__':
    success = test_read_mem()
    sys.exit(0 if success else 1)

