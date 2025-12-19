"""Генератор машинного кода из промежуточного представления."""

from typing import List, Dict


class CodeGenerator:
    """Генератор машинного кода."""
    
    def generate(self, intermediate: List[Dict]) -> bytes:
        """
        Генерирует машинный код из промежуточного представления.
        
        Args:
            intermediate: Список словарей с полями команд
            
        Returns:
            Байтовая последовательность машинного кода
        """
        code = bytearray()
        
        for instr in intermediate:
            instr_bytes = self._generate_instruction(instr)
            code.extend(instr_bytes)
        
        return bytes(code)
    
    def _generate_instruction(self, instr: Dict) -> bytes:
        """Генерирует байты для одной инструкции."""
        opcode = instr['A']
        
        if opcode == 2:  # load_const: 5 байт
            # Биты 0-3: код (2)
            # Биты 4-10: адрес (B)
            # Биты 11-37: константа (C) - 27 бит
            address = instr['B']
            constant = instr['C']
            
            # Байт 0: биты 0-3 (opcode), биты 4-7 (младшие 4 бита адреса)
            byte0 = (opcode & 0x0F) | ((address & 0x0F) << 4)
            # Байт 1: биты 8-10 адреса (3 бита), биты 11-15 константы (5 бит)
            byte1 = ((address >> 4) & 0x07) | ((constant & 0x1F) << 3)
            # Байт 2: биты 16-23 константы (8 бит)
            byte2 = ((constant >> 5) & 0xFF)
            # Байт 3: биты 24-31 константы (8 бит)
            byte3 = ((constant >> 13) & 0xFF)
            # Байт 4: биты 32-37 константы (6 бит)
            byte4 = ((constant >> 21) & 0x3F)
            
            return bytes([byte0, byte1, byte2, byte3, byte4])
        
        elif opcode == 7:  # read_mem: 3 байт
            # Биты 0-3: код (7)
            # Биты 4-10: адрес результата (B)
            # Биты 11-17: адрес источника (C)
            result_addr = instr['B']
            source_addr = instr['C']
            
            # Байт 0: биты 0-3 (opcode), биты 4-7 (младшие 4 бита адреса результата)
            byte0 = (opcode & 0x0F) | ((result_addr & 0x0F) << 4)
            # Байт 1: биты 8-10 адреса результата (3 бита), биты 11-15 адреса источника (5 бит)
            byte1 = ((result_addr >> 4) & 0x07) | ((source_addr & 0x1F) << 3)
            # Байт 2: биты 16-17 адреса источника (2 бита)
            byte2 = (source_addr >> 5) & 0x03
            
            return bytes([byte0, byte1, byte2])
        
        elif opcode == 5:  # write_mem: 3 байт
            # Биты 0-3: код (5)
            # Биты 4-10: адрес источника (B)
            # Биты 11-17: адрес результата (C)
            source_addr = instr['B']
            result_addr = instr['C']
            
            # Байт 0: биты 0-3 (opcode), биты 4-7 (младшие 4 бита адреса источника)
            byte0 = (opcode & 0x0F) | ((source_addr & 0x0F) << 4)
            # Байт 1: биты 8-10 адреса источника (3 бита), биты 11-15 адреса результата (5 бит)
            byte1 = ((source_addr >> 4) & 0x07) | ((result_addr & 0x1F) << 3)
            # Байт 2: биты 16-17 адреса результата (2 бита)
            byte2 = (result_addr >> 5) & 0x03
            
            return bytes([byte0, byte1, byte2])
        
        elif opcode == 13:  # bswap: 6 байт
            # Биты 0-3: код (13)
            # Биты 4-10: адрес результата (B)
            # Биты 11-22: смещение операнда (C) - 12 бит
            # Биты 23-34: смещение результата (D) - 12 бит
            # Биты 35-41: адрес операнда (E) - 7 бит
            result_addr = instr['B']
            operand_offset = instr['C']
            result_offset = instr['D']
            operand_addr = instr['E']
            
            # Байт 0: биты 0-3 (opcode), биты 4-7 (B младшие 4)
            byte0 = (opcode & 0x0F) | ((result_addr & 0x0F) << 4)
            # Байт 1: биты 8-10 (B старшие 3), биты 11-15 (C младшие 5)
            byte1 = ((result_addr >> 4) & 0x07) | ((operand_offset & 0x1F) << 3)
            # Байт 2: биты 16-19 (C старшие 4), биты 20-23 (D младшие 4)
            byte2 = ((operand_offset >> 5) & 0x0F) | ((result_offset & 0x0F) << 4)
            # Байт 3: биты 24-31 (D следующие 8)
            byte3 = (result_offset >> 4) & 0xFF
            # Байт 4: биты 32-34 (D старшие 3 в битах 5-7), биты 35-37 (E младшие 3 в битах 2-4)
            # По декодированию в CPU: D_part3 = (byte4 >> 5) & 0x07, E_part1 = (byte4 >> 2) & 0x07
            byte4 = (((result_offset >> 12) & 0x07) << 5) | (((operand_addr & 0x07) << 2))
            # Байт 5: биты 38-41 (E старшие 4)
            byte5 = (operand_addr >> 3) & 0x0F
            
            return bytes([byte0, byte1, byte2, byte3, byte4, byte5])
        
        else:
            raise ValueError(f"Неизвестный код операции: {opcode}")

