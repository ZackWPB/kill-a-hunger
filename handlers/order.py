import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, Bot

from config.settings import ADMIN_ID

from models.pizza import Pizza
from models.order import OrderForm
from keyboards.main_keyboard import main_kb

router = Router()

@router.callback_query(OrderForm.choosing_pizza)
async def process_pizza_callback(callback: CallbackQuery, state: FSMContext):
    # Обрабатывает выбор пиццы через Inline-кнопки

    # Извлекаем ID пиццы из callback_data
    pizza_id = callback.data
    pizza = Pizza.get_by_id(pizza_id)

    if not pizza:
        await callback.answer("❌ Пицца не найдена.")
        return

    # Сохраняем данные в FSM
    await state.update_data(
        pizza_id=pizza.dish_id,
        pizza_name=pizza.name,
        pizza_price=pizza.price
    )

    # Переходим к вводу адреса
    await state.set_state(OrderForm.entering_address)

    # Отвечаем на callback, чтобы убрать «часики» на кнопке
    await callback.answer()

    # Отправляем сообщение с запросом адреса
    await callback.message.edit_text(
        f"✅ Отлично! {pizza.get_info()}\n\n"
        "🏠 Теперь напиши адрес доставки:\n"
        "(Улица, дом, квартира, подъезд, этаж)",
        parse_mode=None
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
        f"🍕 **Пицца:** {data['pizza_name']}\n"
        f"💰 **Сумма:** {data['pizza_price']} ₽\n"
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