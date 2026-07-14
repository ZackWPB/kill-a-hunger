from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="🍕 Меню"), KeyboardButton(text="📞 Контакты")]
    ],
    resize_keyboard=True
)