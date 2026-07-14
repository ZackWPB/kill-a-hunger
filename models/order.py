from aiogram.fsm.state import State, StatesGroup

class OrderForm(StatesGroup):
    choosing_pizza = State()
    entering_address = State()
    entering_phone = State()