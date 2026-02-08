"""Exercise to compute basic statistics 
(mean, median, mode, variance, std deviation) from a file of numbers

Author: Ali Campos"""

import sys
import time

def read_numbers_from_file(filename: str) -> list[float]:
    """Read numbers from a file, ignoring invalid lines"""
    numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    num = float(line)
                    numbers.append(num)
                except ValueError:
                    print(f"Advertencia: Línea {line_num}: '{line}' no es un núm válido (ignorado)")
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
    return numbers


def calculate_mean(numbers: list[float]) -> float:
    """Calculate the mean of a list of numbers"""
    if not numbers:
        return 0.0
    total_sum_numbers = 0

    for num in numbers:
        total_sum_numbers += num
    return total_sum_numbers / len(numbers)


def calculate_median(numbers: list[float]) -> float:
    """Calculate the median of a list of numbers"""
    if not numbers:
        return 0.0
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 0:
        index = int(n / 2)
        return (sorted_nums[index - 1] + sorted_nums[index]) / 2
    index = int((n + 1) / 2)
    return sorted_nums[index]


def calculate_mode(numbers: list[float]) -> float | list[float] | None:
    """Calculate the mode of a list of numbers"""
    if not numbers:
        return None

    frequency = {}
    for n in numbers:
        frequency[n] = frequency[n] + 1 if n in frequency else 1

    # Found max frequency
    max_freq = 0
    for f in frequency.values():
        max_freq = max(max_freq, f)

    if max_freq == 1:
        return None  # No mode if all numbers are unique
    # Collect numbers with that frequency
    modes = []
    for n in frequency.items():
        if n == max_freq:
            modes.append(n)

    # Return first if unique, list if multiple
    if len(modes) == 1:
        return modes[0]
    return modes


def calculate_variance(numbers: list[float], mean: float) -> float:
    """Calculate the sample variance of a list of numbers"""
    if len(numbers) < 2:
        return 0.0
    total_sum_numbers = 0

    for x in numbers:
        total_sum_numbers += (x - mean) ** 2

    return total_sum_numbers / (len(numbers) - 1)


def sqrt_scratch(x: float, tolerance: float = 1e-10) -> float | None:
    """Calculate the square root of a number using Newton's method"""
    if x < 0:
        return None  # No negative numbers
    if x == 0:
        return 0

    # Initial estimation
    guess = x / 2

    while True:
        # Better guess using Newton's method
        new_guess = (guess + x / guess) / 2
        # Check for convergence
        if abs(new_guess - guess) < tolerance:
            return new_guess
        guess = new_guess


def calculate_std_dev(variance: float) -> float | None:
    """Calculate the standard deviation from the variance"""
    # It could be math.sqrt(variance)
    return sqrt_scratch(variance)


def main():
    """Main function to read numbers, compute statistics, and print results."""
    if len(sys.argv) != 2:
        print("Error: python compute_statistics.py <archivo>")
        sys.exit(1)

    filename = sys.argv[1]
    start_time = time.time()

    numbers = read_numbers_from_file(filename)
    if not numbers:
        print("Error: No se encontraron números válidos en el archivo.")
        return

    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers)
    variance = calculate_variance(numbers, mean)
    std_dev = calculate_std_dev(variance)

    end_time = time.time()
    elapsed_time = end_time - start_time

    results = f"""
    ------
    Fecha {time.strftime("%Y-%m-%d %H:%M:%S")}

    **Estadísticas Descriptivas**
    Total de números: {len(numbers)}
    Media: {mean:.2f}
    Mediana: {median:.2f}
    Moda: {mode}
    Varianza: {variance:.2f}
    Desviación Estándar: {std_dev:.2f}

    Tiempo transcurrido: {elapsed_time:.4f} segundos
    ------
    """

    print(results)

    # Write results to file
    try:
        with open("results/StatisticsResults.txt", 'a', encoding='utf-8') as file:
            file.write(results)

        print("Resultados guardados en results/StatisticsResults.txt")

    except FileNotFoundError as e:
        print(f"No se encontró el archivo: {e}")


if __name__ == "__main__":
    main()
