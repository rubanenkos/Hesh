"""
Тестовий вихідний код на Python
Це приклад програми для демонстрації хеш-функції
"""

def calculate_sum(numbers):
    """Обчислює суму чисел у списку"""
    total = 0
    for num in numbers:
        total += num
    return total

def main():
    """Головна функція програми"""
    numbers = [1, 2, 3, 4, 5, 10, 20, 30]
    result = calculate_sum(numbers)
    print(f"Сума чисел {numbers} дорівнює {result}")
    return result

if __name__ == "__main__":
    main()

