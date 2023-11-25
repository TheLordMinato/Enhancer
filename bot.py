import asyncio
from pyrogram import Client, filters
from PIL import Image as Img, ImageEnhance as Enhnc
from io import BytesIO as Io

Bot = Client("your_bot_name", api_id=your_api_id, api_hash="your_api_hash", bot_token="your_bot_token")

@Bot.on_message(filters.private & filters.photo)
async def enhance_image(bot, msg):    
    if msg.photo:
        text = await msg.reply_text("Wait a Minute")
        photo = msg.photo[-1]
        file = await bot.get_file(photo.file_id)
        path = await file.download()
        img = Img.open(path)
        edit = await text.edit("Enhancing your image\n\nIt can take some time")
        emoji = await msg.reply("⚡️")
        enhncer = Enhnc.Contrast(img)
        rslt = enhncer.enhance(1.5)
        enhnced = IO()
        rslt.save(enhanced_image_io, format="JPEG")
        enhnced.seek(0)
        await msg.reply_photo(photo=enhnced)
        await edit.delete()
        await emoji.delete()


async def run_bot():
    await Bot.start()
    print("Bot has started.")
    await Bot.idle()


if __name__ == "__main__":
    asyncio.run(run_bot())
