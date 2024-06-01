

from pyrogram import Client, filters, types, enums, errors


app = Client(
     api_id=os.getenv('api_id'),
     api_hash=os.getenv('api_hash'),
     bot_token=os.getenv('token')
)



PREFIX = ['.', '!', '/']




@app.on_message(filters.command(['start', 'help']))
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
          types.InlineKeyboardButton(text='𝗛𝗘𝗟𝗣 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦', callback_data=f"help:{uid}")
         ]])
     return await bot.send_message(
         chat_id=m.chat.id,
         text=text,
         reply_to_message_id=m.id,
         reply_markup=button
     )



@app.on_callback_query():
async def cb(app, query):
    data = query.data.split()[0]
    user_id = int(query.data.split()[1])
  
    if data == 'help':
        
        return await query.message.edit_text(
          text=f"""
➥ /gen <query>: for generate credit cards.
**Example**: `/gen 342663651415103`

➥ /fake <country code>: for generate random fake address.
**Example**: `/fake us`

➥ /bin <bin code>: for information about the bin codes.
**Example**: `/bin 464988

**More commands will coming soon 📢.          
          """




  
