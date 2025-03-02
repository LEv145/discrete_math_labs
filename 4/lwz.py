import math


def lzw_encode(text: str) -> str:
    """Кодируем строку по алгоритму LZW."""

    output_codes = _compress_by_lzw(text)

    max_code = max(output_codes)
    bits_per_code = math.ceil(math.log2(max_code + 1))

    return "".join(f"{code:0{bits_per_code}b}" for code in output_codes)


def _compress_by_lzw(input_str: str) -> list[int]:
    """
    Реализуем алгоритм LZW для кодирования строки.

    Алгоритм:
      1. Инициализируем словарь начальными строками (один символ -> его индекс).
      2. Просматриваем входной поток, накапливая подстроку s.
      3. Если s+c содержится в словаре, s расширяется.
      4. Иначе выводим индекс s, добавляем в словарь новую строку s+c и начинаем с c.

    Возвращает список чисел.
    """
    # Инициализируем словарь: для всех уникальных символов строки
    dictionary: dict[str, int] = {}

    # Для воспроизводимости упорядочим символы
    unique_chars = sorted(set(input_str))
    for index, char in enumerate(unique_chars):
        dictionary[char] = index

    index = len(dictionary)  # Следующий номер для нового элемента словаря

    output_codes: list[int] = []
    s = ""  # Текущая обрабатываемая строка

    for c in input_str:
        s_plus = s + c
        if s_plus in dictionary:
            s = s_plus
        else:
            output_codes.append(dictionary[s])
            dictionary[s_plus] = index
            index += 1
            s = c

    # Если осталась непустая строка s, выводим её код
    if s:
        output_codes.append(dictionary[s])

    return output_codes
