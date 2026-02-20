"""Text"""
class CRUDSystemHotelCustomer:
    """CRUD system focus to hotel and customers."""

    def __init__(self, hotel:int=0):
        if hotel == 1:
            self.hotel = 1
            self.customers = 0
        else:
            self.customers = 1
            self.hotel = 0


    def _create_csv_hotel_customers_info(self):
        pass

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba
