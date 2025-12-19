"""Транслятор для преобразования инструкций в промежуточное представление."""

from typing import List, Dict
from assembler.parser import Instruction


class Translator:
    """Транслятор инструкций в промежуточное представление."""
    
    def translate(self, instructions: List[Instruction]) -> List[Dict]:
        """
        Преобразует список инструкций в промежуточное представление.
        
        Args:
            instructions: Список объектов Instruction
            
        Returns:
            Список словарей с полями команд
        """
        intermediate = []
        
        for instr in instructions:
            representation = self._translate_instruction(instr)
            intermediate.append(representation)
        
        return intermediate
    
    def _translate_instruction(self, instr: Instruction) -> Dict:
        """Преобразует одну инструкцию в промежуточное представление."""
        result = {'A': instr.opcode}
        
        if instr.opcode == 2:  # load_const
            result['B'] = instr.fields['address']
            result['C'] = instr.fields['constant']
        elif instr.opcode == 7:  # read_mem
            result['B'] = instr.fields['result_addr']
            result['C'] = instr.fields['source_addr']
        elif instr.opcode == 5:  # write_mem
            result['B'] = instr.fields['source_addr']
            result['C'] = instr.fields['result_addr']
        elif instr.opcode == 13:  # bswap
            result['B'] = instr.fields['result_addr']
            result['C'] = instr.fields['operand_offset']
            result['D'] = instr.fields['result_offset']
            result['E'] = instr.fields['operand_addr']
        
        return result

