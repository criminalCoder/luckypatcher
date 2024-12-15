# from bot import Bot
from pyrogram import filters, Client
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import hashlib
from config import *

@Client.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Client, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))


# @Client.on_message(filters.private & filters.incoming)
# async def useless(_,message: Message):
#     if USER_REPLY_TEXT:
#         await message.reply(USER_REPLY_TEXT)




# Dictionary to temporarily store links


# Generate a unique hash for the link
def generate_hash(link):
    return hashlib.sha256(link.encode()).hexdigest()[:10]

@Client.on_message(filters.private & filters.text)
async def receive_link(client: Client, message: Message):
    """
    Handle when the user sends a link to the bot.
    """
    user_id = message.from_user.id
    link = message.text.strip()

    # Validate link format (basic validation)
    if not link.startswith("http"):
        await message.reply("❌ Invalid link. Please send a valid URL.")
        return

    # Forward the link to the Stream Log Channel
    log_message = await client.send_message(
        chat_id=STREAM_LOGS,
        text=f"🔗 Received Link from User ID {user_id}:\n{link}"
    )

    # Store the link in the dictionary using the log message ID as a reference
    stream_links[log_message.id] = link

    # Send a button to the user to convert the link
    await message.reply(
        "✅ Link received! Click the button below to convert it to a streamable link.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Convert to New Stream Link", callback_data=f"convert_link")]]
        )
    )

