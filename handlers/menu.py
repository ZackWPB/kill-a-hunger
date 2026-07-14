from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models.order import OrderForm
from keyboards.menu import get_menu_keyboard

router = Router()

@router.message(F.text == "🍕 Меню")
async def show_menu(message: Message, state: FSMContext):
    await state.set_state(OrderForm.choosing_pizza)

    keyboard = get_menu_keyboard()  # ← получаем клавиатуру из keyboards

    await message.answer("🍕 Выбери пиццу:", reply_markup=keyboard)