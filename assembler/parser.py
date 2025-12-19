"""Парсер YAML файлов для ассемблера УВМ."""

import yaml
from typing import List, Dict, Any


class Instruction:
    """Класс для представления инструкции."""
    
    def __init__(self, opcode: int, **kwargs):
        self.opcode = opcode
        self.fields = kwargs
    
    def __repr__(self):
        fields_str = ", ".join(f"{k}={v}" for k, v in self.fields.items())
        return f"Instruction(opcode={self.opcode}, {fields_str})"


class Parser:
    """Парсер для преобразования YAML в промежуточное представление."""
    
    # Маппинг имен команд на коды операций
    OPCODES = {
        'load_const': 2,
        'read_mem': 7,
        'write_mem': 5,
        'bswap': 13,
    }
    
    def parse(self, yaml_content: str) -> List[Instruction]:
        """
        Парсит YAML содержимое и возвращает список инструкций.
        
        Args:
            yaml_content: Строка с YAML содержимым
            
        Returns:
            Список объектов Instruction
        """
        data = yaml.safe_load(yaml_content)
        
        if not isinstance(data, dict) or 'instructions' not in data:
            raise ValueError("YAML должен содержать ключ 'instructions'")
        
        instructions = []
        for instr_data in data['instructions']:
            instruction = self._parse_instruction(instr_data)
            instructions.append(instruction)
        
        return instructions
    
    def _parse_instruction(self, instr_data: Dict[str, Any]) -> Instruction:
        """Парсит одну инструкцию."""
        if 'opcode' not in instr_data:
            raise ValueError("Инструкция должна содержать поле 'opcode'")
        
        opcode_name = instr_data['opcode']
        if opcode_name not in self.OPCODES:
            raise ValueError(f"Неизвестный код операции: {opcode_name}")
        
        opcode = self.OPCODES[opcode_name]
        fields = {}
        
        # Парсинг полей в зависимости от типа команды
        if opcode_name == 'load_const':
            fields['address'] = instr_data.get('address', 0)
            fields['constant'] = instr_data.get('constant', 0)
        elif opcode_name == 'read_mem':
            fields['result_addr'] = instr_data.get('result_addr', 0)
            fields['source_addr'] = instr_data.get('source_addr', 0)
        elif opcode_name == 'write_mem':
            fields['source_addr'] = instr_data.get('source_addr', 0)
            fields['result_addr'] = instr_data.get('result_addr', 0)
        elif opcode_name == 'bswap':
            fields['result_addr'] = instr_data.get('result_addr', 0)
            fields['result_offset'] = instr_data.get('result_offset', 0)
            fields['operand_offset'] = instr_data.get('operand_offset', 0)
            fields['operand_addr'] = instr_data.get('operand_addr', 0)
        
        return Instruction(opcode, **fields)

