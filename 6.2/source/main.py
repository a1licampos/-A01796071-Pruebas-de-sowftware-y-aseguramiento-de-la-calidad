"""Text"""
import os
import csv
import math
from crud_hotel_customer import CRUDSystemHotelCustomer
from crud_reservation import SystemReservation

CRUD_HOTEL = CRUDSystemHotelCustomer(1)
CRUD_CUSTOMERS = CRUDSystemHotelCustomer(0)
CD_RESERVATIONS = SystemReservation()


def print_line_break() -> None:
    """Print linre break to show info."""
    print("\n\n /")


def create_csv_hotel_customers_info(folder_tests: str) -> None:
    """Create a file hotel and customers csv."""
    print("[create_csv_hotel_customers_info]")

    path_hotel = os.path.join(folder_tests, "hotel.csv")

    if not os.path.exists(path_hotel):
        with open(path_hotel,
                  mode="w",
                  newline="",
                  encoding="utf-8") as file_hotel:
            writer = csv.writer(file_hotel)
            writer.writerow(["Nombre", "No_estrellas", "Precio_por_noche"])
        print("\tArchivo hotel.csv creado correctamente")
    else:
        print("\thotel.csv ya existe")

    path_customers = os.path.join(folder_tests, "customers.csv")

    if not os.path.exists(path_customers):
        with open(path_customers,
                  mode="w",
                  newline="",
                  encoding="utf-8") as file_customers:
            writer = csv.writer(file_customers)
            writer.writerow(["Nombre", "Apellido", "Telefono"])
        print("\tArchivo clientes.csv creado correctamente")
    else:
        print("\tclientes.csv ya existe")

    path_customers = os.path.join(folder_tests, "reservations.csv")

    if not os.path.exists(path_customers):
        with open(path_customers,
                  mode="w",
                  newline="",
                  encoding="utf-8") as file_customers:
            writer = csv.writer(file_customers)
            writer.writerow(["Hotel_nombre",
                             "Cliente_telefono",
                             "Estatus",
                             "No_habitacion",
                             "No_noches",
                             "Total_precio"])
        print("\tArchivo reservations.csv creado correctamente")
    else:
        print("\teservations.csv ya existe")

    print_line_break()


def valid_phone() -> int:
    """Get an 10 phone digit."""
    while True:
        tel = int(input("TELÉFONO (10 dígitos): "))
        if int(math.log10(tel)) + 1 == 10:
            return int(tel)
        print("ERROR: Debe ser un número de 10 dígitos.")


def valid_price() -> float:
    """Get a price float > 0."""
    while True:
        try:
            precio = float(input("PRECIO POR NOCHE > 0: "))
            if precio > 0:
                return precio
            print("ERROR: El precio debe ser mayor que 0.")
        except ValueError:
            print("ERROR: Ingresa un número válido.")


def valid_hotel_stars() -> int:
    """Get a stars number int > 0."""
    while True:
        try:
            stars = int(input("Estrellas del hotel: "))
            if 0 < stars < 6:
                return stars
            print("ERROR: No estrellas debe ser mayor a 0 y menor a 6.")
        except ValueError:
            print("ERROR: Ingresa un número válido.")


def upper_text(texto: str) -> str:
    """Upper text."""
    return texto.strip().upper()


# --- Principals functions ---
def set_hotel():
    """Add hotel to db."""
    name = upper_text(input("Nombre del hotel: "))
    stars = valid_hotel_stars()
    price = valid_price()
    CRUD_HOTEL.set_register(h_name=name,
                            h_no_stars=stars,
                            h_price_per_night=price)


def set_customer():
    """Add customer to db."""
    name = upper_text(input("Nombre del cliente: "))
    last_name = upper_text(input("Apellido: "))
    phone = valid_phone()
    CRUD_CUSTOMERS.set_register(c_name=name,
                                c_last_name=last_name,
                                c_phone=phone)


def delete_hotel():
    """Delete hotel from db."""
    name = upper_text(input("Nombre del hotel a eliminar: "))
    CRUD_HOTEL.delete_register(h_name=name)


def delete_customer():
    """Delete customer from db."""
    phone = valid_phone()
    CRUD_CUSTOMERS.delete_register(c_phone=phone)


def get_hotel():
    """Get hotel info from db."""
    name = upper_text(input("Nombre del hotel: "))
    print(CRUD_HOTEL.get_register(h_name=name))


def get_customer():
    """Get customer info from db."""
    phone = valid_phone()
    print(CRUD_CUSTOMERS.get_register(c_phone=phone))


