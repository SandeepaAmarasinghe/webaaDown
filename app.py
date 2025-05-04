import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
import yt_dlp
import os
import asyncio

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
API_TOKEN = '7964156018:AAE8c4sDoI5vBFQoRSzuIKAwySnULxNn-wY'  # Make sure to keep this secure

# /start command handler
async def start(update: Update, context):
    await update.message.reply_text("Hi! Send me a YouTube link and I'll download the video for you (max 50MB).")

# Function to download and send the video
async def download(update: Update, context):
    url = update.message.text
    await update.message.reply_text(f"Processing video from {url}...")

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4][filesize<50M]+bestaudio[ext=m4a]/best[filesize<50M]',
            'outtmpl': '/tmp/%(title).40s.%(ext)s',  # Trimmed title for filename
            'merge_output_format': 'mp4',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        file_size = os.path.getsize(filename)
        if file_size >= 50 * 1024 * 1024:
            await update.message.reply_text("❌ Sorry, the downloaded video is still too large to send on Telegram.")
            os.remove(filename)
            return

        await update.message.reply_text("✅ Download complete! Uploading the video...")

        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f, timeout=120)

        os.remove(filename)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Error downloading or sending the video. Make sure the link is valid and try again.")

# Start the bot
def main():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    application.run_polling()

if __name__ == '__main__':
    main()
