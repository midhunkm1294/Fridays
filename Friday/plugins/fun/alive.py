from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

from friday import friday, Message, Config, versions

LOGO_STICKER_ID, LOGO_STICKER_REF = None, None


@friday.on_cmd("alive", about={'header': "This command is just for fun"})
async def alive(message: Message):
    await message.delete()
    try:
        if LOGO_STICKER_ID:
            await sendit(LOGO_STICKER_ID, message)
        else:
            await refresh_id()
            await sendit(LOGO_STICKER_ID, message)
    except (FileIdInvalid, FileReferenceEmpty, BadRequest):
        await refresh_id()
        await sendit(LOGO_STICKER_ID, message)
    output = f"""
**friday is Up and Running**

       __Durable as a Serge__

• **python version** : `{versions.__python_version__}`
• **pyrogram version** : `{versions.__pyro_version__}`
• **friday version** : `{versions.__version__}`
• **license** : {versions.__license__}
• **copyright** : {versions.__copyright__}
• **repo** : [friday]({Config.UPSTREAM_REPO})
"""
    await friday.send_message(message.chat.id, output, disable_web_page_preview=True)


async def refresh_id():
    global LOGO_STICKER_ID, LOGO_STICKER_REF
    sticker = (await friday.get_messages('thefriday', 8)).sticker
    LOGO_STICKER_ID = sticker.file_id
    LOGO_STICKER_REF = sticker.file_ref


async def sendit(fileid, message):
    await friday.send_sticker(message.chat.id, fileid, file_ref=LOGO_STICKER_REF)
