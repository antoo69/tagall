# A Powerful Music And Management Bot
# Property Of Rocks Indian Largest Chatting Group
# Rocks © Rocks
# Owner: Asad Ali + Kattai Massom + Abhimanyu Singh

import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, ChannelParticipantsAdmins
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO, format="%(name)s - [%(levelname)s] - %(message)s"
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID", ""))
api_hash = os.environ.get("API_HASH", "")
bot_token = os.environ.get("TOKEN", "")
client = TelegramClient("client", api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

# Admins and Owners
ADMIN_IDS = [123456789, 8877665533]  # Ganti dengan ID Telegram admin
OWNER_IDS = [989898989]  # Ganti dengan ID Telegram owner

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    chat_id = event.chat_id
    if not event.is_private:
        return await event.respond("I am alive!")
    await event.reply(
        "Hello! I am a bot to help you mention all group members in Telegram.\nRun /help for more information.",
        link_preview=False
    )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
    chat_id = event.chat_id
    if not event.is_private:
        return await event.respond("Please start me in private to use this command.")
    helptext = (
        "Help Menu:\n\n"
        "Commands:\n"
        "/mentionall - Mention all members in the group.\n"
        "/cancel - Cancel an ongoing process.\n"
        "/admin - Mention all admins in the group.\n\n"
        "You can use these commands with a custom message or as a reply to another message."
    )
    await event.reply(helptext, link_preview=False)

@client.on(events.NewMessage(pattern="^/utag ?(.*)"))
async def mentionall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("This command can only be used in groups or channels.")

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            is_admin = True
    if not is_admin:
        return await event.respond("Only admins can mention all.")

    message = event.pattern_match.group(1) or (await event.get_reply_message())
    if not message:
        return await event.respond("Please provide a message or reply to one.")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(chat_id):
        if chat_id not in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
        if usrnum == 5:
            await client.send_message(chat_id, f"{usrtxt}\n\n{message}")
            usrnum = 0
            usrtxt = ""
            await asyncio.sleep(2)
    spam_chats.remove(chat_id)

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
    if event.chat_id not in spam_chats:
        return await event.respond("No process is ongoing.")
    spam_chats.remove(event.chat_id)
    await event.respond("Process stopped.")

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
    chat_id = event.chat_id
    if not event.is_private:
        return await event.respond("Gunakan perintah /help untuk melihat perintah tagall pada bot")
    helptext = """<blockquote>✪ Menu Ferdi Mention Bot

✪ Command: /utag untuk memulai proses tagall.
✪ Command: /cancel untuk menghentikan proses tagall.
✪ Command /atag untuk memanggil semua admin di group.
✪ Anda bisa menggunakan bot ini di group anda.
✪ Contoh: /utag Good Morning atau /utag reply pesan.
✪ Anda bisa menggunakan perintah /utah dengan menambahkan teks atau reply pesan </blockquote>"""
    await event.reply(helptext)

@client.on(events.NewMessage(pattern="^/owner$"))
async def owner(event):
    chat_id = event.chat_id
    if not event.is_private:
        return await event.respond("Please wait .... ")
    ownertext = """✪ Menu Owner Bot Mention

✪ Saya [ᴮ⃮⃯˅• ꜰ໑ʀᴆɪ! ᴅԍ⃮⃯⃖⃗ᴙᴤ°](https://t.me/fsyrl9) Owner
✪ 
✪ Store [Ferdi Store!](https://t.me/Galerifsyrl)
✪ Info bot lain kunjungi [Ferdi Support](https://t.me/FerdiSupport)"""
    await event.reply(ownertext)

@client.on(events.NewMessage(pattern="^/atag ?(.*)"))
async def mention_admins(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("Hanya untuk memanggil admin group")

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            is_admin = True
    if not is_admin:
        return await event.respond("hanya admin yang bisa menggunakan perintah tersebut")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("Berikan saya teks")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond(
                "Tambahkan Saya di group anda dan jadikan saya admin."
            )
    else:
        return await event.respond(
            "Balas pesan atau beri saya beberapa teks untuk menyebutkan orang lain"
        )

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    chat = await event.get_input_chat()
    async for x in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f" \n {x.first_name}"
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{usrtxt}\n\n{msg}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


print("Bot is running...")
client.run_until_disconnected()
