import sys
from pyrogram import Client, filters
from pyrogram.errors import UsernameInvalid

from grab_config import api_id, api_hash

sys.path.append('bot')
from python.config import admin_chat_name

Client = Client('test', api_id, api_hash)


@Client.on_message(filters.chat(admin_chat_name) & filters.command('add', prefixes='/'))
async def adding_me(Client, message):
    try:
        await Client.join_chat(message.text[18:])
    except UsernameInvalid:
        await Client.send_message(admin_chat_name, f"ERROR\n{message.text}")
        await Client.send_sticker(chat_id=admin_chat_name,
                                  sticker=r'CAACAgIAAxkBAAEEB9xiH1fp0016CIMxHCEWhR3RNgc2zgACWAADIjUTD18KQ-JwdxT7IwQ')


Client.run()
