import logging
import asyncio
from aiogram import Dispatcher, Bot

from config.settings import BOT_TOKEN
import models.pizza


logging.basicConfig(level=logging.INFO)

bot = Bot(token= BOT_TOKEN)
dp = Dispatcher()


from handlers.start import router as start_router
from handlers.order import router as order_router
from handlers.menu import router as menu_router
from handlers.contacts import router as contacts_router
from handlers.help import router as help_router
from handlers.cart import router as cart_router

dp.include_router(start_router)
dp.include_router(order_router)
dp.include_router(menu_router)
dp.include_router(contacts_router)
dp.include_router(help_router)
dp.include_router(cart_router)

async def main():
    print("🎸 Kill a Hunger запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())