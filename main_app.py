import os
import sys
import time

from src.dfs_engine import run_exact_dfs
from src.euler_engine import run_fast_eulerian

def main():
    print("=" * 65)
    print("      ПАЗЛ-КОНСТРУКТОР ЦИФРОВИХ ланцюжків (PortaOne Solution)")
    print("=" * 65)
    
    # 1. Interactive file selection menu
    print("\n[МЕНЮ] Виберіть джерело даних:")
    print("1) Запустити з демо файлом  (data/source.txt)")
    print("2) Вказати шлях до свого файлу")
    print("3) Вийти")
    
    choice = input("\nВведіть номер варіанту (1-3): ").strip()
    
    if choice == '3':
        print("Завершення  роботи програми.")
        return
        
    file_path = os.path.join("data", "source.txt")
    if choice == '2':
        file_path = input("Введіть шлях до вашого .txt файлу: ").strip()
        
    if not os.path.exists(file_path):
        print(f"\n[Помилка]: Файл '{file_path}' не знайден!")
        input("\nНатиснути Enter для виходу...")
        return

    # 2. Reading data
    valid_fragments = []
    invalid_lines_count = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            cleaned = line.strip()
            if not cleaned:
                continue
            
            if len(cleaned) >= 6 and cleaned.isdigit():
                valid_fragments.append(cleaned)
            else:
                invalid_lines_count += 1

    if not valid_fragments:
        print("\n[Помилка]: Файл не містить жодного коректного 6-значного числа!")
        input("\nНатиснути Enter для виходу...")
        return

    total_count = len(valid_fragments)
    print(f"\n[Інфо]: Успішно завантажено фрагментів: {total_count}")
    if invalid_lines_count > 0:
        print(f"[Увага]: Пропущено некоректних рядків (не 6 цифр): {invalid_lines_count}")
    print("-" * 50)
    
    # 3. Intelligent engine selection
    start_time = time.time()
    
    if total_count <= 170:
        print(f"[Вибір алгоритму]: Об'єм данних ({total_count} шт.) дозволяє запустити")
        print("                   точний DFS перебір для пошуку 100% максимуму")
        print("Зачекайте, будь ласка, йде розрахунок ...")
        
        result_puzzle, chain_len = run_exact_dfs(fragments)
        engine_used = "Точний DFS (Глобальний максимум)"
    else:
        print(f"[Вибір алгоритму]: Об'єм данних високий ({total_count} шт.). Точний DFS может зависнути.")
        print("                   Автоматично включається швидкий Ейлерів гібрид.")
        print("Обчислення оптимального ланцюжка методом Look-ahead розвилок...")
        
        # We launch with a depth of analysis of 3 steps
        result_puzzle, chain_len = run_fast_eulerian(fragments, depth=4)
        engine_used = "Швидкий Ейлерів гібрид (Look-ahead евристика)"
        
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 4. Output of results
    if result_puzzle:
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ РОБОТИ ПРОГРАМИ:")
        print("=" * 50)
        print(f"Двіжок обчислень:     {engine_used}")
        print(f"Довжина ланцюга (штук):  {chain_len} фрагментів")
        print(f"Довжина отриманого числа: {len(result_puzzle)} знаків")
        print(f"Час розрахунку:         {execution_time:.4f} секунд")
        print("\nЗібране число-пазл:")
        print(result_puzzle)
        print("=" * 50)
    else:
        print("\n[Увага]: Не вдалося зібрати жодного безперервного ланцюжка.")
        
    print("=" * 65)
    input("\nРоботу повністю завершено. Натисніть Enter, щоб вийти...")

if __name__ == "__main__":
    main()
    