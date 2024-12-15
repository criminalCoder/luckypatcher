
from pyrogram import Client,filters, enums, __version__
# from bot import Bot
from config import STREAM_LOGS
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from urllib.parse import quote_plus
from util.file_properties import get_name, get_hash
from config import *
from html import escape
from plugins.channel_post import generate_hash

# @Client.on_callback_query(filters.regex(r"^downstreamlink:"))
# async def handle_generate_stream_link(client: Client, query: CallbackQuery):
#     try:
#         # Extract file_id from callback_data
#         _, file_id = query.data.split(":")
#         user_id = query.from_user.id
#         username = query.from_user.mention

#         # Forward the file to the STREAM_LOGS channel to obtain a unique message
#         log_msg = await client.send_cached_media(
#             chat_id=STREAM_LOGS, 
#             file_id=file_id
#         )

#         # Generate stream and download links
#         file_name = quote_plus(get_name(log_msg))
#         lazy_stream = f"{URL}watch/{str(log_msg.id)}/{file_name}?hash={get_hash(log_msg)}"
#         lazy_download = f"{URL}{str(log_msg.id)}/{file_name}?hash={get_hash(log_msg)}"

#         # Send confirmation to the user
#         await query.message.edit_text(
#             text=f"🍿 ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ 🧩\n\n📂 File Name: {file_name}\n\n⏳ Direct Download Link:\n{lazy_download}\n\n📺 Watch Online:\n{lazy_stream}",
#             disable_web_page_preview=True,
#             reply_markup=InlineKeyboardMarkup(
#                 [
#                     [InlineKeyboardButton("web Download", url=lazy_download)],
#                     [InlineKeyboardButton('▶Stream online', url=lazy_stream)]
#                 ]
#             )
#         )
#     except Exception as e:
#         print(f"Error: {e}")
#         await query.answer(f"☣ Something went wrong\n\n{e}", show_alert=True)

# @Client.on_callback_query(filters.regex(r"^embedcode:"))
# async def handle_get_embed_code(client: Client, query: CallbackQuery):
#     try:
#         # Extract file_id from callback_data
#         _, file_id = query.data.split(":")

#         # Generate embed link
#         embed_url = f"{URL}embed/{file_id}?hash={get_hash(file_id)}"
#         embed_code = f"""
#         <div style="position: relative; padding-bottom: 56.25%; height: 0">
#             <iframe
#                 src="{embed_url}"
#                 scrolling="no"
#                 frameborder="0"
#                 allowfullscreen
#                 style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
#             >
#             </iframe>
#         </div>
#         """

