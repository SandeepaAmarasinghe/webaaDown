import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
import yt_dlp as youtube_dl
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
API_TOKEN = '7964156018:AAE8c4sDoI5vBFQoRSzuIKAwySnULxNn-wY'  # Replace this with your actual bot token

# Function to handle the start command
async def start(update: Update, context):
    await update.message.reply_text('Hi! Send me a YouTube link, and I\'ll download the video for you.')

# Function to download the video and send it back
async def download(update: Update, context):
    url = update.message.text
    try:
        await update.message.reply_text(f"Downloading video from {url}...")

        # Setup yt-dlp options with cookies support
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # This tells yt-dlp to use your cookies.txt
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info_dict)

        await update.message.reply_text("Download complete! Sending the video...")

        with open(video_filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        os.remove(video_filename)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Error downloading the video. Please try again later.")

# Main function to run the bot
def main():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    application.run_polling()

if __name__ == '__main__':
    main()
