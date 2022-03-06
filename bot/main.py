import asyncio

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from python.handlers.broadcast import register_broadcast_handlers
from python.config import bToken
from python.handlers.message_handlers import register_message_handlers

async def set_commands(bot: Bot):
    await bot.set_my_commands(
        [BotCommand(command="/menu", description='main menu'),
         BotCommand(command="/parse_channels", description='a list of channels you are following'),
         BotCommand(command="/add_parse_channel", description='add to the channel list'),
         BotCommand(command="/remove_parse_channel", description='remove a channel from the list'),
         BotCommand(command="/off", description='turn off parsing of your channels'),
         BotCommand(command="/on", description='enable parsing of your channels')
         ]
    )
async def main():
    bot = Bot(token=bToken)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_message_handlers(dp)
    register_broadcast_handlers(dp)
    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    print('Bot started')
    asyncio.run(main())
