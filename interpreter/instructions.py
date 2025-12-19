"""Реализация инструкций УВМ."""

from interpreter.memory import Memory


class InstructionExecutor:
    """Исполнитель инструкций УВМ."""
    
    def __init__(self, memory: Memory):
        """
        Инициализирует исполнитель инструкций.
        
        Args:
            memory: Объект памяти УВМ
        """
        self.memory = memory
    
    def execute_load_const(self, address: int, constant: int):
        """
        Выполняет команду загрузки константы.
        
        Args:
            address: Адрес регистра для записи результата
            constant: Константа для загрузки
        """
        self.memory.set_register(address, constant)
    
    def execute_read_mem(self, result_addr: int, source_addr: int):
        """
        Выполняет команду чтения из памяти.
        
        Args:
            result_addr: Адрес регистра для записи результата
            source_addr: Адрес регистра, содержащего адрес источника в памяти
        """
        mem_addr = self.memory.get_register(source_addr)
        value = self.memory.read_word(mem_addr)
        self.memory.set_register(result_addr, value)
    
    def execute_write_mem(self, source_addr: int, result_addr: int):
        """
        Выполняет команду записи в память.
        
        Args:
            source_addr: Адрес регистра с данными для записи
            result_addr: Адрес регистра, содержащего адрес назначения в памяти
        """
        value = self.memory.get_register(source_addr)
        mem_addr = self.memory.get_register(result_addr)
        self.memory.write_word(mem_addr, value)
    
    def execute_bswap(self, result_addr: int, result_offset: int, 
                     operand_offset: int, operand_addr: int):
        """
        Выполняет команду bswap (обращение байтов).
        
        Args:
            result_addr: Адрес регистра с базовым адресом результата
            result_offset: Смещение для адреса результата
            operand_offset: Смещение для адреса операнда
            operand_addr: Адрес регистра с базовым адресом операнда
        """
        # Получаем адреса
        operand_base = self.memory.get_register(operand_addr)
        result_base = self.memory.get_register(result_addr)
        
        operand_mem_addr = operand_base + operand_offset
        result_mem_addr = result_base + result_offset
        
        # Читаем значение из памяти
        value = self.memory.read_word(operand_mem_addr)
        
        # Выполняем bswap (обращение байтов)
        swapped = ((value & 0x000000FF) << 24) | \
                  ((value & 0x0000FF00) << 8) | \
                  ((value & 0x00FF0000) >> 8) | \
                  ((value & 0xFF000000) >> 24)
        
        # Записываем результат в память
        self.memory.write_word(result_mem_addr, swapped)

