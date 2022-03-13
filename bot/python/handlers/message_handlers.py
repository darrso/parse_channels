import os
import sys
import time
import aiogram.types
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
sys.path.append('bot')
from database.sess import get_users_by_link
from database.sess import create_new_user, check_on_off, switch_on_off, check_parse_channels, check_channel, \
    add_channels, reemove_channels
from python.States.StatesClasses import Adding, Removing
from python.config import bToken, admin_chat, admin_id

bot = Bot(token=bToken)


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
    if data:
        await message.answer(f'Here is the list of channels you are parsing:\n{data}\n\n'
                             f'Delete channel - /remove_parse_channel\n'
                             f'Add channel - /add_parse_channel\n'
                             f'Main menu - /menu')
    else:
        await message.answer("You are not parsing any channels yet.\n\nTo add channels send /add_parse_channel")


async def add_channel(message: types.Message):
    await message.answer("To add a new channel send LINK TO CHANNEL\n\n"
                         "Example:\n"
                         "https://t.me/test\n\n"
                         "P.S. The bot cannot join private channels.\n"
                         "You can add a channel to the list of those that you are parsing, but the bot will subscribe to it only after a while\n"
                         "(you will receive a notification about this)")

    await Adding.first.set()


async def adding_channel(message: types.Message, state: FSMContext):
    res = await check_channel(message.text, message.from_user.id)
    if res == 'NOT LINK!':
        await message.answer('This link is not working!\n'
                             'Try again - /add_parse_channel')
    elif res:
        await bot.send_message(chat_id=admin_chat, text="/add " + message.text)
        await add_channels(message.from_user.id, message.text)
        await message.answer('Successfully!\n\nSend /menu for main menu!')
    else:
        if await add_channels(message.from_user.id, message.text):
            await message.answer('Successfully!\n\nSend /menu for main menu!')
        else:
            await message.answer('This channel is already on your list!\n\n'
                                 'View a list of your channels - /parse_channels')
    await state.finish()


async def remove_channel(message: types.Message):
    data = (await check_parse_channels(message.from_user.id))
    if data == 'No one channels':
        await message.answer("You cannot remove telegram channels from the list, because you have not added any!\n\n"
                             "Checking the list of channels - /parse_channels")
    else:
        await message.answer("Choose number of channel and send it!\n"
                             "Example:\n"
                             "1\n\n"
                             f"Here is the list of channels you are parsing:\n{data}")
        await Removing.first.set()


async def removing_channel(message: types.Message, state: FSMContext):
    data = await reemove_channels(message.from_user.id, message.text)
    if data:
        await message.answer('Success!\n\n'
                             'List of your channels - /parse_channels')
    else:
        await message.answer('Error!\n\n'
                             'Try again - /remove_parse_channel\n'
                             'Main menu - /menu')
    await state.finish()


async def new_post(message: types.Message):
    try:
        time.sleep(2);
        if message.chat.id == admin_chat:
            if message.text[0:9] != "/NEW_POST":
                pass
            else:
                messageid = message.message_id + 1
                users = await get_users_by_link(message.text[10:])
                if users:
                    for i in users:
                        await bot.forward_message(chat_id=int(i), from_chat_id=(admin_chat), message_id=messageid)
                else:
                    pass
    except:
        pass
        


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(main_menu, commands="menu")
    dp.register_message_handler(switch_parametr, commands=['on', 'off'])
    dp.register_message_handler(parse_channel, commands="parse_channels")
    dp.register_message_handler(add_channel, commands='add_parse_channel')
    dp.register_message_handler(adding_channel, state=Adding.first)
    dp.register_message_handler(remove_channel, commands='remove_parse_channel')
    dp.register_message_handler(removing_channel, state=Removing.first)
    dp.register_channel_post_handler(new_post, lambda message: message.text[0:9] == "/NEW_POST")