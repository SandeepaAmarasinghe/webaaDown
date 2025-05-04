import logging
import os
import shutil
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
import yt_dlp as youtube_dl

# -------------------- CONFIG --------------------
API_TOKEN = '7964156018:AAE8c4sDoI5vBFQoRSzuIKAwySnULxNn-wY'  # Your bot token
COOKIES_FILE = 'cookies.txt'  # Optional for YouTube auth

# -------------------- LOGGER --------------------
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- CHECK FFMPEG --------------------
if not shutil.which("ffmpeg"):
    raise EnvironmentError("❌ FFmpeg is not installed. Please install it and add to PATH.")

# -------------------- HANDLERS --------------------
async def start(update: Update, context):
    await update.message.reply_text('👋 Hi! Send me a YouTube or Facebook video URL to download.')

async def download(update: Update, context):
    url = update.message.text.strip()
    try:
        await update.message.reply_text(f"📥 Downloading from:\n{url}")

        # yt-dlp options
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True,
            'cookies': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        await update.message.reply_text("✅ Download complete. Uploading...")

        file_size = os.path.getsize(video_path)
        max_telegram_size = 49 * 1024 * 1024  # 49 MB

        with open(video_path, 'rb') as f:
            if file_size > max_telegram_size:
                await update.message.reply_document(document=f)
            else:
                await update.message.reply_video(video=f)

        os.remove(video_path)

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        await update.message.reply_text(f"⚠️ Error: {e}")

# -------------------- MAIN --------------------
def main():
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()

if __name__ == '__main__':
    main()
