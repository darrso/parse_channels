from aiogram import types, Dispatcher

from bot.database.sess import create_new_user, check_on_off, switch_on_off, check_parse_channels


async def start_command(message: types.Message):
    await message.answer("Hey!\n"
                         "I am a parser for telegram channels.\n\n"
                         "For the main menu, send - /menu.\n"
                         "Everything will be written in detail there.")

    await message.answer_sticker(r'CAACAgIAAxkBAAIKpWHbI3SOA4e7-YIUHXhsSBNwUoWTAAIZAAMB9dsukz3Jt5gbPdEjBA')

    # ДОБАВЛЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ
    await create_new_user(message.from_user.id, message.from_user.username, 'off')


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
                         f"P.S. now - {await check_on_off(message.from_user.id)}\n\n"
                         "My creator is @darrso")
    await message.answer_sticker(r'CAACAgIAAxkBAAIKrmHbJw6ckgI0IrCLe_TJrbUyCJ_xAALRAAM27BsFCW1Sl32PAAEsIwQ')


async def switch_parametr(message: types.Message):
    text = (message.text).replace("/", "")
    if text == 'on':
        await switch_on_off('on', message.from_user.id)
    elif text == 'off':
        await switch_on_off('off', message.from_user.id)
    await message.answer(f'Parameter changed to: {text}'
                         f'\nSend /menu to check it out!')


async def parse_channel(message: types.Message):
    data = (await check_parse_channels(message.from_user.id))
    await message.answer(f'Here is the list of channels you are parsing:\n{data}')


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(main_menu, commands="menu")
    dp.register_message_handler(switch_parametr, commands=['on', 'off'])
    dp.register_message_handler(parse_channel, commands="parse_channels")
