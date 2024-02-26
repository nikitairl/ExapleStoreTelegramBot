from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Menu"),
            KeyboardButton(text="About"),
            KeyboardButton(text="Payment info"),
        ],
        [
            KeyboardButton(text="Shipping info"),
            KeyboardButton(text="Feedback"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="What do you want?",
)


del_kb = ReplyKeyboardRemove()
