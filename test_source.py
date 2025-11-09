"""
Приклад програми
"""

def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def main():
    numbers = [1, 2, 3, 4, 5, 10, 60 30]
    result = calculate_sum(numbers)
    print(f"Сума чисел {numbers} дорівнює {result}")
    return result

if __name__ == "__main__":
    main()

