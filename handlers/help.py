from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    # Помощь
    await message.answer(
        "❓ **Помощь**\n\n"
        "/start - начать работу с ботом\n"
        "/menu - показать меню\n"
        "/help - эта справка\n\n"
        "По всем вопросам пиши в поддержку.",
        parse_mode=None
    )