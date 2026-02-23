"""Text"""
import os
import csv
from crud_hotel_customer import CRUDSystemHotelCustomer
from crud_reservation import SystemReservation

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
        print("\tArchivo hotel.csv creado correctamente")
    else:
        print("\thotel.csv ya existe")

    path_customers = os.path.join(folder_tests, "customers.csv")

    if not os.path.exists(path_customers):
        with open(path_customers, mode="w", newline="", encoding="utf-8") as file_customers:
            writer = csv.writer(file_customers)
            writer.writerow(["Nombre", "Apellido", "Telefono"])
        print("\tArchivo clientes.csv creado correctamente")
    else:
        print("\tclientes.csv ya existe")

    path_customers = os.path.join(folder_tests, "reservations.csv")

    if not os.path.exists(path_customers):
        with open(path_customers, mode="w", newline="", encoding="utf-8") as file_customers:
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


def main():
    """Text."""
    print("--- --- ---")
    create_csv_hotel_customers_info(os.path.join("tests"))

    crud_hotel = CRUDSystemHotelCustomer(1)
    crud_customers = CRUDSystemHotelCustomer(0)


    cd_reservations = SystemReservation()

    # Create reservation
    if crud_hotel.check_no_duplicates(h_name="mafalda 21"):

        if crud_customers.check_no_duplicates(c_phone=1112223333):

            cd_reservations.create_reservation(no_room=1,
                                            no_nights=2,
                                            h_name="mafalda 2",
                                            c_phone=1112223333)
        else:
            print("[Creando reservación] No existe el cliente")
    else:
        print("[Creando reservación] No existe el hotel")

    # Cancel reservation
    if crud_hotel.check_no_duplicates(h_name="mafalda 2"):

        if crud_customers.check_no_duplicates(c_phone=1112223333):

            cd_reservations.cancel_reservation(h_name="mafalda 2",
                                               c_phone=1112223333)
        else:
            print("[Cancelando reservación] No existe el cliente")
    else:
        print("[Cancelando reservación] No existe el hotel")


    # # Set
    # crud_hotel.set_register(h_name="kimba",
    #                         h_no_stars=5,
    #                         h_price_per_night=99.99)

    # crud_customers.set_register(c_name="Ali",
    #                             c_last_name="Campos",
    #                             c_phone=4423427014)

    # # Delete
    # crud_hotel.delete_register(h_name="kimba")
    # crud_customers.delete_register(c_phone=4423427014)

    # # Set
    # crud_hotel.set_register(h_name="mafalda",
    #                         h_no_stars=3,
    #                         h_price_per_night=49.99)

    # crud_customers.set_register(c_name="Mady",
    #                             c_last_name="Campos",
    #                             c_phone=4424264142)

    # Get
    # info_hotel = crud_hotel.get_register(h_name="mafalda")
    # info_customer = crud_customers.get_register(c_phone=4424264142)

    # print(info_hotel)
    # print_line_break()
    # print(info_customer)
    # print_line_break()

    # Update
    # crud_hotel.update_register(h_name="mafalda",
    #                            h_no_stars=2,
    #                            h_price_per_night=10.12,
    #                            h_new_name="mafalda 2")
    # print(crud_hotel.get_register(h_name="mafalda"))

    # crud_customers.update_register(c_phone=4424264142,
    #                                c_name="Dany",
    #                                c_last_name="Martinez",
    #                                c_new_phone=1112223333)
    # print(crud_customers.get_register(c_phone=1112223333))

    # Primero chechamos de que existan el hotel y el cliente

if __name__ == '__main__':
    main()

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba
