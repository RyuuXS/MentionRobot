import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("__**Saya Adalah MentionAll Bot**, Saya Dapat Membantu Anda Mention Semua Member 👻\nClick **/help** Untuk Infromasi Lebih Lanjut__\n\n Maintaned By @RyuuShinni",
                    buttons=(
                      [Button.url('⚜️ Channel', 'https://t.me/Belajarbersamaryuu'),
                      Button.url('👑 OWNER', 'https://t.me/RYUUSHINNI')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of MentionAllBot**\n\nCommand: /all\n__You can use this command with text what you want to mention others.__\n`Example: /all Jangan Lupa Sholat!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nFollow [SHIN](https://github.com/RyuuXS) on Github"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('⚜️ Channel', 'https://t.me/Belajarbersamaryuu'),
                      Button.url('👑 Groub', 'https://t.me/helpforRYUU')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Only admins can mention all!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')
        
print(">> BOT STARTED <<")
client.run_until_disconnected()
