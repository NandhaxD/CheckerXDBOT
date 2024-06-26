

from pyrogram import Client, filters, types, enums, errors
from utils import *

import os
import logging
import asyncio
import requests


######################################################################################################################################################


BOT_INFO = requests.get(f'https://api.telegram.org/bot{os.getenv('token')}/getme').json()['result']
BOT_ID = BOT_INFO['id']
BOT_USERNAME = BOT_INFO['username']
BOT_NAME = BOT_INFO['first_name']

PREFIX = ['.', '!', '/']
CHANNEL = "NandhaBots"

######################################################################################################################################################

FORMAT = f"[{BOT_NAME}] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
              logging.StreamHandler()], format=FORMAT)


######################################################################################################################################################


app = Client(
     name=BOT_NAME,
     api_id=os.getenv('api_id'),
     api_hash=os.getenv('api_hash'),
     bot_token=os.getenv('token')
)

######################################################################################################################################################




@app.on_message(filters.command(['start', 'help'], prefixes=PREFIX))
async def start(app, message):
     m = message
     if not m.from_user:
         return
     mention = m.from_user.mention()
     uid = m.from_user.id
     text = f"""
     **Hello user!, {mention} to know my command hit the help button.**
     """
     button = types.InlineKeyboardMarkup([[
          types.InlineKeyboardButton(text='Commands 🔐', callback_data=f"help:{uid}"),
          types.InlineKeyboardButton(text='⛔', callback_data=f"close:{uid}"),],[
          types.InlineKeyboardButton(text='Channel 📢', url=f"{CHANNEL}.t.me")
         ]])
     return await app.send_message(
         chat_id=m.chat.id,
         text=text,
         reply_to_message_id=m.id,
         reply_markup=button
     )


######################################################################################################################################################


@app.on_callback_query()
async def callback_data(app, query):
    data = query.data.split(':')[0]
    uid = int(query.data.split(':')[1])

    if query.from_user.id != uid:
           return await query.answer(
               "Don't stalk others requests. 💀"
           )
          

    button = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text='⛔', callback_data=f"close:{uid}")]])
    if data == "help":
        await query.message.edit_text(
          text=f"""
**✨ Commands**:

➥ /gen <credit card>: for generate credit cards.
✪ **Example**: `/gen 342663651415103`

➥ /fake <country code>: for generate random fake address.
✪ **Example**: `/fake us`

➥ /chk <credit card>: for check credit card live or dead.
✪ **Example**: `/chk 4742899000125575|11|2027|603`

➥ /bin <bin code>: for information about the bin codes.
✪ **Example**: `/bin 464988`

🔜 **More commands will coming soon **📢.          
          """, reply_markup=button, parse_mode=enums.ParseMode.MARKDOWN)
    elif data == "close":
        await query.message.delete()
        await query.answer('⛔ Deleted!')
        
######################################################################################################################################################


@app.on_message(filters.command('gen', prefixes=PREFIX))
async def cc_generator(app, message):

     m = message
     
     usage = (
       "**❌ Wrong formatting, use /gen bin_code**"
     )
          
     if not message.from_user:
         return
     else:
        if len(m.text.split()) < 2:
             return await m.reply_text(text=usage)
        try:
          bin_code = int(m.text.split()[1][:6])
          limit = int(m.text.split()[2]) if len(m.text.split()) > 2 else False
        except (ValueError, IndexError):
           return await m.reply_text(text=usage)

        msg = await m.reply_text(text="**Generating please wait...**", quote=True)
       
        uid = m.from_user.id
       
        
        data = Checker.generator(bin_code, limit) if limit else Checker.generator(bin_code)
        bin_data = Checker.bin_check(bin_code)
       
        if not data:
           return await msg.edit_text(
             "Uff Something went wrong 🥺"
           )
        text = (
           f"𝗕𝗜𝗡 ➞  <code>{bin_code}</code>\n"
           f"𝗔𝗺𝗼𝘂𝗻𝘁 ➞ <code>{10 if limit == False else limit}</code>\n\n"
        )
        for cc in data:
            date, year = cc['expiration_date'].split('/')              
            text += f"<code>{cc['card_number']}|{date}|{year[2:]}|{cc['cvv']}</code>\n"

        if bin_data:
            text += "\n\n𝗕𝗜𝗡 𝗔𝗱𝗱𝗿𝗲𝘀𝘀:\n"
            for key, value in bin_data.items():
               text += f"➩ <b>{key.capitalize()}</b>: <code>{value}</code>\n"
              
        text += f"\n\n<b>✨ Made by {app.me.mention}</b>"
        button = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text='⛔', callback_data=f"close:{uid}")]])
       
        return await msg.edit_text(
          text=text, 
          parse_mode=enums.ParseMode.HTML,
          reply_markup=button
        )

