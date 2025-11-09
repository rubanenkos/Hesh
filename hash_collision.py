"""
Програма для автоматичного пошуку колізій хеш-функції
"""

import random
from hash_function import CustomHash


class HashCollisionFinder:
    """Клас для пошуку колізій хеш-функції"""
    
    def __init__(self, output_bits=8):
        """
        Ініціалізація
        
        Args:
            output_bits: довжина виходу хеш-функції (2, 4 або 8)
        """
        self.hash_func = CustomHash(output_bits=output_bits)
        self.output_bits = output_bits
        self.max_value = (1 << output_bits) - 1
    
    def find_collision_smart(self, original_data, max_attempts=100000):
        """
        Розумний пошук колізії з використанням різних стратегій
        
        Args:
            original_data: оригінальні дані
            max_attempts: максимальна кількість спроб
            
        Returns:
            модифіковані дані з таким самим хешем або None
        """
        target_hash = self.hash_func.hash(original_data)
        print(f"Цільове хеш-значення: {target_hash} ({self.hash_func.hash_to_binary(target_hash)})")
        
        print(f"Пошук колізії (розумний алгоритм)...")
        
        for attempt in range(max_attempts):
            if attempt % 10000 == 0 and attempt > 0:
                print(f"Спроба {attempt}/{max_attempts}...")
            
            # Стратегія: Випадкові зміни в різних позиціях
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
            
            # Перевірка на точну колізію (і що дані відрізняються від оригіналу)
            if hash_value == target_hash and bytes(test_data) != original_data:
                print(f"\n✓ Колізія знайдена за {attempt + 1} спроб!")
                return bytes(test_data)
        
        print(f"\n✗ Точна колізія не знайдена за {max_attempts} спроб")
        return None
    
    def create_collision_file(self, original_file, output_file, max_attempts=100000):
        """
        Створює файл-колізію для заданого файлу
        
        Args:
            original_file: шлях до оригінального файлу
            output_file: шлях для збереження файлу-колізії
            max_attempts: максимальна кількість спроб
            
        Returns:
            True якщо колізія знайдена, False інакше
        """
        print(f"\n{'='*60}")
        print(f"Створення колізії для файлу: {original_file}")
        print(f"{'='*60}")
        
        # Читаємо оригінальний файл
        with open(original_file, 'rb') as f:
            original_data = f.read()
        
        original_hash = self.hash_func.hash(original_data)
        print(f"Оригінальний хеш: {original_hash} ({self.hash_func.hash_to_binary(original_hash)})")
        print(f"Розмір файлу: {len(original_data)} байт")
        
        # Шукаємо колізію
        collision_data = self.find_collision_smart(original_data, max_attempts)
        
        if collision_data and collision_data != original_data:
            # Зберігаємо файл-колізію
            with open(output_file, 'wb') as f:
                f.write(collision_data)
            
            # Перевіряємо хеш нового файлу
            new_hash = self.hash_func.hash(collision_data)
            
            # Знаходимо відмінності
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
