from aiogram import F
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message(F.text == "📞 Контакты")
async def show_contacts(message: Message):
    await message.answer(
        "📞 **Наши контакты:**\n\n"
        "📱**Поддержка в Telegram:** \n"
        "📞 **Телефон** +7 (980) 549-09-32\n"
        "🌐 **Telegram-канал:** https://t.me/redhotpepperoni\n\n"
        "По вопросам сотрудничества пиши в личку @gentle_punk",
        parse_mode=None
    )