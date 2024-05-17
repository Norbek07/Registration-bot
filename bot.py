import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,ReplyKeyboardRemove
from filters.admin import IsAdminFilter
from filters.check_sub_channel import IsCheckSubChannels,CHANNELS
from bot_state import Register, reg_button
from bot_sqlite import create_users,add_user,count_users, add_user_full,get_all_user_ids
from keyboardbutton import main_button,computer_button,computers,computers_info, phones_info, phone_button, phones

TOKEN = "6858596228:AAF4nh6HiqoqGuU9r_InsILgN19hhPveTv8"
ADMINS = [5012784380]

dp = Dispatcher()

#  Reklama uchun Class yaratildi
class Advert(StatesGroup):
    advert = State()

#  Start bosganda Foydalanuvchilarni ID sini qo'shish
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name

    welcome_text = f"Salom {full_name},  \nKompyuter va telefonlar botiga hush kelibsiz 😊 \nBotdan foydalanish uchun ro'yxatdan o'ting❗️"
    default_text = f"Salom {full_name}, Nima xizmat"
    send_text = message.text

    try:
        add_user(telegram_id, full_name)
        text = welcome_text

    except:
        text = default_text

    await message.answer(text, reply_markup= reg_button)

@dp.message(F.text=="📝 Ro'yxatdan o'tish")
async def register(message:Message, state:FSMContext):
    await message.answer(text= "Ismingizni kiriting !",reply_markup=ReplyKeyboardRemove())
    await state.set_state(Register.first_name)

# Ro'yxatdan o'tish uchun (reg)

#First name 
@dp.message(F.text, Register.first_name)
async def register_first_name(message:Message, state:FSMContext):
    first_name = message.text

    await state.update_data(first_name = first_name)
    await state.set_state(Register.last_name)
    await message.answer(text= "Familiyangizni kiriting")

@dp.message(Register.first_name)
async def register_first_name_del(message:Message, state:FSMContext):
    await message.answer(text= "Ismimgizni to'g'ri kiriting!")
    await message.delete

#last name
@dp.message(F.text, Register.last_name)
async def register_last_name(message:Message, state:FSMContext):
    last_name = message.text
    await message.answer(text="Yoshingizni kiriting")

    await state.update_data(last_name = last_name)
    await state.set_state(Register.age)
    
@dp.message(Register.last_name)
async def register_last_name_del(message:Message, state:FSMContext):
    await message.answer(text= "Familiyangizni to'g'ri kiriting!")
    await message.delete()

# age 
@dp.message(F.text, Register.age)
async def register_age(message:Message, state:FSMContext):
    age = message.text.title()
    await message.answer(text="📍 Manzilni kiriting")

    await state.update_data(age = age)
    await state.set_state(Register.region)

@dp.message(Register.age)
async def register_age_del(message:Message, state:FSMContext):
    await message.answer(text= "Yoshingizni to'g'ri kiriting!")
    await message.delete()

# region 
@dp.message(F.text, Register.region)
async def register_region(message:Message, state:FSMContext):
    region = message.text
    await message.answer(text="☎️ Telefon raqamni kiriting")

    await state.update_data(region = region)
    await state.set_state(Register.phone_number)

@dp.message(Register.region)
async def register_region_del(message:Message, state:FSMContext):
    await message.answer(text= "Manzilni to'g'ri kiriting!")
    await message.delete()

# phone va dataga ma'lumot qo'shish
@dp.message(F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), Register.phone_number)
async def register_email(message:Message, state:FSMContext):
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    age = data.get("age")
    region = data.get("region")
    phone_number = message.text
    text = f"⚠️Yangi o'quvchi ro'yxatdan o'tdi ❗️ : \nIsmi: {first_name} \nFamiliyasi: {last_name} \nYoshi: {age} \nManzil: {region} \nTelefon raqam: {phone_number}"

    await bot.send_message(chat_id=ADMINS[0], text=text)

    await state.clear()
    # data ga ma'lumotini yangilash user id ga qarab
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    try:
        add_user_full(first_name, last_name, age, region, phone_number,telegram_id)
        text = "Siz muvaffaqiyatli ro'yhatdan o'tdingiz 🎉"
    except:
        text = f"Salom {full_name}, Nima xizmat"
    await message.answer(text,reply_markup =main_button)



