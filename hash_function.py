"""
Хеш-функція з виходом 2, 4 або 8 біт
З властивістю лавинного ефекту (зміна будь-якого байту змінює не менше 30% бітів результату)
"""

import hashlib


class CustomHash:
    """Власна хеш-функція з налаштовуваною довжиною виходу"""
    
    def __init__(self, output_bits=8):
        """
        Ініціалізація хеш-функції
        
        Args:
            output_bits: довжина виходу в бітах (2, 4 або 8)
        """
        if output_bits not in [2, 4, 8]:
            raise ValueError("output_bits повинен бути 2, 4 або 8")
        self.output_bits = output_bits
        self.max_value = (1 << output_bits) - 1
        
    def hash(self, data):
        """
        Обчислює хеш-значення для даних
        
        Args:
            data: байти для хешування
            
        Returns:
            хеш-значення (0 до max_value)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if len(data) == 0:
            return 0
        
        # Ініціалізація змінних для лавинного ефекту
        hash_value = 0x5A5A5A5A  # Початкове значення
        state = [0x12345678, 0x9ABCDEF0, 0xFEDCBA09, 0x87654321]
        
        # Обробка кожного байту з множинними проходами для кращого перемішування
        for byte in data:
            # Крок 1: XOR з поточним станом
            hash_value ^= byte
            hash_value ^= (hash_value << 7) | (hash_value >> 25)
            
            # Крок 2: Множення з великим простим числом
            hash_value = (hash_value * 0x9E3779B9) & 0xFFFFFFFF
            
            # Крок 3: Циклічний зсув
            hash_value = ((hash_value << 13) | (hash_value >> 19)) & 0xFFFFFFFF
            
            # Крок 4: Взаємодія зі станом
            state[byte % 4] ^= hash_value
            state[byte % 4] = ((state[byte % 4] << 5) | (state[byte % 4] >> 27)) & 0xFFFFFFFF
            hash_value ^= state[byte % 4]
            
            # Крок 5: Додаткове перемішування
            hash_value ^= (hash_value << 3)
            hash_value ^= (hash_value >> 11)
            hash_value ^= (hash_value << 15)
            hash_value = hash_value & 0xFFFFFFFF
        
        # Фінальне перемішування
        for s in state:
            hash_value ^= s
            hash_value = ((hash_value << 7) | (hash_value >> 25)) & 0xFFFFFFFF
        
        # Взяття модуля для отримання потрібної кількості бітів
        result = hash_value & self.max_value
        
        return result
    
    def hash_file(self, filepath):
        """
        Обчислює хеш-значення для файлу
        
        Args:
            filepath: шлях до файлу
            
        Returns:
            хеш-значення
        """
        with open(filepath, 'rb') as f:
            data = f.read()
        return self.hash(data)
    
    def hash_to_binary(self, hash_value):
        """
        Конвертує хеш-значення в двійковий рядок
        
        Args:
            hash_value: хеш-значення
            
        Returns:
            двійковий рядок
        """
        return format(hash_value, f'0{self.output_bits}b')
    
    def hash_to_hex(self, hash_value):
        """
        Конвертує хеш-значення в шістнадцятковий рядок
        
        Args:
            hash_value: хеш-значення
            
        Returns:
            шістнадцятковий рядок
        """
        if self.output_bits >= 4:
            width = self.output_bits // 4
            return format(hash_value, f'0{width}x')
        else:
            return format(hash_value, '01x')


def test_avalanche_effect(hash_func, test_data, num_tests=100):
    """
    Тестує лавинний ефект хеш-функції
    
    Args:
        hash_func: функція хешування
        test_data: тестові дані
        num_tests: кількість тестів
        
    Returns:
        середній відсоток змінених бітів
    """
    import random
    
    original_hash = hash_func.hash(test_data)
    original_bits = hash_func.hash_to_binary(original_hash)
    
    changed_bits_count = []
    
    for _ in range(num_tests):
        # Створюємо копію даних
        modified_data = bytearray(test_data)
        
        # Змінюємо один випадковий байт
        if len(modified_data) > 0:
            pos = random.randint(0, len(modified_data) - 1)
            modified_data[pos] = (modified_data[pos] + 1) % 256
        
        # Обчислюємо новий хеш
        new_hash = hash_func.hash(bytes(modified_data))
        new_bits = hash_func.hash_to_binary(new_hash)
        
        # Підраховуємо змінені біти
        changed = sum(1 for a, b in zip(original_bits, new_bits) if a != b)
        changed_bits_count.append(changed)
    
    avg_changed = sum(changed_bits_count) / len(changed_bits_count)
    percentage = (avg_changed / hash_func.output_bits) * 100
    
    return percentage, changed_bits_count


if __name__ == "__main__":
    # Тестування хеш-функції
    print("Тестування хеш-функції з різними довжинами виходу:\n")
    
    test_string = "Hello, World! This is a test message for hash function."
    test_bytes = test_string.encode('utf-8')
    
    for bits in [2, 4, 8]:
        print(f"\n{'='*50}")
        print(f"Хеш-функція з виходом {bits} біт:")
        print(f"{'='*50}")
        
        hash_func = CustomHash(output_bits=bits)
        hash_value = hash_func.hash(test_bytes)
        
        print(f"Вхідні дані: {test_string[:50]}...")
        print(f"Хеш-значення (десяткове): {hash_value}")
        print(f"Хеш-значення (двійкове): {hash_func.hash_to_binary(hash_value)}")
        print(f"Хеш-значення (шістнадцяткове): {hash_func.hash_to_hex(hash_value)}")
        
        # Тест лавинного ефекту
        percentage, _ = test_avalanche_effect(hash_func, test_bytes, num_tests=100)
        print(f"Середній відсоток змінених бітів при зміні одного байту: {percentage:.2f}%")
        
        if percentage >= 30:
            print("✓ Лавинний ефект задовольняє вимогам (≥30%)")
        else:
            print("✗ Лавинний ефект не задовольняє вимогам (<30%)")

