"""CLI для интерпретатора УВМ."""

import argparse
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from interpreter.memory import Memory
from interpreter.cpu import CPU


def create_memory_dump(memory: Memory, start_addr: int, end_addr: int) -> ET.Element:
    """
    Создает XML дамп памяти.
    
    Args:
        memory: Объект памяти
        start_addr: Начальный адрес
        end_addr: Конечный адрес
        
    Returns:
        XML элемент с дампом памяти
    """
    root = ET.Element('memory_dump')
    root.set('start', str(start_addr))
    root.set('end', str(end_addr))
    
    for addr in range(start_addr, min(end_addr + 1, memory.size), 4):
        value = memory.read_word(addr)
        entry = ET.SubElement(root, 'entry')
        entry.set('address', f'0x{addr:04X}')
        entry.set('value', f'0x{value:08X}')
        entry.text = str(value)
    
    return root


def main():
    """Главная функция CLI интерпретатора."""
    parser = argparse.ArgumentParser(description='Интерпретатор для учебной виртуальной машины')
    parser.add_argument('program_file', type=str, help='Путь к бинарному файлу программы')
    parser.add_argument('dump_file', type=str, help='Путь к файлу для сохранения дампа памяти')
    parser.add_argument('--start', type=int, default=0, help='Начальный адрес для дампа')
    parser.add_argument('--end', type=int, default=1024, help='Конечный адрес для дампа')
    
    args = parser.parse_args()
    
    # Читаем программу
    try:
        with open(args.program_file, 'rb') as f:
            program_bytes = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {args.program_file} не найден", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Создаем память и CPU
    memory = Memory()
    cpu = CPU(memory)
    
    # Загружаем программу в память
    memory.load_program(program_bytes)
    
    # Выполняем программу
    try:
        cpu.execute(program_bytes)
    except Exception as e:
        print(f"Ошибка выполнения программы: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Создаем дамп памяти
    dump_root = create_memory_dump(memory, args.start, args.end)
    
    # Сохраняем дамп
    try:
        dump_path = Path(args.dump_file)
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        
        tree = ET.ElementTree(dump_root)
        ET.indent(tree, space='  ')
        tree.write(dump_path, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        print(f"Ошибка при сохранении дампа: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Программа выполнена успешно")
    print(f"Дамп памяти сохранен в: {args.dump_file}")


if __name__ == '__main__':
    main()

