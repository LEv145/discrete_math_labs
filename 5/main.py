from typing import List, Tuple, Optional


def polynomial_modulo(dividend: int, divisor: int) -> int:
    """Вычисляет остаток от полиномиального деления по модулю 2.

    Args:
        dividend: Делимое в виде целого числа (бинарное представление коэффициентов полинома).
        divisor: Делитель в виде целого числа (бинарное представление коэффициентов полинома).

    Returns:
        Остаток от деления в виде целого числа.
    """
    while dividend.bit_length() >= divisor.bit_length():
        shift = dividend.bit_length() - divisor.bit_length()
        dividend ^= divisor << shift
    return dividend


def build_systematic_generator_matrix(n: int, k: int, generator_polynomial: str) -> List[int]:
    """Строит систематическую порождающую матрицу для циклического кода.

    Args:
        n: Длина кодового слова.
        k: Длина информационного сообщения.
        generator_polynomial: Порождающий полином в виде бинарной строки.

    Returns:
        Список кодовых слов (строк матрицы) в виде целых чисел.
    """
    generator = int(generator_polynomial, 2)
    generator_matrix = []

    for row_index in range(k):
        # Создание стандартного базисного вектора для текущей строки
        message = 1 << (k - 1 - row_index)

        # Сдвиг для получения систематической части
        shifted_message = message << (n - k)

        # Вычисление остатка от деления
        remainder = polynomial_modulo(shifted_message, generator)

        # Формирование кодового слова
        codeword = shifted_message ^ remainder
        generator_matrix.append(codeword)

    return generator_matrix


def encode_message(message: int, generator_matrix: List[int]) -> int:
    """Кодирует сообщение с использованием порождающей матрицы.

    Args:
        message: Сообщение для кодирования (целое число, представляющее k бит).
        generator_matrix: Порождающая матрица в виде списка строк-целых чисел.

    Returns:
        Закодированное сообщение (целое число, представляющее n бит).
    """
    codeword = 0
    for bit_position in range(len(generator_matrix)):
        if message & (1 << (len(generator_matrix) - 1 - bit_position)):
            codeword ^= generator_matrix[bit_position]
    return codeword


def count_set_bits(value: int) -> int:
    """Подсчитывает количество установленных битов в числе."""
    return bin(value).count("1")


def calculate_minimum_distance(codewords: List[int]) -> int:
    """Вычисляет минимальное кодовое расстояние для списка кодовых слов.

    Args:
        codewords: Список кодовых слов в виде целых чисел.

    Returns:
        Минимальное расстояние Хэмминга.
    """
    nonzero_weights = [count_set_bits(cw) for cw in codewords if cw != 0]
    return min(nonzero_weights) if nonzero_weights else 0


def int_to_binary_string(value: int, bit_length: int) -> str:
    """Конвертирует целое число в бинарную строку заданной длины."""
    return format(value, f'0{bit_length}b')


def calculate_error_capabilities(minimum_distance: int) -> Tuple[int, int]:
    """Вычисляет возможности кода по обнаружению и исправлению ошибок.

    Args:
        minimum_distance: Минимальное кодовое расстояние

    Returns:
        Кортеж (максимальная обнаруживаемая кратность, максимальная исправляемая кратность)
    """
    max_detectable = minimum_distance - 1          # Формула для обнаружения ошибок
    max_correctable = (minimum_distance - 1) // 2  # Формула для исправления ошибок
    return max_detectable, max_correctable


def is_valid_codeword(received_word: int, codewords: List[int]) -> bool:
    """Проверяет, является ли полученное слово допустимым кодовым словом."""
    return received_word in codewords


def find_closest_codeword(distorted_word: int, codewords: List[int]) -> Optional[int]:
    """Находит ближайшее кодовое слово по расстоянию Хэмминга."""
    min_distance = float('inf')
    closest = None

    for cw in codewords:
        distance = count_set_bits(distorted_word ^ cw)
        if distance < min_distance:
            min_distance = distance
            closest = cw

    return closest


def analyze_error_case(original_cw: int, received_word: int, codewords: List[int], t_correct: int, t_detect: int, CODEWORD_LENGTH: int):
    """Анализирует случай ошибки и выводит результаты проверки."""
    is_valid = is_valid_codeword(received_word, codewords)
    closest_cw = find_closest_codeword(received_word, codewords)
    error_weight = count_set_bits(original_cw ^ received_word)

    print("\nАнализ случая:")
    print(f"  Вес ошибки: {error_weight}")
    print(f"  Полученное слово {'ВАЛИДНО' if is_valid else 'НЕВАЛИДНО'}")
    print(f"  Ближайшее кодовое слово: {int_to_binary_string(closest_cw, CODEWORD_LENGTH)}")

    # Логика проверки
    if error_weight <= t_correct:
        status = "УСПЕШНО ИСПРАВЛЕНО" if closest_cw == original_cw else "ОШИБКА ИСПРАВЛЕНИЯ"
        print(f"  Результат: {status} (ошибка в пределах исправляемой способности)")
    elif error_weight <= t_detect:
        print(f"  Результат: ОШИБКА ОБНАРУЖЕНА (вес ошибки в пределах обнаруживающей способности)")
    else:
        print(f"  Результат: НЕ ОБНАРУЖЕНА (превышена обнаруживающая способность)")


