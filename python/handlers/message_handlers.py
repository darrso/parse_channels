from aiogram import types, Dispatcher


async def start_command(message: types.Message):
    await message.answer("Hey!\n"
                         "I am a parser for telegram channels.\n\n"
                         "For the main menu, send - /menu.\n"
                         "Everything will be written in detail there.")

    await message.answer_sticker(r'CAACAgIAAxkBAAIKpWHbI3SOA4e7-YIUHXhsSBNwUoWTAAIZAAMB9dsukz3Jt5gbPdEjBA')


async def main_menu(message: types.Message):
    await message.answer(f"Welcome to the main menu, {message.from_user.username}!\n"
                         f"I am a bot that parses telegram channels.\n\n"
                         "Here are my commands:\n"
                         "/menu - main menu\n"
                         "/parse_channels - a list of channels you are following\n"
                         "/add_parse_channel - add to the channel list\n"
                         "/remove_parse_channel - remove a channel from the list\n"
                         "/off - turn off parsing of your channels\n"
                         "/on - enable parsing of your channels\n\n"
                         "My creator is @darrso")
    await message.answer_sticker(r'CAACAgIAAxkBAAIKrmHbJw6ckgI0IrCLe_TJrbUyCJ_xAALRAAM27BsFCW1Sl32PAAEsIwQ')


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(main_menu, commands="menu")
