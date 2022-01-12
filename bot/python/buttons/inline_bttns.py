from aiogram import types

start_bttn = types.InlineKeyboardMarkup(row_width=2)

text_and_data = (
    ('Yes', 'yes'), ('No', 'no')
)
start_bttn.add(*(types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data))