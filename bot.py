import os
import subprocess
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def mirror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    msg = await update.message.reply_text("🔎 Checking link...")

    filename = url.split("/")[-1]

    await msg.edit_text("📥 Downloading...")

    download = subprocess.Popen(
        ["aria2c","-x16","-s16","-o",filename,url]
    )

    download.wait()

    await msg.edit_text("☁ Uploading to Drive...")

    subprocess.run(["rclone","copy",filename,"drive:ROM"])

    await msg.edit_text("✅ Mirror selesai!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mirror))

app.run_polling()
