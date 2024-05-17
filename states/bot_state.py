from aiogram.fsm.state import State, StatesGroup

from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

reg_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Ro'yxatdan o'tish")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Choise button..."
)

class Register(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    region = State()
    phone_number = State()

    
