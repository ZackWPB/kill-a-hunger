from aiogram.fsm.context import FSMContext

class CartService:

    @staticmethod
    async def get_cart(state: FSMContext):
        data = await state.get_data()
        return data.get("cart", [])

    @staticmethod
    async def add_item(state: FSMContext, dish: dict) -> None:
        data = await state.get_data()
        cart = data.get("cart", [])
        cart.append(dish)
        await state.update_data(cart=cart)

    @staticmethod
    async def remove_item(state: FSMContext, dish_id: str) -> None:
        data = await state.get_data()
        cart = data.get("cart", [])
        cart = [item for item in cart if item["id"] != dish_id]
        await state.update_data(cart=cart)

    @staticmethod
    async def clear(state: FSMContext) -> None:
        await state.update_data(cart=[])