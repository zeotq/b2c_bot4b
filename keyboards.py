from tkinter.tix import ROW
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo

kb_main = [
        [
            KeyboardButton(text="Заказ такси 🚖"),
            KeyboardButton(text="Доставка еды 🥂"),
        ],
        [
            KeyboardButton(text="/help"),
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
    [
        KeyboardButton(text="Номер телефона", request_contact=True),
        KeyboardButton(text="Имя"),
    ],
    [
        KeyboardButton(text="Закрыть")    
    ]
]

kb_taxi_2 = [
    [
        KeyboardButton(text="Номер телефона", request_contact=True),
        KeyboardButton(text="Имя"),
    ],
    [
        KeyboardButton(text="Закрыть"),
        KeyboardButton(text="Сохранить")    
    ]
]

kb_taxi_main = [
    [
        KeyboardButton(text="Вызвать такси", request_location=True),
    ],
    [
        KeyboardButton(text="Изменить данные"),
        KeyboardButton(text="Закрыть")
    ]
]


kb_admin = [
    [
        KeyboardButton(text = "get_user_by_id"),
        KeyboardButton(text = "add_comment"),
        KeyboardButton(text = "set_trustfactor")
    ]
]

kb_commode = [
        InlineKeyboardButton(text = "Вежливый", callback_data='good'),
        InlineKeyboardButton(text = "Ханыга (Илья)", callback_data='stupid'),
        InlineKeyboardButton(text = "Слишком вежливый", callback_data='bad')
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
keyboard_taxi_reg = ReplyKeyboardMarkup(
    keyboard=kb_taxi_1,
    resize_keyboard=True,
)
keyboard_taxi_reg_finish = ReplyKeyboardMarkup(
    keyboard=kb_taxi_2,
    resize_keyboard=True,
)
keyboard_taxi_main = ReplyKeyboardMarkup(
    keyboard=kb_taxi_main,
    resize_keyboard=True,
)
keyboard_commode = InlineKeyboardMarkup(
    row_width=1
)
keyboard_commode.add(kb_commode[0], kb_commode[1], kb_commode[2])
