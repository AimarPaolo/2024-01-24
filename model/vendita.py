from dataclasses import dataclass
from datetime import date


@dataclass
class Vendita:
    Retailer_code: int
    Product_number: int
    Order_method_code: int
    Date: date
    Quantity: int
    Unit_price: float
    Unit_sale_price: float

    def __hash__(self):
        return hash((self.Retailer_code, self.Product_number, self.Order_method_code))
