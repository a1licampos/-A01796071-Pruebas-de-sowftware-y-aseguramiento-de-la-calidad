"""Exercise 2: Convert a list of integers to binary and hexadecimal representations

Author: Ali Campos"""

import sys
import time


def read_numbers_from_file(filename: str) -> list[int]:
    """Read numbers from a file, ignoring invalid lines"""
    numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    num = int(line)
                    numbers.append(num)
                except ValueError:
                    print(f"Advertencia: Línea {line_num}: '{line}' no es un núm válido (ignorado)")
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
    return numbers


def decimal_to_binary(n: int) -> str:
    """Convert a decimal integer to binary string (without sign)"""
    if n == 0:
        return "0"
    bits = ""
    while n > 0:
        bits = str(n % 2) + bits
        n //= 2
    return bits


def complement_to_2(binary: str, n_bits: int) -> str:
    """Calculate the two's complement of a binary string for n_bits"""
    # 1) Complete with zeros to n_bits
    binary = binary.zfill(n_bits)

    # 2) One's complement (invert bits)
    comp1 = ""
    for b in binary:
        comp1 += "1" if b == "0" else "0"

    # 3) Add 1
    result = list(comp1)
    carry = 1
    for i in range(len(result) - 1, -1, -1):
        suma = int(result[i]) + carry
        result[i] = str(suma % 2)
        carry = suma // 2

    return "".join(result)  # return full if no trim needed


def convert_list_to_signed_binary(lista: list[int]) -> list[str]:
    """Convert a list of integers to signed binary in two's complement"""
    # 1) Determine the number of bits needed
    max_value = max(abs(x) for x in lista)
    num_bits = len(decimal_to_binary(max_value)) + 1  # +1 for sign

    # 2) Convert each number
    result_binary = []
    for number in lista:
        if number >= 0:
            # unsigned binary
            binary = decimal_to_binary(number).zfill(num_bits)
        else:
            # binary of the positive
            binary_pos = decimal_to_binary(abs(number))
            # two's complement
            binary = complement_to_2(binary_pos, num_bits)
        result_binary.append(binary)

    return result_binary


def map_decimal_to_hexadecimal() -> dict[int, str]:
    """Create a mapping from decimal to hexadecimal characters"""
    m = dict.fromkeys(range(16), 0)
    digit = ord('0')
    c = ord('a')

    for i in range(16):
        if i < 10:
            m[i] = chr(digit)
            digit += 1
        else:
            m[i] = chr(c)
            c += 1
    return m


def decimal_to_hexadecimal(number: list[int]) -> list[str]:
    """Convert a decimal integer to hexadecimal"""
    result_hexadecimal = []
    m = map_decimal_to_hexadecimal()

    for num in number:
        result = ""

        if num == 0:
            result_hexadecimal.append("0")
            continue
        if num > 0:
            while num:
                result = m[num % 16] + result
                num //= 16
        else:
            n = num + 2**32
            while n:
                result = m[n % 16] + result
                n //= 16

        result_hexadecimal.append(result)

    return result_hexadecimal


def main():
    """Main function to read numbers, compute statistics, and print results."""
    if len(sys.argv) != 2:
        print("Error: python convert_numbers.py <archivo>")
        sys.exit(1)

    filename = sys.argv[1]
    start_time = time.time()

    numbers = read_numbers_from_file(filename)
    if not numbers:
        print("Error: No se encontraron números válidos en el archivo.")
        return
    hexadecimal_numbers = decimal_to_hexadecimal(numbers)
    binary_numbers = convert_list_to_signed_binary(numbers)

    end_time = time.time()
    elapsed_time = end_time - start_time

    results = f"""------
Fecha {time.strftime("%Y-%m-%d %H:%M:%S")}
Tiempo de ejecución: {elapsed_time:.4f} segundos
Total de números: {len(numbers)}

**Números Binarios & Hexadecimales**
\n
"""
    for n, b, h in zip(numbers, binary_numbers, hexadecimal_numbers):
        results += f"{n} -> {b} -> {h}\n"

    results += "------\n"


    print(results)

    # Write results to file
    try:
        with open("results/ConvertionResults.txt", 'a', encoding='utf-8') as file:
            file.write(results)

        print("Resultados guardados en results/ConvertionResults.txt")

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
