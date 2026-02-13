"""Programa que calcula el total de ingresos por ventas a partir de
datos de catálogo y ventas almacenados en archivos JSON.

Author: Ali campos
"""
import sys
import time
import json


def get_catalog_sales_data(
        file_catalog: str,
        file_sales: str
) -> tuple[dict | None, dict | None]:
    """Load catalog and sales data from JSON files"""
    try:
        with open(file_catalog, "r", encoding="utf-8") as f:
            catalog_data = json.load(f)

    except FileNotFoundError:
        print(f"Error: Archivo '{file_catalog}' no encontrado.")
        return None, None
    try:
        with open(file_sales, "r", encoding="utf-8") as f:
            sales_data = json.load(f)

    except FileNotFoundError:
        print(f"Error: Archivo '{file_sales}' no encontrado.")
        return None, None
    return catalog_data, sales_data


def compute_total_sales(
        catalog_data: dict,
        sales_data: dict
) -> tuple[float, int, str]:
    """Calculate total sales revenue from catalog and sales data"""
    prices = {p["title"]: p["price"] for p in catalog_data}

    invalid_data = ""
    total = 0
    count_sales = 0

    for sale in sales_data:

        product = sale["Product"]
        quantity = sale["Quantity"]

        if not isinstance(quantity, int) or quantity <= 0:
            invalid_data += f"Cantidad inválida para '{product}': {quantity}\n"
            continue

        if not isinstance(product, str) or product not in prices:
            invalid_data += f"Producto desconocido: '{product}'\n"
            continue

        total += prices[product] * quantity
        count_sales += quantity

    return total, count_sales, invalid_data


def main():
    """Calculate total sales revenue from catalog and sales data files"""
    if len(sys.argv) != 3:
        print(
            "Error: python compute_sales.py "
            "<archivo_catalogo> <archivo_ventas>"
        )
        sys.exit(1)

    start_time = time.time()

    file_catalog = sys.argv[1]
    file_sales = sys.argv[2]

    catalog_data, sales_data = get_catalog_sales_data(file_catalog, file_sales)

    total_revenue, count_sales, invalid_data = compute_total_sales(
        catalog_data,
        sales_data
    )

    end_time = time.time()
    elapsed_time = end_time - start_time
    results = f"""
    ------
    Fecha: {time.strftime("%Y-%m-%d %H:%M:%S")}
    Tiempo de ejecución: {elapsed_time:.4f} segundos

    Total de ventas: {count_sales}
    Total de ingresos: ${total_revenue:.2f}

    Datos inválidos:\n
{invalid_data if invalid_data else "Ninguno"}
    ------
    """

    print(results)

    # Write results to file
    try:
        with open("results/SalesResults.txt", 'a', encoding='utf-8') as file:
            file.write(results)

        print("Resultados guardados en results/SalesResults.txt")

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
