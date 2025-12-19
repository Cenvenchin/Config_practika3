"""CLI для ассемблера УВМ."""

import argparse
import sys
from pathlib import Path
from assembler.parser import Parser
from assembler.translator import Translator
from assembler.codegen import CodeGenerator


def main():
    """Главная функция CLI ассемблера."""
    parser = argparse.ArgumentParser(description='Ассемблер для учебной виртуальной машины')
    parser.add_argument('input_file', type=str, help='Путь к исходному YAML файлу')
    parser.add_argument('output_file', type=str, help='Путь к выходному бинарному файлу')
    parser.add_argument('--test', action='store_true', help='Режим тестирования')
    
    args = parser.parse_args()
    
    # Читаем входной файл
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {args.input_file} не найден", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Парсим YAML
    try:
        parser_obj = Parser()
        instructions = parser_obj.parse(yaml_content)
    except Exception as e:
        print(f"Ошибка при парсинге YAML: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Транслируем в промежуточное представление
    try:
        translator = Translator()
        intermediate = translator.translate(instructions)
    except Exception as e:
        print(f"Ошибка при трансляции: {e}", file=sys.stderr)
        sys.exit(1)
    
    # В режиме тестирования выводим промежуточное представление
    if args.test:
        print("Промежуточное представление:")
        for i, instr in enumerate(intermediate):
            fields = ", ".join(f"{k}={v}" for k, v in instr.items())
            print(f"  Инструкция {i}: {fields}")
        print()
    
    # Генерируем машинный код
    try:
        codegen = CodeGenerator()
        machine_code = codegen.generate(intermediate)
    except Exception as e:
        print(f"Ошибка при генерации кода: {e}", file=sys.stderr)
        sys.exit(1)
    
    # В режиме тестирования выводим байты
    if args.test:
        print("Машинный код (байты):")
        byte_str = ", ".join(f"0x{b:02X}" for b in machine_code)
        print(f"  {byte_str}")
        print()
    
    # Сохраняем результат
    try:
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(machine_code)
    except Exception as e:
        print(f"Ошибка при записи файла: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Ассемблировано команд: {len(intermediate)}")
    print(f"Результат сохранен в: {args.output_file}")


if __name__ == '__main__':
    main()

