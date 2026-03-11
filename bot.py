import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔞 Adult & Large Video Downloader Ready!\nLink bhejiye, main 1DM+ ke liye direct link nikal dunga.")

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status = await update.message.reply_text("🔎 Sniffing hidden video link...")

    # Adult sites bypass karne ke liye advanced settings
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'referer': url,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Sirf info extract karenge, download nahi (taaki 2GB+ support kare)
            info = ydl.extract_info(url, download=False)
            direct_link = info.get('url', None)
            title = info.get('title', 'video')

        if direct_link:
            msg = f"✅ **Link Found!**\n\n**Video:** {title}\n\n**Download Link:** `{direct_link}`\n\n☝️ Is lamba link ko copy karein aur **1DM+** mein paste karke 2GB ki file download karein."
            await status.edit_text(msg, parse_mode='Markdown')
        else:
            await status.edit_text("❌ Is site ka direct link nahi mil raha. Shayad cookies ki zaroorat hai.")

    except Exception as e:
        await status.edit_text(f"❌ Error: Site access denied. Kuch sites VPN ya Login maangti hain.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_link))
    app.run_polling()

if __name__ == '__main__':
    main()
            
