"""Скрипт для запуска всех тестов."""

import sys
import subprocess
from pathlib import Path

def run_test(test_file):
    """Запускает один тест как отдельный процесс."""
    print(f"\n{'='*60}")
    print(f"Запуск {test_file}")
    print('='*60)
    
    try:
        # Запускаем тест как отдельный процесс
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        # Выводим stdout
        if result.stdout:
            print(result.stdout)
        
        # Выводим stderr если есть ошибки
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"ОШИБКА при запуске теста: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    tests = [
        'tests/test1.py',
        'tests/test2.py',
        'tests/test3.py',
        'tests/test4.py',
    ]
    
    results = []
    for test in tests:
        success = run_test(test)
        results.append((test, success))
    
    print(f"\n{'='*60}")
    print("РЕЗУЛЬТАТЫ ТЕСТОВ")
    print('='*60)
    
    all_passed = True
    for test, success in results:
        status = "[OK] ПРОЙДЕН" if success else "[FAIL] НЕ ПРОЙДЕН"
        print(f"{test}: {status}")
        if not success:
            all_passed = False
    
    print('='*60)
    if all_passed:
        print("Все тесты пройдены успешно!")
        sys.exit(0)
    else:
        print("Некоторые тесты не пройдены.")
        sys.exit(1)

