"""Class to implement system reservations:
Create and cancel"""

import os
from typing import Tuple, Optional
import pandas as pd

class SystemReservation:
    """CD system focus to reservations"""

    def __init__(self):
        self.folder_tests = os.path.join("tests")
        os.makedirs(self.folder_tests, exist_ok=True)


    def _print_line_break(self) -> None:
        """Print linre break to show info."""
        print("\n\n")


    def _csv_to_pandas(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Return pandas from csv file."""
        df1 = pd.read_csv(f"{self.folder_tests}/reservations.csv", encoding="utf-8")
        df2 = pd.read_csv(f"{self.folder_tests}/hotel.csv", encoding="utf-8")
        df3 = pd.read_csv(f"{self.folder_tests}/customers.csv", encoding="utf-8")

        return df1, df2, df3


    def _pandas_to_csv(self, df:pd.DataFrame) -> None:
        """Save pandas information into csv file."""
        try:
            df.to_csv(f"{self.folder_tests}/reservations.csv", index=False, encoding="utf-8")
            print("\n==> reservations.csv actualizado correctamente")
        except (IOError, OSError) as e:
            print(f"Eror in _pandas_to_csv [reservations.csv]: {e}")
        self._print_line_break()


    def create_reservation(self,
                           no_room:int,
                           no_nights:int,
                           h_name:str,
                           c_phone:int) -> None:
        """Create a reservation in hotel."""
        if no_room < 0:
            print("El no de habitación no puede ser menor que 0")
            return False

        if no_nights <= 0:
            print("El no de noches tiene que ser mayor a 0")
            return False

        df_reservations, df_hotel, _ = self._csv_to_pandas()

        row_hotel = df_hotel.query(f'Nombre == "{h_name}"')
        price = row_hotel["Precio_por_noche"][0] * no_nights

        if c_phone in df_reservations["Cliente_telefono"].values:

            row_reservations = df_reservations[df_reservations["Cliente_telefono"] == c_phone]

            if row_reservations.iloc[0]["Estatus"]:
                print(f"El cliente tel:{c_phone} ya tiene una reservación en '{h_name}' activa")
                return False

        new_data = {
            "Hotel_nombre": h_name,
            "Cliente_telefono": c_phone,
            "Estatus": True,
            "No_habitacion": no_room,
            "No_noches": no_nights,
            "Total_precio": price
        }

        df = pd.concat([df_reservations, pd.DataFrame([new_data])], ignore_index=True)
        print(f"\tRevervacion exitosa: hotel: {h_name} & cliente tel:{c_phone}")

        self._pandas_to_csv(df)
        self._print_line_break()
        return True


    def cancel_reservation(self,
                           h_name:str,
                           c_phone:int) -> None:
        """Cancel a reservation in hotel with phone customer."""

        df_reservations, _, _ = self._csv_to_pandas()

        df_reservations.loc[
            (df_reservations["Hotel_nombre"] == h_name) &
            (df_reservations["Cliente_telefono"] == c_phone),
            "Estatus"
        ] = False

        print(f"\n\tReservación ha sido cancelada: hotel: {h_name} & cliente tel:{c_phone}")

        self._pandas_to_csv(df_reservations)
        self._print_line_break()
        return True


    def show_reservations(self):
        """Show reservations"""
        df_reservations, _, _ = self._csv_to_pandas()

        return df_reservations

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba
