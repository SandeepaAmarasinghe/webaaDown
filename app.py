import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Your bot token
token = '7964156018:AAE8c4sDoI5vBFQoRSzuIKAwySnULxNn-wY'  # Your token here

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
async def start(update: Update, context):
    await update.message.reply_text("Hello! Send me a YouTube Shorts link, and I'll download it for you.")

# Function to handle received messages (e.g., YouTube URLs)
async def handle_message(update: Update, context):
    url = update.message.text  # Get the text message (URL)
    
    # Check if the message is a YouTube Shorts URL
    if 'youtube.com/shorts/' in url:
        await update.message.reply_text("Downloading video...")
        download_video(url)  # Call the download function
        await update.message.reply_text("Download complete!")
    else:
        await update.message.reply_text("Please send a valid YouTube Shorts link.")

# Initialize the application
application = Application.builder().token(token).build()

# Add handlers
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT, handle_message))

# Start the bot
application.run_polling()
