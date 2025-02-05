import math
from itertools import permutations


def count_unique_words_itertools(word: str, word_length: int) -> int:
    all_perms = permutations(word, word_length)

    unique_words = set(all_perms)

    return len(unique_words)


def count_unique_words_math() -> int:
    # Количество каждой буквы в слове КОМБИНАТОРИКА
    # Буквы с двумя повторениями: К, О, И, А (4 буквы)
    # Остальные буквы: М, Б, Н, Т, Р (5 букв), всего 9 уникальных букв

    # Случай 1: Все 4 буквы разные (Выбираем 4 из 9 уникальных букв и переставляем их всеми способами)
    case1 = math.comb(9, 4) * math.factorial(4)

    # Случай 2: Одна пара и две уникальные буквы (Выбираем букву для пары (4 варианта), затем 2 из оставшихся 8 букв)
    case2 = 4 * math.comb(8, 2) * (math.factorial(4) // 2)

    # Случай 3: Две пары (Выбираем 2 буквы из 4 возможных для пар)
    case3 = math.comb(4, 2) * (math.factorial(4) // (2 * 2))

    return case1 + case2 + case3


def main() -> None:
    word = "КОМБИНАТОРИКА"
    word_length = 4

    unique_word_count = count_unique_words_itertools(word, word_length)
    print(f"Количество различных 4-буквенных слов: {unique_word_count}")

    unique_word_count = count_unique_words_math()
    print(f"Количество различных 4-буквенных слов: {unique_word_count}")


if __name__ == "__main__":
    main()
