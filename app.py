import logging
import os
import moviepy.editor as mp
import yt_dlp as youtube_dl
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to compress video if it's too large
def compress_video(input_file, output_file):
    video = mp.VideoFileClip(input_file)
    video.write_videofile(output_file, bitrate="5000k")
    video.close()

# Command handler to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Send me a YouTube video URL and I will download it for you.')

# Function to download and send the video
async def download(update: Update, context: CallbackContext):
    url = update.message.text
    try:
        await update.message.reply_text(f"Downloading video from {url}...")

        # yt-dlp options with cookies for YouTube authentication
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': '/tmp/%(title)s.%(ext)s',  # Output path for the video
            'cookies': 'cookies.txt',  # Assuming cookies.txt is in the same directory as app.py
        }

        # Download the video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info_dict)

        # Check video size
        video_size = os.path.getsize(video_filename) / (1024 * 1024)  # in MB
        if video_size > 50:
            compressed_video_filename = f"/tmp/compressed_{os.path.basename(video_filename)}"
            compress_video(video_filename, compressed_video_filename)
            video_filename = compressed_video_filename

        await update.message.reply_text(f"Download complete! Sending the video...")

        # Send the video to Telegram chat
        with open(video_filename, 'rb') as video_file:
            await update.message.reply_document(document=video_file)

        # Optionally delete the video after sending
        os.remove(video_filename)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"Error downloading the video. Please try again later.")

def main():
    # Set up the bot with your token
    token = '7964156018:AAE8c4sDoI5vBFQoRSzuIKAwySnULxNn-wY'  # Your Telegram Bot API token
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handler for receiving URLs
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
