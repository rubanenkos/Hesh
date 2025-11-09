"""
Головна програма для обчислення дайджестів повідомлень та пошуку колізій
"""

import os
import random
from hash_function import CustomHash


class HashCollisionFinder:
    """Клас для пошуку колізій хеш-функції"""
    
    def __init__(self, output_bits=8):
        self.hash_func = CustomHash(output_bits=output_bits)
        self.output_bits = output_bits
        self.max_value = (1 << output_bits) - 1
    
    def find_collision_smart(self, original_data, max_attempts=100000):
        target_hash = self.hash_func.hash(original_data)
        print(f"Цільове хеш-значення: {target_hash} ({self.hash_func.hash_to_binary(target_hash)})")
        print(f"Пошук колізії (розумний алгоритм)...")
        
        for attempt in range(max_attempts):
            if attempt % 10000 == 0 and attempt > 0:
                print(f"Спроба {attempt}/{max_attempts}...")
            
            test_data = bytearray(original_data)
            num_changes = random.randint(1, min(10, len(test_data)))
            
            for _ in range(num_changes):
                pos = random.randint(0, len(test_data) - 1)
                change_type = random.choice(['add', 'xor', 'swap'])
                if change_type == 'add':
                    test_data[pos] = (test_data[pos] + random.randint(1, 255)) % 256
                elif change_type == 'xor':
                    test_data[pos] ^= random.randint(1, 255)
                elif change_type == 'swap' and len(test_data) > 1:
                    other_pos = random.randint(0, len(test_data) - 1)
                    test_data[pos], test_data[other_pos] = test_data[other_pos], test_data[pos]
            
            hash_value = self.hash_func.hash(bytes(test_data))
            
            if hash_value == target_hash and bytes(test_data) != original_data:
                print(f"\n✓ Колізія знайдена за {attempt + 1} спроб!")
                return bytes(test_data)
        
        print(f"\n✗ Точна колізія не знайдена за {max_attempts} спроб")
        return None
    
    def create_collision_file(self, original_file, output_file, max_attempts=100000):
        print(f"\n{'='*60}")
        print(f"Створення колізії для файлу: {original_file}")
        print(f"{'='*60}")
        
        with open(original_file, 'rb') as f:
            original_data = f.read()
        
        original_hash = self.hash_func.hash(original_data)
        print(f"Оригінальний хеш: {original_hash} ({self.hash_func.hash_to_binary(original_hash)})")
        print(f"Розмір файлу: {len(original_data)} байт")
        
        collision_data = self.find_collision_smart(original_data, max_attempts)
        
        if collision_data and collision_data != original_data:
            with open(output_file, 'wb') as f:
                f.write(collision_data)
            
            new_hash = self.hash_func.hash(collision_data)
            differences = sum(1 for a, b in zip(original_data, collision_data) if a != b)
            if len(original_data) != len(collision_data):
                differences += abs(len(original_data) - len(collision_data))
            
            print(f"\n✓ Файл-колізія створено: {output_file}")
            print(f"Хеш нового файлу: {new_hash} ({self.hash_func.hash_to_binary(new_hash)})")
            print(f"Розмір нового файлу: {len(collision_data)} байт")
            print(f"Хеші співпадають: {original_hash == new_hash}")
            print(f"Файли відрізняються: {collision_data != original_data}")
            print(f"Кількість відмінностей: {differences} байт")
            return True
        else:
            print(f"\n✗ Не вдалося знайти колізію")
            return False


def calculate_digests():
    """Обчислює дайджести для всіх тестових файлів"""
    print("="*70)
    print("ОБЧИСЛЕННЯ ДАЙДЖЕСТІВ ПОВІДОМЛЕНЬ")
    print("="*70)
    
    # Створюємо список файлів для обробки
    files = []
    
    # Word документ (створимо як текстовий файл, оскільки створення справжнього .docx складніше)
    word_file = "test_document.txt"
    if os.path.exists(word_file):
        files.append(("Word документ", word_file))
    
    # Вихідний код
    source_file = "test_source.py"
    if os.path.exists(source_file):
        files.append(("Вихідний код", source_file))
    
    # Зображення
    image_file = "test_image.png"
    if os.path.exists(image_file):
        files.append(("Зображення", image_file))
    
    if not files:
        print("Помилка: не знайдено тестових файлів!")
        return {}
    
    results = {}
    
    # Обчислюємо хеші для різних довжин виходу
    for output_bits in [2, 4, 8]:
        print(f"\n{'='*70}")
        print(f"Хеш-функція з виходом {output_bits} біт:")
        print(f"{'='*70}")
        
        hash_func = CustomHash(output_bits=output_bits)
        results[output_bits] = {}
        
        for file_type, filepath in files:
            try:
                hash_value = hash_func.hash_file(filepath)
                binary_hash = hash_func.hash_to_binary(hash_value)
                hex_hash = hash_func.hash_to_hex(hash_value)
                
                file_size = os.path.getsize(filepath)
                
                print(f"\n{file_type}: {filepath}")
                print(f"  Розмір файлу: {file_size} байт")
                print(f"  Дайджест (десяткове): {hash_value}")
                print(f"  Дайджест (двійкове): {binary_hash}")
                print(f"  Дайджест (шістнадцяткове): {hex_hash}")
                
                results[output_bits][filepath] = {
                    'hash': hash_value,
                    'binary': binary_hash,
                    'hex': hex_hash,
                    'size': file_size
                }
            except Exception as e:
                print(f"\nПомилка при обробці {filepath}: {e}")
    
    return results


def find_collisions():
    """Знаходить колізії для тестових файлів"""
    print("\n" + "="*70)
    print("ПОШУК КОЛІЗІЙ ХЕШ-ФУНКЦІЇ")
    print("="*70)
    
    files = [
        ("test_document.txt", "test_document_collision.txt"),
        ("test_source.py", "test_source_collision.py"),
        ("test_image.png", "test_image_collision.png")
    ]
    
    for output_bits in [2, 4, 8]:
        print(f"\n{'='*70}")
        print(f"Пошук колізій для хеш-функції з виходом {output_bits} біт:")
        print(f"{'='*70}")
        
        finder = HashCollisionFinder(output_bits=output_bits)
        
        for original_file, collision_file in files:
            if os.path.exists(original_file):
                print(f"\nФайл: {original_file}")
                success = finder.create_collision_file(
                    original_file, 
                    collision_file,
                    max_attempts=100000 if output_bits <= 4 else 50000
                )
                if success:
                    print(f"✓ Колізія успішно створена")
                else:
                    print(f"✗ Не вдалося знайти колізію (спробуйте збільшити max_attempts)")
            else:
                print(f"\nФайл {original_file} не знайдено, пропускаємо...")


def main():
    """Головна функція"""
    print("\n" + "="*70)
    print("ПРОГРАМА ДЛЯ РОБОТИ З ХЕШ-ФУНКЦІЄЮ")
    print("="*70)
    
    # Крок 1: Обчислюємо дайджести
    results = calculate_digests()
    
    # Крок 2: Шукаємо колізії
    find_collisions()
    
    print("\n" + "="*70)
    print("РОБОТУ ЗАВЕРШЕНО")
    print("="*70)
    print("\nСтворені файли-колізії мають такий самий хеш, як оригінальні файли,")
    print("але відрізняються вмістом, що демонструє вразливість коротких хеш-функцій.")


if __name__ == "__main__":
    main()