def main() -> None:
    # Параметры кода
    CODEWORD_LENGTH = 23
    MESSAGE_LENGTH = 12
    GENERATOR_POLYNOMIAL = "101011100011"

    print("Основные характеристики кода:")
    print(f"Длина кодового слова (n): {CODEWORD_LENGTH} бит")
    print(f"Длина сообщения (k): {MESSAGE_LENGTH} бит")
    print(f"Избыточность: {CODEWORD_LENGTH - MESSAGE_LENGTH} бит")

    # Построение порождающей матрицы
    generator_matrix = build_systematic_generator_matrix(
        n=CODEWORD_LENGTH,
        k=MESSAGE_LENGTH,
        generator_polynomial=GENERATOR_POLYNOMIAL
    )

    # Вывод матрицы
    print()
    print(f"Систематическая порождающая матрица G ({MESSAGE_LENGTH} строк по {CODEWORD_LENGTH} бит):")
    for index, row in enumerate(generator_matrix):
        binary_row = int_to_binary_string(row, CODEWORD_LENGTH)
        print(f"Строка {index:2d}: {binary_row}")

    # Генерация всех кодовых слов
    all_codewords = [encode_message(msg, generator_matrix) for msg in range(1 << MESSAGE_LENGTH)]

    # Вывод примеров кодовых слов
    print()
    print("Первые 10 кодовых слов:")
    for i in range(10):
        msg_bits = int_to_binary_string(i, MESSAGE_LENGTH)
        cw_bits = int_to_binary_string(all_codewords[i], CODEWORD_LENGTH)
        print(f"Сообщение {msg_bits} → Кодовое слово {cw_bits}")

    min_distance = calculate_minimum_distance(all_codewords)

    print()
    print(f"Минимальное расстояние (d): {min_distance}")

    t_detect, t_correct = calculate_error_capabilities(min_distance)
    print()
    print(f"Гарантированно обнаруживает до {t_detect} ошибок в кодовом слове")
    print(f"Гарантированно исправляет до {t_correct} ошибок в кодовом слове")

    # Пример 1: Ошибка весом 2 (исправляется)
    m_example = 1  # 000000000001 (12 бит)
    cw_example = encode_message(m_example, generator_matrix)

    # Создаем ошибку в битах 5 и 17 (нумерация слева направо)
    error_vector_2 = (1 << (CODEWORD_LENGTH - 1 - 5)) ^ (1 << (CODEWORD_LENGTH - 1 - 17))
    received_word_2 = cw_example ^ error_vector_2

    print()
    print("Пример 1: Ошибка весом 2")
    print(f"Исходное сообщение: {int_to_binary_string(m_example, MESSAGE_LENGTH)}")
    print(f"Кодовое слово:      {int_to_binary_string(cw_example, CODEWORD_LENGTH)}")
    print(f"Вектор ошибки:      {int_to_binary_string(error_vector_2, CODEWORD_LENGTH)}")
    analyze_error_case(cw_example, received_word_2, all_codewords, t_correct, t_detect, CODEWORD_LENGTH)

    # Пример 2: Ошибка весом 4 (обнаруживается, но не исправляется)
    error_vector_4 = int("11110000000000000000000", 2)  # Первые 4 бита
    received_word_4 = cw_example ^ error_vector_4

    print("\nПример 2: Ошибка весом 4")
    print(f"Исходное сообщение: {int_to_binary_string(m_example, MESSAGE_LENGTH)}")
    print(f"Кодовое слово:      {int_to_binary_string(cw_example, CODEWORD_LENGTH)}")
    print(f"Вектор ошибки:      {int_to_binary_string(error_vector_4, CODEWORD_LENGTH)}")
    analyze_error_case(cw_example, received_word_4, all_codewords, t_correct, t_detect, CODEWORD_LENGTH)

    # Пример 3: Ошибка весом 7 (превышает обнаруживающую способность)
    error_vector_7 = int("11111110000000000000000", 2)  # Первые 7 бит
    received_word_7 = cw_example ^ error_vector_7

    print("\nПример 3: Ошибка весом 7")
    print(f"Исходное сообщение: {int_to_binary_string(m_example, MESSAGE_LENGTH)}")
    print(f"Кодовое слово:      {int_to_binary_string(cw_example, CODEWORD_LENGTH)}")
    print(f"Вектор ошибки:      {int_to_binary_string(error_vector_7, CODEWORD_LENGTH)}")
    analyze_error_case(cw_example, received_word_7, all_codewords, t_correct, t_detect, CODEWORD_LENGTH)


if __name__ == "__main__":
    main()