def update_hotel():
    """Update hotel info into db."""
    name = upper_text(input("Nombre del hotel a modificar info: "))
    new_name = None
    stars = None
    price = None

    print("Quieres modificar el nombre del hotel?")
    elec = input("Y/N: ").upper()
    if elec == "Y":
        new_name = upper_text(input("Nuevo nombre del hotel: "))

    print("Quieres modificar las estrellas del hotel?")
    elec = input("Y/N: ").upper()
    if elec == "Y":
        stars = valid_hotel_stars()

    print("Quieres modificar el precio por noche del hotel?")
    elec = input("Y/N: ").upper()
    if elec == "Y":
        price = valid_price()

    CRUD_HOTEL.update_register(h_name=name,
                               h_no_stars=stars,
                               h_price_per_night=price,
                               h_new_name=new_name)

    if new_name is not None:
        print(CRUD_HOTEL.get_register(h_name=new_name))
    else:
        print(CRUD_HOTEL.get_register(h_name=name))


def update_customer():
    """Update customer info into db."""
    print("Telefono del cliente que se van a modificar los datos")
    phone = valid_phone()
    name = None
    last_name = None
    new_phone = None

    print("Quieres modificar el nombre del cliente")
    elec = input("Y/N: ").upper()
    if elec == "Y":
        name = upper_text(input("Nombre del cliente: "))

    print("Quieres modificar el apellido del cliente")
    elec = input("Y/N: ").upper()
    if elec == "Y":
        last_name = upper_text(input("Apellido: "))

    print("Quieres modificar el telefono del cliente")
    elec = input("Y/N: ").upper()
    if elec == "Y":
        new_phone = valid_phone()

    CRUD_CUSTOMERS.update_register(c_phone=phone,
                                   c_name=name,
                                   c_last_name=last_name,
                                   c_new_phone=new_phone)

    if new_phone is not None:
        print(CRUD_CUSTOMERS.get_register(c_phone=new_phone))
    else:
        print(CRUD_CUSTOMERS.get_register(c_phone=phone))


def create_reservation():
    """Create reservation into db."""
    no_room = int(input("No de habitación: "))
    no_nights = int(input("No de noches: "))
    name = upper_text(input("Nombre del hotel: "))
    print("Telefono del cliente: ")
    phone = valid_phone()

    if CRUD_HOTEL.check_no_duplicates(h_name=name):

        if CRUD_CUSTOMERS.check_no_duplicates(c_phone=phone):

            CD_RESERVATIONS.create_reservation(no_room=no_room,
                                               no_nights=no_nights,
                                               h_name=name,
                                               c_phone=phone)
        else:
            print("[Creando reservación] No existe el cliente")
    else:
        print("[Creando reservación] No existe el hotel")


def cancel_reservation():
    """Cancel reservation into db."""
    name = upper_text(input("Nombre del hotel: "))
    print("Telefono del cliente: ")
    phone = valid_phone()

    if CRUD_HOTEL.check_no_duplicates(h_name=name):

        if CRUD_CUSTOMERS.check_no_duplicates(c_phone=phone):

            CD_RESERVATIONS.cancel_reservation(h_name=name,
                                               c_phone=phone)
        else:
            print("[Cancelando reservación] No existe el cliente")
    else:
        print("[Cancelando reservación] No existe el hotel")


def show_reservations():
    """Show all the reservations into db."""
    print(CD_RESERVATIONS.show_reservations())


def main():
    """Main function to use CRUD program and create reservations"""
    print("--- --- ---")
    create_csv_hotel_customers_info(os.path.join("tests"))


def menu():
    """Menu to select actions."""
    opciones = {
        "1": ("SET hotel", set_hotel),
        "2": ("DELETE hotel", delete_hotel),
        "3": ("GET hotel", get_hotel),
        "4": ("UPDATE hotel", update_hotel),
        "5": ("SET cliente", set_customer),
        "6": ("DELETE cliente", delete_customer),
        "7": ("GET cliente", get_customer),
        "8": ("UPDATE cliente", update_customer),
        "9": ("Crear reservación", create_reservation),
        "10": ("Cancelar reservación", cancel_reservation),
        "V": ("Ver reservaciones", show_reservations()),
        "E": ("Salir", None)
    }

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        for clave, (texto, _) in opciones.items():
            print(f"{clave}. {texto}")
        elec = input("Elige una opción (e para salir): ").upper()

        if elec == "E":
            print("Saliendo...")
            break

        if elec in opciones:
            func = opciones[elec][1]
            if func:
                func()
        else:
            print("Opción inválida.")


if __name__ == '__main__':
    main()
    menu()

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba
