from typing import List, Optional

class Dish:
    # Общее храниилище для ВСЕХ (и пицц, и напитков, и всего)
    all_dishes: List[Dish] = []

    def __init__(self, dish_id: str, name: str, price: int, description: str = None, ingredients: list = None):
        self.name = name
        self.price = price
        self.dish_id = dish_id
        self.description = description if description else ''
        self.ingredients = ingredients if ingredients else []

        # Автоматически добавляем объект в общее хранилище
        Dish.all_dishes.append(self)

    @classmethod
    def get_by_id(cls, dish_id: str) -> Optional['Dish']:
        # Ищет блюдо по ID среди всех блюд
        for dish in cls.all_dishes:
            if dish.dish_id == dish_id:
                return dish
        return None

    @classmethod
    def get_by_name(cls, name: str) -> Optional['Dish']:
        # Ищет пиццу по имени (используется при выборе)
        for dish in cls.all_dishes:
            if dish.name == name:
                return dish
        return None

    def get_info(self):
        return f"{self.name} - {self.price} ₽"


