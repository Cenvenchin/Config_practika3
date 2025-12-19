"""CPU интерпретатора УВМ."""

from typing import List, Dict
from interpreter.memory import Memory
from interpreter.instructions import InstructionExecutor


class CPU:
    """CPU интерпретатора УВМ."""
    
    def __init__(self, memory: Memory):
        """
        Инициализирует CPU.
        
        Args:
            memory: Объект памяти УВМ
        """
        self.memory = memory
        self.executor = InstructionExecutor(memory)
        self.pc = 0  # Program Counter
    
    def decode_instruction(self, bytes_data: bytes, offset: int) -> tuple:
        """
        Декодирует инструкцию из байтов.
        
        Args:
            bytes_data: Байты программы
            offset: Смещение для чтения
            
        Returns:
            Кортеж (opcode, fields_dict, size)
        """
        if offset >= len(bytes_data):
            return None
        
        byte0 = bytes_data[offset]
        opcode = byte0 & 0x0F
        
        if opcode == 2:  # load_const: 5 байт
            if offset + 5 > len(bytes_data):
                raise ValueError("Недостаточно байтов для команды load_const")
            
            byte1 = bytes_data[offset + 1]
            byte2 = bytes_data[offset + 2]
            byte3 = bytes_data[offset + 3]
            byte4 = bytes_data[offset + 4]
            
            B_low = (byte0 >> 4) & 0x0F
            B_high = (byte1 >> 5) & 0x07
            B = B_low | (B_high << 4)
            
            C_part1 = (byte1 >> 3) & 0x1F
            C_part2 = byte2
            C_part3 = byte3
            C_part4 = byte4 & 0x3F
            C = C_part1 | (C_part2 << 5) | (C_part3 << 13) | (C_part4 << 21)
            
            return (opcode, {'address': B, 'constant': C}, 5)
        
        elif opcode == 7:  # read_mem: 3 байт
            if offset + 3 > len(bytes_data):
                raise ValueError("Недостаточно байтов для команды read_mem")
            
            byte1 = bytes_data[offset + 1]
            byte2 = bytes_data[offset + 2]
            
            B_low = (byte0 >> 4) & 0x0F
            B_high = (byte1 >> 5) & 0x07
            B = B_low | (B_high << 4)
            
            C_part1 = (byte1 >> 3) & 0x1F
            C_part2 = byte2 & 0x03
            C = C_part1 | (C_part2 << 5)
            
            return (opcode, {'result_addr': B, 'source_addr': C}, 3)
        
        elif opcode == 5:  # write_mem: 3 байт
            if offset + 3 > len(bytes_data):
                raise ValueError("Недостаточно байтов для команды write_mem")
            
            byte1 = bytes_data[offset + 1]
            byte2 = bytes_data[offset + 2]
            
            B_low = (byte0 >> 4) & 0x0F
            B_high = (byte1 >> 5) & 0x07
            B = B_low | (B_high << 4)
            
            C_part1 = (byte1 >> 3) & 0x1F
            C_part2 = byte2 & 0x03
            C = C_part1 | (C_part2 << 5)
            
            return (opcode, {'source_addr': B, 'result_addr': C}, 3)
        
        elif opcode == 13:  # bswap: 6 байт
            if offset + 6 > len(bytes_data):
                raise ValueError("Недостаточно байтов для команды bswap")
            
            byte1 = bytes_data[offset + 1]
            byte2 = bytes_data[offset + 2]
            byte3 = bytes_data[offset + 3]
            byte4 = bytes_data[offset + 4]
            byte5 = bytes_data[offset + 5]
            
            B_low = (byte0 >> 4) & 0x0F
            B_high = (byte1 >> 5) & 0x07
            B = B_low | (B_high << 4)
            
            # C (operand_offset) биты 11-22 (12 бит)
            C_part1 = (byte1 >> 3) & 0x1F  # биты 11-15 (5 бит)
            C_part2 = byte2 & 0x0F  # биты 16-19 (4 бита)
            C = C_part1 | (C_part2 << 5)
            
            # D (result_offset) биты 23-34 (12 бит)
            D_part1 = (byte2 >> 4) & 0x0F  # биты 20-23 (4 бита)
            D_part2 = byte3  # биты 24-31 (8 бит)
            D_part3 = (byte4 >> 5) & 0x07  # биты 32-34 (3 бита)
            D = D_part1 | (D_part2 << 4) | (D_part3 << 12)
            
            # E (operand_addr) биты 35-41 (7 бит)
            E_part1 = (byte4 >> 2) & 0x07  # биты 35-37 (3 бита)
            E_part2 = byte5 & 0x0F  # биты 38-41 (4 бита)
            E = E_part1 | (E_part2 << 3)
            
            return (opcode, {
                'result_addr': B,
                'operand_offset': C,
                'result_offset': D,
                'operand_addr': E
            }, 6)
        
        else:
            raise ValueError(f"Неизвестный код операции: {opcode}")
    
    def execute(self, program_bytes: bytes):
        """
        Выполняет программу.
        
        Args:
            program_bytes: Байты программы
        """
        self.pc = 0
        
        while self.pc < len(program_bytes):
            try:
                decoded = self.decode_instruction(program_bytes, self.pc)
                if decoded is None:
                    break
                
                opcode, fields, size = decoded
                
                # Выполняем инструкцию
                if opcode == 2:
                    self.executor.execute_load_const(
                        fields['address'], fields['constant']
                    )
                elif opcode == 7:
                    self.executor.execute_read_mem(
                        fields['result_addr'], fields['source_addr']
                    )
                elif opcode == 5:
                    self.executor.execute_write_mem(
                        fields['source_addr'], fields['result_addr']
                    )
                elif opcode == 13:
                    self.executor.execute_bswap(
                        fields['result_addr'],
                        fields['result_offset'],
                        fields['operand_offset'],
                        fields['operand_addr']
                    )
                
                self.pc += size
                
            except Exception as e:
                raise RuntimeError(f"Ошибка выполнения на адресе {self.pc}: {e}")

