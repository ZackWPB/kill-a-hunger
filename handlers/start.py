from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from keyboards.main_keyboard import main_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    # Приветствие и главное меню
    await state.clear()
    await message.answer(
        "🌶️🎸 **Red Hot Pepperoni** 🎸🌶️\n\n"
        "Рок-н-ролльная пицца с отсылками к Red Hot Chili Peppers.\n"
        "Чтобы сделать заказ, нажми и выбери пиццу.",
        reply_markup=main_kb,
    )