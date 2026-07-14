from typing import Optional

from models.pizza import PIZZAS, Pizza

def get_pizza_by_id(pizza_id: str) -> Optional[Pizza]:
    # Возвращает словарь пиццы или None, если не найдена
    for pizza in PIZZAS:
        if pizza.dish_id == pizza_id:
            return pizza
    return None