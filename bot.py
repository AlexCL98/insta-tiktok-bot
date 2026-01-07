import os
import yt_dlp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

DOWNLOADS = "downloads"

def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    await update.message.reply_text(
        "🤖 Bot privado activo\n"
        "Envíame links de Instagram o TikTok\n"
        "✔ Lives terminados\n✔ Videos públicos"
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    url = update.message.text.strip()
    await update.message.reply_text("⏳ Descargando...")

    os.makedirs(DOWNLOADS, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{DOWNLOADS}/%(title)s.%(ext)s",
        "format": "mp4/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(
            video=open(filename, "rb"),
            caption="✅ Descarga lista"
        )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    print("Bot iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()
