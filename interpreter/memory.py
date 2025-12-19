"""Модель памяти УВМ."""

from typing import List


class Memory:
    """Модель памяти УВМ (объединенная память команд и данных)."""
    
    def __init__(self, size: int = 65536):
        """
        Инициализирует память.
        
        Args:
            size: Размер памяти в байтах
        """
        self.size = size
        self.data: List[int] = [0] * size
        self.registers: List[int] = [0] * 128  # Регистры (адреса 0-127)
    
    def read_byte(self, address: int) -> int:
        """Читает байт из памяти."""
        if address < 0 or address >= self.size:
            raise IndexError(f"Адрес памяти вне диапазона: {address}")
        return self.data[address] & 0xFF
    
    def write_byte(self, address: int, value: int):
        """Записывает байт в память."""
        if address < 0 or address >= self.size:
            raise IndexError(f"Адрес памяти вне диапазона: {address}")
        self.data[address] = value & 0xFF
    
    def read_word(self, address: int) -> int:
        """Читает 32-битное слово из памяти (little-endian)."""
        return (self.read_byte(address) |
                (self.read_byte(address + 1) << 8) |
                (self.read_byte(address + 2) << 16) |
                (self.read_byte(address + 3) << 24))
    
    def write_word(self, address: int, value: int):
        """Записывает 32-битное слово в память (little-endian)."""
        self.write_byte(address, value & 0xFF)
        self.write_byte(address + 1, (value >> 8) & 0xFF)
        self.write_byte(address + 2, (value >> 16) & 0xFF)
        self.write_byte(address + 3, (value >> 24) & 0xFF)
    
    def get_register(self, address: int) -> int:
        """Получает значение регистра."""
        if address < 0 or address >= 128:
            raise IndexError(f"Адрес регистра вне диапазона: {address}")
        return self.registers[address]
    
    def set_register(self, address: int, value: int):
        """Устанавливает значение регистра."""
        if address < 0 or address >= 128:
            raise IndexError(f"Адрес регистра вне диапазона: {address}")
        self.registers[address] = value & 0xFFFFFFFF
    
    def load_program(self, program_bytes: bytes, offset: int = 0):
        """Загружает программу в память."""
        for i, byte_val in enumerate(program_bytes):
            if offset + i < self.size:
                self.data[offset + i] = byte_val

