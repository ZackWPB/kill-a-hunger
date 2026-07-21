import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, Bot

from config.settings import ADMIN_ID

from models.pizza import Pizza
from models.order import OrderForm
from keyboards.main_keyboard import main_kb
from services.cart_service import CartService

router = Router()

@router.callback_query(OrderForm.choosing_pizza)
async def process_pizza_callback(callback: CallbackQuery, state: FSMContext):
    pizza_id = callback.data
    pizza = Pizza.get_by_id(pizza_id)

    if not pizza:
        await callback.answer("❌ Пицца не найдена.")
        return

    # Добавляем в корзину
    await CartService.add_item(state, {
        "id": pizza.dish_id,
        "name": pizza.name,
        "price": pizza.price,
    })

    # Отвечаем на callback
    await callback.answer()

    # Получаем корзину
    cart = await CartService.get_cart(state)
    total = sum(item["price"] for item in cart)

    # Формирование список пицц в корзине
    cart_text = "\n".join([
        f"{item['name']} - {item['price']} ₽"
        for item in cart
    ])

    # Отображаем корзину
    await callback.message.edit_text(
        f"🛒 **Твоя корзина:**\n\n"
        f"{cart_text}\n\n"
        f"\n\n💰 **Итого: {total} ₽\n\n"
        "Выбери дейстиве:\n"
        "Добавить еще - /menu\n"
        "Оформить заказ - /checkout\n"
    )

    # Убираем клавиатуру после выбора
    await callback.message.edit_reply_markup(reply_markup=None)

@router.message(OrderForm.entering_address)
async def process_address(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("❌ Слишком короткий адрес. Напиши подробнее, пожалуйста.")
        return

    await state.update_data(address=message.text)
    await state.set_state(OrderForm.entering_phone)
    await message.answer(
        "📞 Отправь **номер телефона** для связи: \n"
        "Пример: '+7 900 123 45 67'",
        parse_mode=None
    )

@router.message(OrderForm.entering_phone)
async def process_phone(message: Message, state: FSMContext, bot: Bot):
    if not any(char.isdigit() for char in message.text):
        await message.answer("❌ Пожалуйста, отправь настоящий номер телефона с цифрами.")
        return

    await state.update_data(phone=message.text)
    data = await state.get_data()

    # Формируем красивый отчет для админа
    order_text = (
        f"🔥 **НОВЫЙ ЗАКАЗ!** 🔥\n\n"
        f"🍕 **Пицца:** \n"
        f"💰 **Сумма:**  \n"
        f"📍 **Адрес:** {data['address']}\n"
        f"📞 **Телефон:** {data['phone']}\n"
        f"👤 **Клиент:** @{message.from_user.username or 'нет юзернейма'} (ID: {message.from_user.id})\n"
        f"🕒 **Время:** {message.date.strftime('%d.%m.%Y %H:%M')}"
    )

    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, order_text)
    else:
        logging.error("ADMIN_ID не задан в .env")


    # Отправляем подтверждение клиенту
    await message.answer(
        "✅ **Заказ принят!** ✅\n\n"
        f"Скоро с тобой свяжется оператор для подтверждения по номеру {data['phone']}.\n"
        "Спасибо, что выбрал **Red Hot Pepperoni**! 🎸🌶️\n\n"
        "Чтобы сделать новый заказ, нажми /start",
        reply_markup=main_kb,
        parse_mode=None
    )

    await state.clear()