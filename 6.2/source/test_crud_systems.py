"""Python file to implemente test cases"""

import os
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

from . import main as app_main  # noqa: E402
from .crud_hotel_customer import CRUDSystemHotelCustomer  # noqa: E402
from .crud_reservation import SystemReservation  # noqa: E402


class BaseCRUDTestCase(unittest.TestCase):
    """Base fixtures for CRUD tests using isolated CSVs."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.hotel_path = os.path.join(self.temp_dir.name, "hotel.csv")
        self.customers_path = os.path.join(self.temp_dir.name, "customers.csv")
        self.reservations_path = os.path.join(self.temp_dir.name,
                                              "reservations.csv")

        pd.DataFrame([
            {"Nombre": "HOTEL UNO",
             "No_estrellas": 4,
             "Precio_por_noche": 100.0},
        ]).to_csv(self.hotel_path, index=False, encoding="utf-8")

        pd.DataFrame([
            {"Nombre": "ANA", "Apellido": "LOPEZ", "Telefono": 1234567890},
        ]).to_csv(self.customers_path, index=False, encoding="utf-8")

        pd.DataFrame(
            columns=[
                "Hotel_nombre",
                "Cliente_telefono",
                "Estatus",
                "No_habitacion",
                "No_noches",
                "Total_precio",
            ]
        ).to_csv(self.reservations_path, index=False, encoding="utf-8")

        self.hotel_crud = CRUDSystemHotelCustomer(1)
        self.hotel_crud.folder_tests = self.temp_dir.name

        self.customer_crud = CRUDSystemHotelCustomer(0)
        self.customer_crud.folder_tests = self.temp_dir.name

        self.reservation_sys = SystemReservation()
        self.reservation_sys.folder_tests = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()


class CRUDHotelCustomerTests(BaseCRUDTestCase):
    """Class to testing CRUD hotel."""

    def test_check_no_duplicates_for_hotel_and_customer(self):
        """Test check_no_duplicates for hotel and customer."""
        self.assertTrue(
            self.hotel_crud.check_no_duplicates(h_name="HOTEL UNO")
        )
        self.assertFalse(
            self.hotel_crud.check_no_duplicates(h_name="OTRO")
        )
        self.assertTrue(
            self.customer_crud.check_no_duplicates(c_phone=1234567890)
        )
        self.assertFalse(
            self.customer_crud.check_no_duplicates(c_phone=1111111111)
        )

    def test_set_and_get_hotel_register(self):
        """Test set and get register for hotel."""
        self.hotel_crud.set_register(
            h_name="HOTEL DOS", h_no_stars=3, h_price_per_night=80.0
        )
        df = pd.read_csv(self.hotel_path)
        self.assertEqual(len(df), 2)
        row = self.hotel_crud.get_register(h_name="HOTEL DOS")
        self.assertEqual(row.iloc[0]["No_estrellas"], 3)

    def test_prevent_duplicate_customer_register(self):
        """Test that duplicate customer register is prevented."""
        self.customer_crud.set_register(
            c_name="ANA", c_last_name="LOPEZ", c_phone=1234567890
        )
        df = pd.read_csv(self.customers_path)
        self.assertEqual(len(df), 1)

    def test_delete_customer_register(self):
        """Test delete register for customer."""
        self.customer_crud.delete_register(c_phone=1234567890)
        df = pd.read_csv(self.customers_path)
        self.assertEqual(len(df), 0)

    def test_update_hotel_register(self):
        """Test update register for hotel."""
        self.hotel_crud.update_register(
            h_name="HOTEL UNO",
            h_no_stars=5,
            h_price_per_night=150.5,
            h_new_name="HOTEL ACTUALIZADO"
        )
        df = pd.read_csv(self.hotel_path)
        self.assertIn("HOTEL ACTUALIZADO", df["Nombre"].values)
        row = df[df["Nombre"] == "HOTEL ACTUALIZADO"].iloc[0]
        self.assertEqual(row["No_estrellas"], 5)
        self.assertEqual(row["Precio_por_noche"], 150.5)

    def test_update_customer_with_invalid_new_phone(self):
        """Test update register for customer with invalid new phone."""
        self.customer_crud.update_register(
            c_phone=1234567890,
            c_name="ANA",
            c_last_name="RAMOS",
            c_new_phone=123,
        )
        df = pd.read_csv(self.customers_path)
        row = df.iloc[0]
        self.assertEqual(row["Telefono"], 1234567890)
        self.assertEqual(row["Apellido"], "RAMOS")


class CRUDHotelCustomerEdgeTests(BaseCRUDTestCase):
    """Extra coverage for edge branches."""

    def test_get_register_nonexistent_hotel_returns_empty(self):
        """Test get register for nonexistent hotel returns empty DataFrame."""
        result = self.hotel_crud.get_register(h_name="NOPE")
        self.assertTrue(result.empty)

    def test_set_register_missing_args_hotel(self):
        """Test set register for hotel with missing arguments."""
        self.hotel_crud.set_register(h_name=None,
                                     h_no_stars=None,
                                     h_price_per_night=None)
        df = pd.read_csv(self.hotel_path)
        self.assertEqual(len(df), 1)

    def test_set_register_duplicate_hotel(self):
        """Test set register for hotel with duplicate name."""
        self.hotel_crud.set_register(h_name="HOTEL UNO",
                                     h_no_stars=4,
                                     h_price_per_night=100.0)
        df = pd.read_csv(self.hotel_path)
        self.assertEqual(len(df), 1)

    def test_delete_nonexistent_customer(self):
        """Test delete register for nonexisten customer."""
        self.customer_crud.delete_register(c_phone=9999999999)
        df = pd.read_csv(self.customers_path)
        self.assertEqual(len(df), 1)

    def test_update_customer_nonexistent(self):
        """Test update register for nonexistent customer."""
        self.customer_crud.update_register(c_phone=5555555555,
                                           c_name="X",
                                           c_last_name="Y",
                                           c_new_phone=4444444444)
        df = pd.read_csv(self.customers_path)
        self.assertNotIn(4444444444, df["Telefono"].values)

    def test_update_hotel_invalid_values(self):
        """Test update register for hotel with invalid values."""
        self.hotel_crud.update_register(h_name="HOTEL UNO",
                                        h_no_stars=0,
                                        h_price_per_night=-1,
                                        h_new_name=None)
        df = pd.read_csv(self.hotel_path)
        row = df.iloc[0]
        self.assertEqual(row["Nombre"], "HOTEL UNO")
        self.assertEqual(row["No_estrellas"], 4)
        self.assertEqual(row["Precio_por_noche"], 100.0)


class ReservationSystemTests(BaseCRUDTestCase):
    """Tests for reservation system."""

    def test_create_reservation_success(self):
        """Test creating a reservation successfully."""
        created = self.reservation_sys.create_reservation(
            no_room=5, no_nights=2, h_name="HOTEL UNO", c_phone=1234567890
        )
        self.assertTrue(created)
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Total_precio"], 200.0)

    def test_create_reservation_rejects_existing_active(self):
        """Test rejecting a reservation when customer already has an active."""
        pd.DataFrame(
            [
                {
                    "Hotel_nombre": "HOTEL UNO",
                    "Cliente_telefono": 1234567890,
                    "Estatus": True,
                    "No_habitacion": 1,
                    "No_noches": 1,
                    "Total_precio": 100.0,
                }
            ]
        ).to_csv(self.reservations_path, index=False, encoding="utf-8")

        created = self.reservation_sys.create_reservation(
            no_room=2, no_nights=3, h_name="HOTEL UNO", c_phone=1234567890
        )
        self.assertFalse(created)
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 1)

    def test_cancel_reservation_marks_inactive(self):
        """Test canceling a reservation marks it as inactive."""
        pd.DataFrame(
            [
                {
                    "Hotel_nombre": "HOTEL UNO",
                    "Cliente_telefono": 1234567890,
                    "Estatus": True,
                    "No_habitacion": 1,
                    "No_noches": 2,
                    "Total_precio": 200.0,
                }
            ]
        ).to_csv(self.reservations_path, index=False, encoding="utf-8")

        self.reservation_sys.cancel_reservation(h_name="HOTEL UNO",
                                                c_phone=1234567890)
        df = pd.read_csv(self.reservations_path)
        self.assertFalse(df.iloc[0]["Estatus"])

    def test_create_reservation_with_invalid_inputs(self):
        """Test creating a reservation with invalid inputs is rejected."""
        self.assertFalse(
            self.reservation_sys.create_reservation(
                no_room=-1, no_nights=1, h_name="HOTEL UNO", c_phone=1234567890
            )
        )
        self.assertFalse(
            self.reservation_sys.create_reservation(
                no_room=1, no_nights=0, h_name="HOTEL UNO", c_phone=1234567890
            )
        )
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 0)


class MainHelpersTests(unittest.TestCase):
    """Tests for helper functions in main.py."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_csv_hotel_customers_info_creates_files(self):
        """Test that create_csv_hotel_customers_info creates CSV files."""
        app_main.create_csv_hotel_customers_info(self.temp_dir.name)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir.name,
                                                    "hotel.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir.name,
                                                    "customers.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir.name,
                                                    "reservations.csv")))

    def test_upper_text_trims_and_uppercases(self):
        """Test that upper_text trims whitespace and converts to uppercase."""
        self.assertEqual(app_main.upper_text("  hola mundo  "), "HOLA MUNDO")

    @patch("builtins.input", side_effect=["123", "1234567890"])
    def test_valid_phone_loops_until_valid(self, mock_input):
        """Test valid_phone loops until 10-digit phone number is entered."""
        self.assertEqual(app_main.valid_phone(), 1234567890)
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["-1", "10.5"])
    def test_valid_price_requires_positive(self, mock_input):
        """Test that valid_price loops until a positive price is entered."""
        self.assertEqual(app_main.valid_price(), 10.5)
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["7", "3"])
    def test_valid_hotel_stars_requires_range(self, mock_input):
        """Test hotel stars loops until number between 1 and 5 is entered."""
        self.assertEqual(app_main.valid_hotel_stars(), 3)
        self.assertEqual(mock_input.call_count, 2)


