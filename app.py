from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
import logging
import yt_dlp as youtube_dl
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
API_TOKEN = 'YOUR_BOT_TOKEN'

# Function to handle the start command
async def start(update: Update, context):
    await update.message.reply_text('Hi! Send me a YouTube link, and I\'ll download the video for you.')

# Function to download the video and send it back
async def download(update: Update, context):
    url = update.message.text
    try:
        await update.message.reply_text(f"Downloading video from {url}...")
        
        # Setup yt-dlp options
        ydl_opts = {
            'format': 'mp4',  # you can change to other formats if you prefer
            'outtmpl': '/tmp/%(title)s.%(ext)s',  # Output path for the video
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info_dict)  # Get the filename

        await update.message.reply_text(f"Download complete! Sending the video...")

        # Send the video to the Telegram chat
        with open(video_filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        # Optionally delete the video after sending
        os.remove(video_filename)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"Error downloading the video. Please try again later.")

# Error handler function
async def error(update: Update, context):
    logger.error(f"Update {update} caused error {context.error}")
    await update.message.reply_text(f"An error occurred: {context.error}")

# Main function to handle commands and run the bot
def main():
    # Set up the application
    application = Application.builder().token(API_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    # Add error handler
    application.add_error_handler(error)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
