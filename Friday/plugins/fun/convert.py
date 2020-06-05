from friday import friday, Message


@friday.on_cmd("small", about={
    'header': "Make caps smaller",
    'usage': "{tr}small [text | reply to msg]"})
async def small_(message: Message):
    text = message.input_str
    if message.reply_to_message:
        text = message.reply_to_message.text
    if not text:
        await message.err("input not found")
        return
    await message.edit(text.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                                    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢ")))


@friday.on_cmd("lower", about={
    'header': "Convert text to lowwer",
    'usage': "{tr}lower [text | reply to msg]"})
async def lower_(message: Message):
    text = message.input_str
    if message.reply_to_message:
        text = message.reply_to_message.text
    if not text:
        await message.err("input not found")
        return
    await message.edit(text.lower())


@friday.on_cmd("upper", about={
    'header': "Convert text to upper",
    'usage': "{tr}upper [text | reply to msg]"})
async def upper_(message: Message):
    text = message.input_str
    if message.reply_to_message:
        text = message.reply_to_message.text
    if not text:
        await message.err("input not found")
        return
    await message.edit(text.upper())
