from aiogram import types

kb_1 = [
        [
            types.KeyboardButton(text="/drone"),
            types.KeyboardButton(text="/help"),
            types.KeyboardButton(text="/close")
        ],
]
kb_2 = [
        [
            types.KeyboardButton(text="/place"),
            types.KeyboardButton(text="/orders"),
            types.KeyboardButton(text="/cancel")
        ],
        [
            types.KeyboardButton(text="/close")
        ],
]
kb_admin = [
    [
        types.KeyboardButton(text = "get_user_by_id"),
        types.KeyboardButton(text = "add_comment"),
        types.KeyboardButton(text = "set_trustfactor")
        ]
]