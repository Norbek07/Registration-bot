from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💻 Computers"),KeyboardButton(text="📱 Phones")],
        [KeyboardButton(text="💁🏻‍♂️ About us"),KeyboardButton(text="📍 Location")],
        [KeyboardButton(text="☎️ Contact admin")]

    ],
    resize_keyboard=True,
    input_field_placeholder="Choise button..."
)
computers = [
    "Mackbook",
    "Lenovo",
    "HP",
    "ASUS",
    "Victus",
    "ACER",
    "Samsung"
]

computers_info = {
    "Mackbook":{"photo":"https://univershop.uz/wp-content/uploads/2023/10/3-2.jpg","price":1200,"color":"Black"},
    "Lenovo":{"photo":"https://apexdeals.com/wp-content/uploads/2019/12/61CprQzNyML._SL1000_.jpg","price":500,"color":"white or black"},
    "HP":{"photo":"https://ekb.wadoo.ru/upload/iblock/1b8/1b8fa2b22bc78cefb258ec3af62e5584.png","price":700,"color":"white or blue"},
    "ASUS":{"photo":"https://u-begemota.ru/wa-data/public/shop/products/52/99/108339952/images/89636/89636.750x0.jpg","price":1100,"color":"black"},
    "Victus":{"photo":"https://m.media-amazon.com/images/I/71TN45+oJ0L._AC_UF1000,1000_QL80_.jpg","price":850,"color":"white, blue or black"},
    "ACER":{"photo":"https://cdn1.ozone.ru/s3/multimedia-6/6274282638.jpg","price":870,"color":"black or white"},
    "Samsung":{"photo":"https://www.enkey.it/wp-content/uploads/2020/07/Samsung-Galaxy-Book-Ion-e1571758899774-scaled.jpg","price":959,"color":"blue"},

}

computer_button = ReplyKeyboardBuilder()

for computer in computers:
    computer_button.add(KeyboardButton(text=computer))

computer_button.adjust(2,repeat=True)
computer_button.row(KeyboardButton(text="🔙 ortga"))
computer_button = computer_button.as_markup(resize_keyboard=True,input_field_placeholder="Choise computer...")


phones = [
    "Iphone",
    "Samsung s24",
    "Artel",
    "Redmi",
    "Oppo"
]

phones_info = {
    "Iphone":{"photo":"https://www.iphones.ru/wp-content/uploads/2023/08/iPhone-15-Pro-Colors-Mock-Feature.jpg","price":1200,"color":"Black"},
    "Samsung s24":{"photo":"https://lh6.googleusercontent.com/cUOt5ircjGf1UfMp11OQKP-JzCDc59S_E-Gg-vHBGqqcRlFEnWE80Jj73B5lviSl6OarM5KwJD0I_7Jkq7F1TeGXQsMsa4FR9E9l5rMBHgDFVXjR2ulvBKtTHYycOFLZ8hZm-86e", "price":1200,"color":"Black"},
    "Artel":{"photo":"https://artelgroup.org/upload/articles/0_n85jsdC.png","price":1200,"color":"Black"},
    "Redmi":{"photo":"https://prostoreshop.ru/upload/iblock/1b7/mhz49f9nuiv94iwuugxhi16lh8r9vzpy.jpg","price":1200,"color":"Black"},
    "Oppo":{"photo":"https://www.deepspecs.com/wp-content/uploads/2020/05/1-oppo-a92-deepspecs-com.jpg","price":1200,"color":"Black"},
}

phone_button = ReplyKeyboardBuilder()

for phone in phones:
    phone_button.add(KeyboardButton(text=phone))

phone_button.adjust(2,repeat=True)
phone_button.row(KeyboardButton(text="🔙 ortga"))
phone_button = phone_button.as_markup(resize_keyboard=True,input_field_placeholder="Choise computer...")