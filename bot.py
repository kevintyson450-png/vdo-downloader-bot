import requests
from bs4 import BeautifulSoup
import telegram
import youtube_dl

# Your Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Initialize Telegram Bot
bot = telegram.Bot(token=BOT_TOKEN)

# Function to download video
def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False

# Telegram Bot Handler
def handle_message(update, context):
    message = update.message
    chat_id = message.chat_id
    url = message.text

    bot.send_message(chat_id=chat_id, text="Downloading video...")

    if download_video(url):
        bot.send_message(chat_id=chat_id, text="Video downloaded successfully!")
        # You can add code here to send the video file to the user
    else:
        bot.send_message(chat_id=chat_id, text="Failed to download video.")

# Set up handlers
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

# Start the bot
updater.start_polling()
updater.idle()
