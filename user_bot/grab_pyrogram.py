import sys
import time
from pyrogram import Client, filters
from pyrogram.errors import UsernameInvalid
from datetime import datetime
from grab_config import api_id, api_hash
from sqlalchemy.exc import PendingRollbackError
sys.path.append('bot')
from python.config import admin_chat_name, admin_chat
from database.sess import add_post_to_database, add_postS_to_database, rollback

Client = Client('test', api_id, api_hash)


@Client.on_message(filters.chat(admin_chat_name) & filters.command('add', prefixes='/'))
async def adding_me(Client, message):
    try:
        await Client.join_chat(message.text[18:])
    except UsernameInvalid:
        await Client.send_message(admin_chat_name, f"ERROR\n{message.text}")
        await Client.send_sticker(chat_id=admin_chat_name,
                                  sticker=r'CAACAgIAAxkBAAEEB9xiH1fp0016CIMxHCEWhR3RNgc2zgACWAADIjUTD18KQ-JwdxT7IwQ')

@Client.on_message(filters.channel)
async def echo(Client, message):
    if (str(time.strftime("%d.%m.%g %H:%M", time.gmtime())) == str(time.strftime("%d.%m.%g %H:%M",time.gmtime(message.date)))):
        chat_data = (await Client.get_chat(message.chat.id))
        chat_name =  chat_data["username"]
        if chat_name is None:
            link = chat_data["invite_link"]
            if link is None:
                try:
                    link = (((chat_data["pinned_message"])["caption_entities"])[1])["url"]
                except:
                    pass
        else:
            link = "https://t.me/" + chat_name
        try:
            chat_media_group = await Client.get_media_group(message.chat.id, message.message_id)
            messages = [i["message_id"] for i in chat_media_group]
            if await add_postS_to_database(link, messages):
                await Client.send_message(admin_chat_name, "/NEW_POST\n"
            f"{link}")
                await Client.forward_messages(chat_id=admin_chat, from_chat_id=message.chat.id, message_ids=messages)

        except ValueError:
            result = await add_post_to_database(link, message.message_id)
            if result:
                await Client.send_message(admin_chat_name, "/NEW_POST\n"
            f"{link}")
                await message.forward(int(admin_chat))
        except PendingRollbackError:
            await roolback()
Client.run()