class MainCrudFlowTests(unittest.TestCase):
    """Tests for the main CRUD flow using mocked inputs."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.hotel_path = os.path.join(self.temp_dir.name,
                                       "hotel.csv")
        self.customers_path = os.path.join(self.temp_dir.name,
                                           "customers.csv")
        self.reservations_path = os.path.join(self.temp_dir.name,
                                              "reservations.csv")

        pd.DataFrame([
            {"Nombre": "HOTEL UNO",
             "No_estrellas": 4,
             "Precio_por_noche": 100.0},
        ]).to_csv(self.hotel_path, index=False, encoding="utf-8")

        pd.DataFrame([
            {"Nombre": "ANA", "Apellido": "LOPEZ", "Telefono": 1234567890},
        ]).to_csv(self.customers_path, index=False, encoding="utf-8")

        pd.DataFrame(
            columns=[
                "Hotel_nombre",
                "Cliente_telefono",
                "Estatus",
                "No_habitacion",
                "No_noches",
                "Total_precio",
            ]
        ).to_csv(self.reservations_path, index=False, encoding="utf-8")

        self.hotel_crud = CRUDSystemHotelCustomer(1)
        self.hotel_crud.folder_tests = self.temp_dir.name

        self.customer_crud = CRUDSystemHotelCustomer(0)
        self.customer_crud.folder_tests = self.temp_dir.name

        self.reservation_sys = SystemReservation()
        self.reservation_sys.folder_tests = self.temp_dir.name

        app_main.CRUD_HOTEL = self.hotel_crud
        app_main.CRUD_CUSTOMERS = self.customer_crud
        app_main.CD_RESERVATIONS = self.reservation_sys

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("source.main.valid_hotel_stars", return_value=3)
    @patch("source.main.valid_price", return_value=75.0)
    @patch("builtins.input", return_value="Hotel Tres")
    def test_set_hotel_flow(self):
        """Test the flow of setting a hotel with mocked inputs."""
        app_main.set_hotel()
        df = pd.read_csv(self.hotel_path)
        self.assertIn("HOTEL TRES", df["Nombre"].values)

    @patch("source.main.valid_phone", return_value=9876543210)
    @patch("builtins.input", side_effect=["Ana", "Lopez"])
    def test_set_customer_flow(self):
        """Test the flow of setting a customer with mocked inputs."""
        app_main.set_customer()
        df = pd.read_csv(self.customers_path)
        self.assertIn(9876543210, df["Telefono"].values)

    @patch("builtins.input", return_value="hotel uno")
    def test_delete_hotel_flow(self):
        """Test the flow of deleting a hotel with mocked input."""
        app_main.delete_hotel()
        df = pd.read_csv(self.hotel_path)
        self.assertEqual(len(df), 0)

    @patch("source.main.valid_phone", return_value=1234567890)
    @patch("builtins.input", return_value="ANA")
    def test_delete_customer_flow(self):
        """Test the flow of deleting a customer with mocked input."""
        app_main.delete_customer()
        df = pd.read_csv(self.customers_path)
        self.assertEqual(len(df), 0)

    @patch("source.main.valid_phone", return_value=1234567890)
    @patch("builtins.input", side_effect=["1", "2", "HOTEL UNO"])
    def test_create_reservation_flow(self):
        """Test the flow of creating a reservation with mocked inputs."""
        app_main.create_reservation()
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 1)
        self.assertTrue(df.iloc[0]["Estatus"])

    @patch("source.main.valid_phone", return_value=1234567890)
    @patch("builtins.input", return_value="HOTEL UNO")
    def test_cancel_reservation_flow(self):
        """Test the flow of canceling a reservation with mocked inputs."""
        pd.DataFrame([
            {
                "Hotel_nombre": "HOTEL UNO",
                "Cliente_telefono": 1234567890,
                "Estatus": True,
                "No_habitacion": 1,
                "No_noches": 1,
                "Total_precio": 100.0,
            }
        ]).to_csv(self.reservations_path, index=False, encoding="utf-8")

        app_main.cancel_reservation()
        df = pd.read_csv(self.reservations_path)
        self.assertFalse(df.iloc[0]["Estatus"])

    @patch("builtins.input", return_value="HOTEL UNO")
    def test_get_hotel_flow(self):
        """Test the flow of getting a hotel with mocked input."""
        result = app_main.get_hotel()
        self.assertIsNone(result)

    @patch("source.main.valid_phone", return_value=1234567890)
    @patch("builtins.input", return_value="1234567890")
    def test_get_customer_flow(self):
        """Test the flow of getting a customer with mocked inputs."""
        result = app_main.get_customer()
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["HOTEL UNO", "N", "N", "N"])
    def test_update_hotel_no_changes(self):
        """Test the flow of updating a hotel with no changes."""
        app_main.update_hotel()
        df = pd.read_csv(self.hotel_path)
        self.assertIn("HOTEL UNO", df["Nombre"].values)

    @patch("source.main.valid_phone", return_value=1234567890)
    @patch("builtins.input", side_effect=["N", "N", "N"])
    def test_update_customer_no_changes(self):
        """Test the flow of updating a customer with no changes."""
        app_main.update_customer()
        df = pd.read_csv(self.customers_path)
        self.assertIn(1234567890, df["Telefono"].values)

    @patch("source.main.valid_phone", return_value=1234567890)
    @patch("builtins.input", side_effect=["1", "1", "HOTEL NO"])
    def test_create_reservation_hotel_missing(self):
        """Test creating a reservation when the hotel does not exist."""
        app_main.create_reservation()
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 0)

    @patch("source.main.valid_phone", return_value=9999999999)
    @patch("builtins.input", side_effect=["1", "1", "HOTEL UNO"])
    def test_create_reservation_customer_missing(self):
        """Test creating a reservation when the customer does not exist."""
        app_main.create_reservation()
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 0)

    @patch("source.main.valid_phone", return_value=1234567890)
    @patch("builtins.input", return_value="HOTEL NO")
    def test_cancel_reservation_hotel_missing(self):
        """Test canceling a reservation when the hotel does not exist."""
        app_main.cancel_reservation()
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 0)

    @patch("source.main.valid_phone", return_value=9999999999)
    @patch("builtins.input", return_value="HOTEL UNO")
    def test_cancel_reservation_customer_missing(self):
        """Test canceling a reservation when the customer does not exist."""
        app_main.cancel_reservation()
        df = pd.read_csv(self.reservations_path)
        self.assertEqual(len(df), 0)


if __name__ == "__main__":
    unittest.main()
