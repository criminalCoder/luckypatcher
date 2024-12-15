
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

import hashlib
import hmac

# Define a secret key for hash generation (keep it private!)
SECRET_KEY = "theoneandonlylazydeveloper"  # Replace with a strong, unique key

def generate_hash(log_msg_id):
    """
    Generate a secure hash for a given log message ID.
    """
    # Encode the log_msg_id and secret key
    log_msg_id_bytes = str(log_msg_id).encode()
    secret_key_bytes = SECRET_KEY.encode()

    # Create the hash using HMAC with SHA256
    hash_digest = hmac.new(secret_key_bytes, log_msg_id_bytes, hashlib.sha256).hexdigest()
    return hash_digest[:10]  # Use the first 10 characters for compactness

def validate_hash(log_msg_id, provided_hash):
    """
    Validate the provided hash against the expected hash for the given log_msg_id.
    """
    # Generate the expected hash for the given log_msg_id
    expected_hash = generate_hash(log_msg_id)

    # Compare the provided hash with the expected hash
    return hmac.compare_digest(expected_hash, provided_hash)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio) & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')],
        [InlineKeyboardButton("📂Downolad / Stream🍿", callback_data=f'generate_stream_link')],
        [InlineKeyboardButton("<> Get EMBED code </>", callback_data=f'get_embed_code')]
        ]
        )

    await reply_text.edit(f"<b>📂Telegram File Link:</b>\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    # if not DISABLE_CHANNEL_BUTTON:
    #     await post_message.edit_reply_markup(reply_markup)

@Client.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
