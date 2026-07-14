from .dish import Dish

class Pizza(Dish):
    def __init__(self, dish_id: str, name: str, price: int, description: str = None, ingredients: list = None, diameter: int = None):
        super().__init__(dish_id, name, price, description, ingredients)
        self.diameter = diameter if diameter else int


cant_stop_rock = Pizza(
    dish_id="p001",
    name="Can't Stop Rock",
    price=449
)


the_weird_one = Pizza(
    dish_id="p002",
    name="The Weird One",
    price=529
)

saturday_morning = Pizza(
    dish_id="p003",
    name="Saturday Morning",
    price=549
)

