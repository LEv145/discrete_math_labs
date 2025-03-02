from math import log2
from collections import Counter

from huffman_codes import huffman_encode
from lwz import lzw_encode


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
    pairs_freq = collect_pairs_frequencies(text)

    print("# Частоты\n")

    print("Частоты символов:", letter_freq)
    print("Частоты пар:", pairs_freq)

    huffman_code = huffman_encode(text, letter_freq)
    lzw_code = lzw_encode(text)

    huffman_total_bits = len(huffman_code)
    lzw_code_total_bits = len(lzw_code)
    uniform_total_bits = n * 6

    print("\n# Подсчёт бит\n")
    print("## Сжатие по Хаффману\n")

    print(f"Количество бит до сжатия: {uniform_total_bits}")
    print(f"Количество бит после сжатия по Хаффману: {huffman_total_bits}")
    print(f"Степень сжатия: ≈{huffman_total_bits / uniform_total_bits:.5%}")
    print(f"Коэффициент сжатия: ≈{uniform_total_bits / huffman_total_bits:.5}")

    print("\n## Сжатие LZW\n")

    print(f"Количество бит до сжатия: {uniform_total_bits}")
    print(f"Количество бит после сжатия LZW: {lzw_code_total_bits}")
    print(f"Степень сжатия: ≈{lzw_code_total_bits / uniform_total_bits:.5%}")
    print(f"Коэффициент сжатия: ≈{uniform_total_bits / lzw_code_total_bits:.5}")

    print("\n# Вычисление энтропии по формуле Шеннона\n")

    # Количество информации на символ I = sum(p * log2(1/p)) = -sum(p * log2(p))
    entropy = -sum((freq/n) * log2(freq/n) for freq in letter_freq.values())
    shannon_total_bits = n * entropy

    print(f"Количество информации по формуле Шеннона: {shannon_total_bits}")
    print(f"Количество бит после сжатия по Хаффману: {huffman_total_bits}")
    print(f"Количество бит после сжатия LZW: {huffman_total_bits}")


if __name__ == "__main__":
    main()
