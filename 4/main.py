from math import log2
from collections import Counter

from huffman_codes import compress_by_huffman_codes


def collect_letter_frequencies(text: str) -> dict[str, int]:
    counter = Counter(text)

    frequencies = {}
    for key, value in counter.items():
        frequencies[key] = value

    return frequencies


def collect_pairs_frequencies(text: str) -> dict[str, int]:
    pairs = [text[i] + text[i+1] for i in range(len(text) - 1)]
    counter = Counter(pairs)

    frequencies = {}
    for key, value in counter.items():
        frequencies[key] = value

    return frequencies



def main() -> None:
    with open("text.txt") as fp:
        text = fp.read()
    n = len(text)

    letter_freq = collect_letter_frequencies(text)
    #data_2 = collect_pairs_frequencies(text)

    huffman_codes = compress_by_huffman_codes(letter_freq)

    print("# Подсчёт бит")

    # Общее число бит при кодировании Хаффмана:
    huffman_total_bits = sum(letter_freq[char] * len(huffman_codes[char]) for char in letter_freq)
    # Равномерное кодирование (6 бит на символ)
    uniform_total_bits = n * 6

    print(f"Количество бит до сжатия: {uniform_total_bits}")
    print(f"Количество бит после сжатия: {huffman_total_bits}")
    print(f"Степень сжатия: ≈{huffman_total_bits / uniform_total_bits:.5%}")
    print(f"Коэффициент сжатия: ≈{uniform_total_bits / huffman_total_bits:.5}")

    print("# Вычисление энтропии по формуле Шеннона")

    # Количество информации на символ I = sum(p * log2(1/p)) = -sum(p * log2(p))
    entropy = -sum((freq/n) * log2(freq/n) for freq in letter_freq.values())
    shannon_total_bits = n * entropy
    print(f"Количество информации по формуле Шеннона: {shannon_total_bits}")
    print(f"Количество бит после сжатия: {huffman_total_bits}")
    print(f"Разница: {huffman_total_bits - shannon_total_bits}")


if __name__ == "__main__":
    main()
