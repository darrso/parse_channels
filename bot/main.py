import asyncio

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from python.config import bToken
from python.handlers.message_handlers import register_message_handlers


async def main():
    bot = Bot(token=bToken)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_message_handlers(dp)

    await dp.start_polling()


if __name__ == '__main__':
    print('Bot started')
    asyncio.run(main())
