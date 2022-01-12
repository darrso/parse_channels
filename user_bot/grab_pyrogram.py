from pyrogram import Client, filters

from grab_config import api_id, api_hash

Client = Client('test', api_id, api_hash)


@Client.on_message(filters.chat(['test_darr', 'test_darr_2']))
async def my_handler(Client, message):
    await Client.send_message("me", message.text)


Client.run()