######################################################################################################################################################


@app.on_message(filters.command('fake', prefixes=PREFIX))
async def fake_adress(app, message):
      
     m = message
     
     if not m.from_user:
         return
     
     country = m.text.split()[1] if len(m.text.split()) == 2 else False
     uid = m.from_user.id
     button = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text='⛔', callback_data=f"close:{uid}")]])

     msg = await m.reply_text(
         "**Generating please wait.....**"
     )
  
     data = Checker.fake(country) if country else Checker.fake()
       
     if not data:
           return await msg.edit_text(
             "Uff Something went wrong 🥺"
           )

     text = '𝗥𝗮𝗻𝗱𝗼𝗺 𝗙𝗮𝗸𝗲 𝗔𝗱𝗱𝗿𝗲𝘀𝘀:\n\n'
     for key, value in data.items():
         text += f"<b>{key.capitalize()}</b>: <code>{value}</code>\n"

     text += f"\n<b>✨ Made by {app.me.mention}</b>"
     return await msg.edit_text(
          text=text, 
          parse_mode=enums.ParseMode.HTML,
          reply_markup=button
     )
  
        
######################################################################################################################################################


@app.on_message(filters.command('bin', prefixes=PREFIX))
async def bin_checker(app, message):
     m = message
     
     usage = (
       "**❌ Wrong formatting, use /bin bin_code**"
     )
          
     if not m.from_user:
         return
     
     bin_code = m.text.split()[1] if len(m.text.split()) == 2 else False
     uid = m.from_user.id
     button = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text='⛔', callback_data=f"close:{uid}")]])

     msg = await m.reply_text(
         "**Checking please wait....**"
     )
     if not bin_code:
         return await msg.edit_text(usage)
       
     try:
        bin_code = int(bin_code[:6])
     except ValueError:
         return await msg.edit_text(usage)

     data = Checker.bin_check(bin_code)
  
     if not data:
           return await msg.edit_text(
             "Uff Something went wrong 🥺"
           )

     text = '𝗕𝗜𝗡 𝗔𝗱𝗱𝗿𝗲𝘀𝘀:\n\n'
     for key, value in data.items():
          text += f"<b>{key.capitalize()}</b>: <code>{value}</code>\n"
       
     text += f"\n<b>✨ Made by {app.me.mention}</b>"
     return await msg.edit_text(
          text=text, 
          parse_mode=enums.ParseMode.HTML,
          reply_markup=button
     )
     
  
######################################################################################################################################################


@app.on_message(filters.command(['chk','check'], prefixes=PREFIX))
async def checker(app, message):
     m = message
     
     usage = (
       "**❌ Wrong formatting**,\n```Example:\n/chk 4569332809704994|08|28|490```"
     )

     if not m.from_user:
         return
     elif not len(m.text.split()) > 1:
          return await m.reply_text(usage)

     msg = await m.reply_text("**⏳ Checking....**")
     cc = m.text.split(None, 1)[1]
     data = Checker.checker(cc)
     if not data:
         return await msg.edit("**👀 the credit card type is invalid.**")
     text = f"""
**𝗕𝗜𝗡**: `{data['cc_number'][:6]}`

**𝗖𝗿𝗲𝗱𝗶𝘁 𝗰𝗮𝗿𝗱**: {data['cc_number']}
**𝗕𝗮𝗻𝗸 𝗡𝗮𝗺𝗲**: {data['bank_name']}
**𝗦𝘁𝗮𝘁𝘂𝘀**: {data['status']}

**✨ Made By {app.me.mention}**
"""
     return await msg.edit(text)

######################################################################################################################################################


app.run()
  