@dp.message(Register.phone_number)
async def register_phone_number_del(message:Message):
    await message.answer(text= "Telefon raqamni to'g'ri kiriting!")
    await message.delete() 

@dp.message(Command("count"), IsAdminFilter(ADMINS))
async def foyda_soni(message:Message):
    try:
        foydalanuvchilar_soni = count_users()[0]
        await message.answer(f"Botimizda {foydalanuvchilar_soni}ta foydalanuvchi mavjud")
    except:
        await message.answer(f"Botimizda foydalanuvchi yo'q")

@dp.message(Command("advert"),IsAdminFilter(ADMINS))
async def advert_admin(message:Message,state:FSMContext):
    await message.answer("Reklama yuboringiz mumkin...")
    await state.set_state(Advert.advert)
import time

@dp.message(Advert.advert)
async def send_advert(message:Message,state:FSMContext):
    message_id = message.message_id
    from_user = message.from_user.id
    ids = get_all_user_ids()

    for id in ids:
        try:
            await bot.copy_message(chat_id=id[0],from_chat_id=from_user,message_id=message_id)
            time.sleep(0.1)
        except:
            pass
    await state.clear()

@dp.message(F.text=="💁🏻‍♂️ About us")
async def about_as_handler(message:Message):
    about = "Biz sizga arzon va sifatli texnikalar xarid qilishingizda yordam beramiz ! \n➕ Barcha maxsulotlarimiz 100% kafolatlangan ✅ \n➕ Tovarlarni O'zbekiston bo'ylab yetkazib berish bepul ✅ "
    photo_link = "https://picjumbo.com/wp-content/uploads/entrepreneur-working-in-the-office-2210x1473.jpg"
    await message.answer_photo(photo=photo_link,caption=about)

@dp.message(F.text=="☎️ Contact admin")
async def about_as_handler(message:Message):
    about = "Admin info: \nTel: +998 (97)8710140 \nAdmin: @asilbe_admin" 
    await message.answer(text= about)

@dp.message(F.text == "📍 Location")
async def company_location(message:Message):
    lat = 40.102296
    long = 65.37345
    await message.answer("📍 Asilebk company location ")
    await message.reply_location(latitude=lat,longitude=long)


@dp.message(F.text=="💻 Computers")
async def my_computers(message:Message):
    await message.answer("Our computers",reply_markup=computer_button)

@dp.message(F.text.func(lambda computer:computer in computers))
async def computer_info(message:Message):
    info = computers_info.get(message.text)

    photo = info.get("photo")
    price = info.get("price")
    color = info.get("color")

    text = f"{message.text}\nprice: {price}$ \ncolor:{color} and ..."

    await message.answer_photo(photo=photo,caption=text)


@dp.message(F.text=="📱 Phones")
async def my_computers(message:Message):
    await message.answer("Our computers",reply_markup=phone_button)

@dp.message(F.text.func(lambda phone:phone in phones))
async def computer_info(message:Message):
    info = phones_info.get(message.text)

    photo = info.get("photo")
    price = info.get("price")
    color = info.get("color")

    text = f"{message.text}\nprice: {price}$\ncolor:{color} and ..."

    await message.answer_photo(photo=photo,caption=text)


@dp.message(F.text=="🔙 ortga")
async def computer_func(message:Message):
    text = "Asosiy menu"
    await message.answer(text=text, reply_markup=main_button)

# Bot ishga tushishi haqida ma'lumot
@dp.startup()
async def bot_start():
    await bot.send_message(ADMINS[0], "Botimiz ishga tushdi !")

@dp.shutdown()
async def bot_start():
    await bot.send_message(ADMINS[0], "Bot to'xtadi !")    


async def main():
    create_users()
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML) 
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
