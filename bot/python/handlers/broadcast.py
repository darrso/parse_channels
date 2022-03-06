import sys
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram_broadcaster import TextBroadcaster, MessageBroadcaster
sys.path.append('bot')
from database.sess import get_users_by_link, get_all_users
from python.States.StatesClasses import Broadcast
from python.config import admin_id


async def broadcast_command(message: types.Message):
    if str(message.from_user.id) == admin_id:
        await message.answer('Enter text:\n\n'
                             'Example:\n'
                             "Channel Durov's Channel - parsing from now on\n\n"
                             "send CANCEL if you do not want to send mailing to users")
        await Broadcast.first.set()


async def get_href(message: types.Message, state: FSMContext):
    if message.text.upper() == "CANCEL":
        await state.finish()
        await message.answer("You have canceled the mailing list!\n\n"
                             "Main menu - /menu")
    else:
        await state.update_data(text=message.text)
        await message.answer('Enter link to channel(or send NO):')
        await Broadcast.next()


async def send_broadcast(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    if message.text.lower() != 'no':
        users = await get_users_by_link(message.text)
        await TextBroadcaster(users, f'{data["text"]}\n\nLink to channel:\n{message.text}').run()
        await message.answer(f"Received mailing: {len(users)} users")
    else:
        users = await get_all_users()
        await TextBroadcaster(users, text=data['text']).run()
        await message.answer(f"Received mailing: {len(users)} users")


def register_broadcast_handlers(dp: Dispatcher):
    dp.register_message_handler(broadcast_command, commands="broadcast")
    dp.register_message_handler(get_href, state=Broadcast.first)
    dp.register_message_handler(send_broadcast, state=Broadcast.second)