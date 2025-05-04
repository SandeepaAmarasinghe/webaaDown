import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import yt_dlp as youtube_dl

# === Set up logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# === Your Bot Token ===
API_TOKEN = '7964156018:AAE8c4sDoI5vBFQoRSzuIKAwySnULxNn-wY'  # Replace with your actual bot token

# === /start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Send me a YouTube link, and I\'ll download the video for you.')

# === Download and Send YouTube Video ===
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    try:
        await update.message.reply_text(f"📥 Downloading video from:\n{url}")

        # yt-dlp options
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'cookies': 'cookies.txt'  # Use cookies.txt to access restricted videos
        }

        # Download video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Notify user
        await update.message.reply_text("✅ Download complete. Sending the file...")

        file_size = os.path.getsize(filename)
        with open(filename, 'rb') as video:
            if file_size > 49 * 1024 * 1024:
                # Send as document if > 50MB
                await update.message.reply_document(document=video, filename=os.path.basename(filename))
            else:
                # Send as regular video
                await update.message.reply_video(video=video, filename=os.path.basename(filename))

        os.remove(filename)

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        await update.message.reply_text("⚠️ Failed to download or send video. Make sure the link is correct and you are using a valid cookies.txt if needed.")

# === Main Bot Application ===
def main():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    application.run_polling()

if __name__ == '__main__':
    main()
