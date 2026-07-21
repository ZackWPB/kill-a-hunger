from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

from models.order import OrderForm
from services.cart_service import CartService

router = Router()

@router.message(Command("checkout"))
async def checkout(message: Message, state: FSMContext):
    cart = await CartService.get_cart(state)

    if not cart:
        await message.answer("❌ Корзина пуста. Добавь пиццу через /menu")
        return

    total = sum(item["price"] for item in cart)
    cart_text = "\n".join([
        f" {item['name']} - {item['price']} ₽"
        for item in cart
    ])

    await state.set_state(OrderForm.entering_address)
    await message.answer(
        f"🛒 **Твой заказ:**\n\n"
        f"{cart_text}\n\n"
        f"💰 **Итого: {total} ₽**\n\n"
        f"🏠 Ввод адрес доставки:"
    )