from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,InlineKeyboardButton
from data import config
import asyncio
import logging
import sys
from menucommands.set_bot_commands  import set_default_commands
from baza.sqlite import Database
from filters.admin import IsBotAdminFilter
from keyboard_buttons import admin_keyboard
from aiogram.fsm.context import FSMContext #new
from states.reklama import Adverts
from aiogram.utils.keyboard import InlineKeyboardBuilder
from states.bot_state import Register, reg_button
from baza.bot_sqlite import create_users,add_user,count_users, add_user_full,get_all_user_ids
from keyboard_buttons.keyboardbutton import main_button,computer_button,computers,computers_info, phones_info, phone_button, phones
import time 

ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()


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
    await message.answer(text= "Ismingizni kiriting !",reply_markup=reg_button)
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

@dp.message(Register.region)
async def register_region_del(message:Message, state:FSMContext):
    await message.answer(text= "☎️ Telefon raqamni kiriting")
    await message.delete()

@dp.message(Adverts.advert)
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


@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz")
    except:
        await message.answer(text="Assalomu alaykum")




# @dp.message(IsCheckSubChannels())
# async def kanalga_obuna(message:Message):
#     text = ""
#     inline_channel = InlineKeyboardBuilder()
#     for index,channel in enumerate(CHANNELS):
#         ChatInviteLink = await bot.create_chat_invite_link(channel)
#         inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
#     inline_channel.adjust(1,repeat=True)
#     button = inline_channel.as_markup()
#     await message.answer(f"{text} kanallarga azo bo'ling",reply_markup=button)



#help commands
@dp.message(Command("help"))
async def help_commands(message:Message):
    await message.answer("Sizga qanday yordam kerak")
    
#about commands
@dp.message(Command("about"))
async def about_commands(message:Message):
    await message.answer("Sifat 2024")


@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    # Spamdan himoya qilish uchun klassik ichki o'rta dastur. So'rovlar orasidagi asosiy vaqtlar 0,5 soniya
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))



async def main() -> None:
    global bot,db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = Database(path_to_db="main.db")
    await set_default_commands(bot)
    await dp.start_polling(bot)
    setup_middlewares(dispatcher=dp, bot=bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
