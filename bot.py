""" A Pyrogram Bot to Enhance image and Quality 🤖
    made by me 🗿"""

import asyncio
from pyrogram import Client, filters, idle
from speedtest import Speedtest
from PIL import Image as Img, ImageEnhance as Enhnc
from io import BytesIO as Io
from config import API_ID, API_HASH, BOT_TOKEN

Bot = Client("Image Enhancer", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@Bot.on_message(filters.private & filters.command("start"))
async def start_command(_, msg):
    await msg.reply_text("hello i am image enhancer bot send any image")

@Bot.on_message(filters.private & filters.photo)
async def enhance_image(bot, msg):    
    if msg.photo:
        text = await msg.reply_text("Wait a minute")
        download_location = f"./DOWNLOADS/photos/{msg.from_user.id}.jpg"
        path = await bor.download_media(
                message=msg.photo, file_name=download_location
        )
        img = Img.open(path)
        edit = await text.edit("Enhancing your image\n\nIt can take some time")
        emoji = await msg.reply("⚡️")
        enhancer = Enhnc.Contrast(img)
        result = enhancer.enhance(1.5)
        enhncd = Io()
        result.save(enhncd, format="JPEG")
        enhncd.seek(0)
        await msg.reply_photo(photo=enhncd)
        await edit.delete()
        await emoji.delete()

@Bot.on_message(filters.command("testspeed"))
async def run_speedtest(client, message):
    reply_msg = await message.reply_text("Analyzing...", quote=True)
    speed_test = Speedtest()
    speed_test.get_best_server()
    await reply_msg.edit("Checking download speed")
    speed_test.download()
    await reply_msg.edit("Checking upload speed")
    speed_test.upload()
    speed_test.results.share()
    results = speed_test.results.dict()
    photo = results["share"]
    text = f"Speed Test Info\nName: {results['server']['name']}\nServer: {results['server']['country']}, {results['server']['cc']}\nLatency: {results['server']['latency']}\nUpload Speed: {human_readable(results['upload'] / 8)}/s\nDownload Speed: {human_readable(results['download'] / 8)}/s"
    await reply_msg.edit_text("Sending info")
    await message.reply_photo(photo=photo, caption=text)
    await reply_msg.delete()

#Get size in human-readable format.
def human_readable(size):
    x = 2 ** 10
    var = 0
    size = float(size)
    units = {0: ' ', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > x:
        size /= x
        var += 1
    return f"{round(size, 2)} {units[var]}"

Bot.run()
