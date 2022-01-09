from aiogram import types
from aiogram.types import KeyboardButton

yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
yes_no.add(KeyboardButton('Yes'), KeyboardButton('No'))