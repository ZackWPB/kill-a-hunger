from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models.dish import Dish

def get_menu_keyboard():
    """Возвращает клавиатуру с пиццами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for pizza in Dish.all_dishes:
        button = InlineKeyboardButton(
            text=f"{pizza.name} — {pizza.price} ₽",
            callback_data=pizza.dish_id  # ← здесь id, а не dish_id
        )
        keyboard.inline_keyboard.append([button])
    return keyboard