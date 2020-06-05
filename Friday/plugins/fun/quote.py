import asyncio

from pyrogram.errors.exceptions.bad_request_400 import YouBlockedUser

from friday import friday, Message


@friday.on_cmd("quote", about={
    'header': "Quote a message",
    'usage': "{tr}quote [text or reply to msg]"})
async def quotecmd(message: Message):
    """quotecmd"""
    asyncio.get_event_loop().create_task(message.delete())
    args = message.input_str
    replied = message.reply_to_message
    async with friday.conversation('QuotLyBot') as conv:
        try:
            if replied:
                await conv.forward_message(replied)
            else:
                if not args:
                    await message.err('input not found!')
                    return
                await conv.send_message(args)
        except YouBlockedUser:
            await message.edit('first **unblock** @QuotLyBot')
            return
        quote = await conv.get_response(mark_read=True)
        await friday.forward_messages(chat_id=message.chat.id,
                                      from_chat_id=conv.chat_id,
                                      message_ids=quote.message_id,
                                      as_copy=True)
