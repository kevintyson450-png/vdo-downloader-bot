import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔞 1DM+ Sniffer Mode (Cookies Active)!\nLink bhejiye, main direct download link nikal dunga.")

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status = await update.message.reply_text("🔎 Cookies ke sath link extract ho raha hai...")

    # Check agar cookies file mojud hai
    cookie_path = 'cookies.txt'
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    # Agar cookies file hai toh use add karo
    if os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            direct_link = info.get('url', None)
            title = info.get('title', 'video')

        if direct_link:
            msg = f"✅ **Link Found!**\n\n**Video:** {title}\n\n**Direct Link:** `{direct_link}`\n\n☝️ Is lamba link ko copy karein aur **1DM+** mein paste karke download karein."
            await status.edit_text(msg, parse_mode='Markdown')
        else:
            await status.edit_text("❌ Direct link nahi mila. Shayad link galat hai ya cookies expired hain.")

    except Exception as e:
        await status.edit_text(f"❌ Error: Site ne block kiya hai. Error: {str(e)[:50]}...")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_link))
    app.run_polling()

if __name__ == '__main__':
    main()
            
