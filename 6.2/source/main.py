"""Text"""
import os
import csv
from crud_hotel_customer import CRUDSystemHotelCustomer

def print_line_break() -> None:
    """Print linre break to show info."""
    print("\n\n")


def create_csv_hotel_customers_info(folder_tests:str) -> None:
    """Create a file hotel and customers csv."""
    print("[create_csv_hotel_customers_info]")

    path_hotel = os.path.join(folder_tests, "hotel.csv")

    if not os.path.exists(path_hotel):
        with open(path_hotel, mode="w", newline="", encoding="utf-8") as file_hotel:
            writer = csv.writer(file_hotel)
            writer.writerow(["Nombre", "No_estrellas", "Precio_por_noche"])
        print("\tArchivo hotel.csv creado correctament")
    else:
        print("\thotel.csv ya existe")

    path_customers = os.path.join(folder_tests, "customers.csv")

    if not os.path.exists(path_customers):
        with open(path_customers, mode="w", newline="", encoding="utf-8") as file_customers:
            writer = csv.writer(file_customers)
            writer.writerow(["Nombre", "Apellido", "Telefono"])
        print("\tArchivo clientes.csv creado correctament")
    else:
        print("\tclientes.csv ya existe")

    print_line_break()


def main():
    """Text."""
    print("--- --- ---")
    create_csv_hotel_customers_info(os.path.join("tests"))

    crud_hotel = CRUDSystemHotelCustomer(1)
    crud_hotel.set_information("kimba", 5, 99.99)

    # Necesitaria revisar que los datos son adecuados (tamaño phone, test, name)
    crud_customers = CRUDSystemHotelCustomer(0)
    crud_customers.set_information(c_name="Mady",
                                   c_last_name="Campos",
                                   c_phone=4423427014)

if __name__ == '__main__':
    main()

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba
