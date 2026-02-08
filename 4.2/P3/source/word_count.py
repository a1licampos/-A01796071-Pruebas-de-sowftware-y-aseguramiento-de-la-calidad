"""Exercise 3: Word Count with File Output
Author: Ali Campos"""

import sys
import time


def read_words_from_file(filename: str) -> list[str]:
    """Read words from a file, ignoring invalid lines"""
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    # print(line)
                    words.append(line)
                except ValueError:
                    print(f"Advertencia: Línea {line_num}: '{line}' palabra inválida (ignorado)")
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
    return words


def count_unique_words(words: list[str]) -> tuple[list[str], list[int]]:
    """Count total and unique words in the list"""

    words_frecuency = []
    words_counted = []
    index = -1

    for n, _ in enumerate(words):
        first_word = False
        # print("n es igual a:", n)
        # print(words_frecuency)
        # print("\n\n")

        for word in words:
            if word == words[n] and words[n] not in words_counted:
                # print("Misma palabra:", words[n])

                if not first_word:
                    # print("Primera vez que se encuentra la palabra:", words[n])
                    index += 1
                    words_frecuency = words_frecuency + [1]
                    first_word = True
                else:
                    # print(f"segunda vez ({n})")
                    words_frecuency[index] += 1

        if words[n] not in words_counted:
            words_counted.append(words[n])
        # print("Palabras contadas:", words_counted)

    # print(words_frecuency)

    return words_counted, words_frecuency


def count_num_total_words(frequency: list[int]) -> int:
    """Count total number of words from the frequency list"""
    total = 0
    for f in frequency:
        total += f
    return total


def print_results(words: list[str], frequency: list[int]) -> str:
    """Format the results as a string for output"""
    results = "Palabra\t\tFrecuencia\n"
    for word, freq in zip(words, frequency):
        results += f"{word}\t\t{freq}\n"
    return results


def main():
    """Main function to read numbers, compute statistics, and print results."""
    if len(sys.argv) != 2:
        print("Error: python word_count.py <archivo>")
        sys.exit(1)

    filename = sys.argv[1]
    start_time = time.time()

    words = read_words_from_file(filename)
    unique_words, words_frequency = count_unique_words(words)
    word_count = count_num_total_words(words_frequency)
    end_time = time.time()
    elapsed_time = end_time - start_time

    results = f"""
------
Fecha {time.strftime("%Y-%m-%d %H:%M:%S")}

**Datos**
Total de palabras: {word_count}
Tiempo transcurrido: {elapsed_time:.4f} segundos

"""
    results += print_results(unique_words, words_frequency)
    results += "------\n\n"

    print(results)

    # Write results to file
    try:
        with open("results/WordCountResults.txt", 'a', encoding='utf-8') as file:
            file.write(results)

        print("Resultados guardados en results/WordCountResults.txt")

    except FileNotFoundError as e:
        print(f"No se encontró el archivo: {e}")

if __name__ == '__main__':
    main()

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba
