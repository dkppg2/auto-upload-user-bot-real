import os
import sys

from pyrogram import Client, filters, types
from database import db
from bot import User
from config import CHANNELS, LIST_TEMPLATE, OWNER_ID


@User.on_message(filters.command("start", prefixes="!"))
async def start_cmd_handler(c: Client, m: types.Message):
    await m.edit("Hey, Wassup!")


@User.on_message(filters.command("restart", prefixes="!") & filters.user(OWNER_ID))
async def restart_cmd_handler(c: Client, m: types.Message):
    restart()


@User.on_message(filters.command("view_list", prefixes="!") & filters.user(OWNER_ID))
async def view_list_cmd_handler(c: Client, m: types.Message):
    __temp = []
    for channel in CHANNELS:
        if channel not in __temp:
            list_text = await db.get_lists(channel["channel_name"])
            await m.reply(LIST_TEMPLATE.format(list_text))
            __temp.append(channel["channel_name"])

@User.on_message(filters.command("send_list", prefixes="!") & filters.user(OWNER_ID))
async def view_list_cmd_handler(c: Client, m: types.Message):
    editable = await m.edit("Broadcasting lists")
    for channel in CHANNELS:
        list_text = await db.get_lists(channel["channel_name"])
        for channel_id in channel["channel_id"]:
            await c.send_message(chat_id=channel_id, text=list_text)
    await editable.edit("Done")

def restart():
    os.execv(sys.executable, ['python'] + sys.argv)

