﻿from aiogram.types import KeyboardButton
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
            KeyboardButton("GitHub", web_app=WebAppInfo(url = "https://github.com/zeotq/b2c_bot4b"))
        ],
        [
            KeyboardButton(text="Закрыть")
        ],
]
kb_admin = [
    [
        KeyboardButton(text = "get_user_by_id"),
        KeyboardButton(text = "add_comment"),
        KeyboardButton(text = "set_trustfactor")
        ]
]