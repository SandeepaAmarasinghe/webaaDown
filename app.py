import yt_dlp
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Your existing bot token and settings
token = '7964156018:AAE8c4sDoI5vBFQoRSzuIKAwySnULxNn-wY'  # Replace with your actual bot token
updater = Updater(token, use_context=True)

# Function to handle YouTube video download
def download_video(url):
    # yt-dlp options
    ydl_opts = {
        'format': 'mp4',  # or any format you prefer
        'outtmpl': '/tmp/%(title)s.%(ext)s',  # Output path for the video
        'cookies': 'cookies.txt',  # Path to your cookies.txt file
    }

    try:
        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Pass the video URL
    except Exception as e:
        print(f"Error downloading video: {str(e)}")

# Function to handle /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me a YouTube Shorts link, and I'll download it for you.")

# Function to handle received messages (e.g., YouTube URLs)
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text  # Get the text message (URL)
    
    # Check if the message is a YouTube Shorts URL
    if 'youtube.com/shorts/' in url:
        update.message.reply_text("Downloading video...")
        download_video(url)  # Call the download function
        update.message.reply_text("Download complete!")
    else:
        update.message.reply_text("Please send a valid YouTube Shorts link.")

# Add handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(None, handle_message))

# Start the bot
updater.start_polling()
updater.idle()