#         # Send embed code to the user
#         await query.message.reply_text(
#             text=f"Here is your embed code:\n\n<code>{embed_code}</code>",
#             parse_mode="HTML",
#             disable_web_page_preview=True
#         )
#     except Exception as e:
#         print(f"Error: {e}")
#         await query.answer(f"☣ Something went wrong\n\n{e}", show_alert=True)


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"○ Dev : <a href='https://t.me/LazyDeveloperr'>❤LazyDeveloperr❤</a>\n○  Updates Channel: <a href='https://t.me/LazyDeveloper'> LazyDeveloper</a> </b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton("⚡️ ᴄʟᴏsᴇ", callback_data = "close"),
                    InlineKeyboardButton('🍁 ᴘʀᴇᴍɪᴜᴍ', url='https://t.me/LazyDeveloperr')
                    ]
                ]
            )
        )
    
    elif data.startswith("generate_stream_link"):
        # _, fileid = data.split(":")
        print("hit generate_stream_link callback")
        try:
            xo = await query.message.reply_text(f'🔐')
            user_id = query.from_user.id
            username =  query.from_user.mention 
            new_text = query.message.text
            print(f"new text => {new_text}")
            # Directly access the file from the callback query's associated message
            file = getattr(query.message.reply_to_message, query.message.reply_to_message.media.value)
            file_id = file.file_id
            # file_name = quote_plus(file.file_name)

            log_msg = await client.send_cached_media(
                chat_id=STREAM_LOGS, 
                file_id=file_id,
            )

            fileName = {quote_plus(get_name(log_msg))}
            lazy_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
            lazy_download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            
            await asyncio.sleep(1)
            await xo.delete()

            await log_msg.reply_text(
                text=f"🍿 ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ  🧩\n\n<blockquote>{new_text}</blockquote>\n<blockquote>⏳Direct Download link:\n{lazy_download}</blockquote>\n<blockquote>📺Watch Online\n{lazy_stream}</blockquote>\n🧩User Id: {user_id} \n👮‍♂️ UserName: {username}",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                                                    InlineKeyboardButton('▶Stream online', url=lazy_stream)]])  # web stream Link
            )
            
            await query.message.edit_text(
                text=f"🍿 ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ 🧩\n\n<blockquote>{new_text}</blockquote>\n<blockquote>⏳Direct Download link:\n{lazy_download}</blockquote>\n<blockquote>📺Watch Online\n{lazy_stream}</blockquote>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                        InlineKeyboardButton('▶Stream online', url=lazy_stream)
                    ],
                    [
                        InlineKeyboardButton("<> Get EMBED code </>", callback_data="get_embed_code")
                    ]
                    ])  # web stream Link
            )
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong sweetheart\n\n{e}", show_alert=True)
            return 
    
    elif data.startswith("get_embed_code"):
        # _, fileid, = data.split(":")
        # print('Hit me 1')
        try:
            xo = await query.message.reply_text(f'🔐')

            file = getattr(query.message.reply_to_message, query.message.reply_to_message.media.value)
            fileid = file.file_id

            log_msg = await client.send_cached_media(
                chat_id=STREAM_LOGS, 
                file_id=fileid,
            )

            fileName = {quote_plus(get_name(log_msg))}
            # print(f'Hit me 1 {fileName}')
            
            # Generate the embed URL
            lazy_embed = f"{URL}embed/{str(log_msg.id)}?hash={get_hash(log_msg)}"
            print(f'Hit me 1 = {lazy_embed}')
            # Create the HTML embed code
            embed_code = f"""
<div style="position: relative; padding-bottom: 56.25%; height: 0">
    <iframe
        src="{lazy_embed}"
        scrolling="no"
        frameborder="0"
        webkitallowfullscreen
        mozallowfullscreen
        allowfullscreen
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%">
    </iframe>
</div>
            """
            print(f'Hit me 1 {embed_code}')
            escaped_embed_code = escape(embed_code)  # Escapes special characters
            # Send the embed code to the user
            await asyncio.sleep(1)
            await xo.delete()

            await query.message.reply_text(
                text=f"👩‍💻 Here is your embed code:\n\n<blockquote><code>{escaped_embed_code}</code></blockquote>",
                quote=True,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            print(e)
            await query.answer(f"☣ Unable to generate embed code\n\n{e}", show_alert=True)
    
    elif data.startswith("convert_link"):

        try:
            xo = await query.message.reply_text(f'🔐')

            original_link = query.message.text
           
            log_msg = await client.send_message(
                chat_id=STREAM_LOGS, 
                text=original_link,
            )

            await asyncio.sleep(1)
            await xo.delete()
            secure_hash = generate_hash(log_msg.id)
            print(f"generated secure hash ==> {secure_hash}")
            stream_url = f"{URL}play/{secure_hash}{str(log_msg.id)}?hash={secure_hash}"
            await query.message.reply_text(
                text=f"✅ Your streamable link is ready:\n\n[🔗 Watch Now]({stream_url})",
                quote=True,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(1)
            await client.send_message(
                    chat_id=STREAM_LOGS,
                    text=f"✅ Converted Link for User:\n🔗 Original: {original_link}\n🌐 Stream: {stream_url}"
                )
            
            await query.answer("✅ Link converted successfully!")
        except Exception as e:
            print(e)
            await query.answer(f"☣ Unable to generate  link\n\n{e}", show_alert=True)

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

