"""Text"""

import os
from typing import Optional
import pandas as pd

class CRUDSystemHotelCustomer:
    """CRUD system focus to hotel and customers."""

    def __init__(self, hotel:int=0):
        if hotel == 1:
            self.hotel = 1
            self.customers = 0
        else:
            self.customers = 1
            self.hotel = 0

        self.folder_tests = os.path.join("tests")
        os.makedirs(self.folder_tests, exist_ok=True)


    def _print_line_break(self) -> None:
        """Print linre break to show info."""
        print("\n\n")


    def _csv_to_pandas(self) -> pd.DataFrame:
        """Return pandas from csv file."""
        if self.hotel == 1:
            return pd.read_csv(f"{self.folder_tests}/hotel.csv", encoding="utf-8")
        else:
            return pd.read_csv(f"{self.folder_tests}/customers.csv", encoding="utf-8")


    def _pandas_to_csv(self, df:pd.DataFrame) -> None:
        """Save pandas information into csv file."""
        if self.hotel == 1:
            try:
                df.to_csv(f"{self.folder_tests}/hotel.csv", index=False, encoding="utf-8")

                print("--> hotel.csv actualizado correctamente")
            except (IOError, OSError) as e:
                print(f"Eror in _pandas_to_csv [1]: {e}")

        else:
            try:
                df.to_csv(f"{self.folder_tests}/customers.csv", index=False, encoding="utf-8")

                print("**> customers.csv actualizado correctamente")
            except (IOError, OSError) as e:
                print(f"Eror in _pandas_to_csv [2]: {e}")
        
        self._print_line_break()


    def _check_no_duplicates(self,
                             h_name:Optional[str]=None,
                             c_phone:Optional[int]=None) -> bool:
        """Check there is not duplicates registers by hotel name and phone customer."""
        df = self._csv_to_pandas()

        if self.hotel == 1:
            return h_name in df["Nombre"].values
        else:
            return c_phone in df["Telefono"].values


    def get_register(self,
                        h_name:Optional[str]=None,
                        c_phone:Optional[int]=None) -> None:
        """Delete hotel or customer from db."""
        df = self._csv_to_pandas()

        if self.hotel == 1:
            try:
                row = df.query(f'Nombre == "{h_name}"')
            except (KeyError, TypeError) as e:
                print(f"Error in get_register [1]: {e}")
                return None

            if row.empty:
                print(f"\tEl hotel {h_name} no existe en el csv")
            else:
                return row
        else:
            try:
                row = df.query(f'Telefono == {c_phone}')
            except (KeyError, TypeError) as e:
                print(f"Error in get_register [2]: {e}")
                return None

            if row.empty:
                print(f"\tEl cliente tel:{c_phone} no existe en el csv")
            else:
                return row


    def set_register(self,
                        h_name:Optional[str]=None,
                        h_no_stars:Optional[int]=None,
                        h_price_per_night:Optional[float]=None,
                        c_name:Optional[str]=None,
                        c_last_name:Optional[str]=None,
                        c_phone:Optional[int]=None) -> None:
        """Insert information in csv."""
        print("[create_csv_hotel_customers_info]")

        df = self._csv_to_pandas()

        if self.hotel == 1:
            if h_name is None or h_no_stars is None or h_price_per_night is None:
                print("\tFaltan argumentos del hotel: name, no_stars y price_per_night.")
                self._print_line_break()
                return

            if self._check_no_duplicates(h_name=h_name):
                print(f"\tEl hotel {h_name} YA ESTÁ registrado")
                self._print_line_break()
                return

            new_data = {
                "Nombre": h_name,
                "No_estrellas": h_no_stars,
                "Precio_por_noche": h_price_per_night
            }

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

            print(f"\tEl hotel {h_name} ha sido agregado...")

        else:
            if c_name is None or c_last_name is None or c_phone is None:
                print("\tFaltan argumentos del cliente: name, last_name y phone.")
                self._print_line_break()
                return

            if self._check_no_duplicates(c_phone=c_phone):
                print(f"\tEl cliente {c_name} con el teléfono {c_phone} YA ESTÁ registrado")
                self._print_line_break()
                return

            new_data = {
                "Nombre": c_name,
                "Apellido": c_last_name,
                "Telefono": c_phone
            }

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

            print(f"\tEl cliente {c_name} ha sido agregado...")

        self._pandas_to_csv(df)
        self._print_line_break()


    def delete_register(self,
                        h_name:Optional[str]=None,
                        c_phone:Optional[int]=None) -> None:
        """Delete hotel or customer from db."""
        df = self._csv_to_pandas()

        if self.hotel == 1:
            if self._check_no_duplicates(h_name=h_name):
                df = df[df["Nombre"] != h_name]
                print(f"\tEl hotel {h_name} ha sido eliminado con éxito")
            else:
                print(f"\tNo existe el hotel {h_name}")
        else:
            if self._check_no_duplicates(c_phone=c_phone):
                df = df[df["Telefono"] != c_phone]
                print(f"\tEl cliente tel:{c_phone} ha sido eliminado con éxito")
            else:
                print(f"\tNo existe el cliente tel:{c_phone}")

        self._pandas_to_csv(df)

import pandas as pd

df = pd.read_csv("hotel.csv")

nombre_modificar = "Hotel Plaza"

df.loc[df["Nombre"] == nombre_modificar, "No Estrellas"] = 5
df.loc[df["Nombre"] == nombre_modificar, "Precio por noche"] = 2000

df.to_csv("hotel.csv", index=False)

print("Hotel modificado correctamente")

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba
