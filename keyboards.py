from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo

kb_main = [
        [
            KeyboardButton(text="Заказ такси 🚖"),
            KeyboardButton(text="Доставка еды 🥂"),
        ],
        [
            KeyboardButton(text="Информация о проекте"),
        ],
        [
            KeyboardButton("GitHub", web_app=WebAppInfo(url = "https://github.com/zeotq/b2c_bot4b.git"))
        ],
        [
            KeyboardButton(text="Закрыть")
        ],
]
kb_taxi_0 = [
    [
        KeyboardButton(text="Регистрация")],
    [
        KeyboardButton(text="Закрыть")]]

kb_taxi_1 = [
    [KeyboardButton(text="Заказать такси")]]


kb_admin = [
    [
        KeyboardButton(text = "get_user_by_id"),
        KeyboardButton(text = "add_comment"),
        KeyboardButton(text = "set_trustfactor")
        ]
]


keyboard_main_menu = ReplyKeyboardMarkup(
    keyboard=kb_main,
    resize_keyboard=True,
)
keyboard_admin = ReplyKeyboardMarkup(
    keyboard=kb_admin,
    resize_keyboard=True,
)
keyboard_taxi_0 = ReplyKeyboardMarkup(
    keyboard=kb_taxi_0,
    resize_keyboard=True,
)
keyboard_taxi_1 = ReplyKeyboardMarkup(
    keyboard=kb_taxi_1,
    resize_keyboard=True,
)