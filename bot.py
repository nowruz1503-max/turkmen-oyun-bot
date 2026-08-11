import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)

@app.route("/")
def home():
    return "Türkmen Oýun Merkezi boty işleýär!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Profilim", callback_data="profile")],
        [InlineKeyboardButton("💰 Balans", callback_data="balance")],
        [InlineKeyboardButton("🛒 Hyzmatlar", callback_data="services")],
        [InlineKeyboardButton("💳 Töleg", callback_data="payment")],
        [InlineKeyboardButton("📞 Kömek", callback_data="help")]
    ]

    await update.message.reply_text(
        "🎮 Türkmen Oýun Merkezine hoş geldiňiz!\n\n"
        "Aşakdaky menýudan saýlaň:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "profile": "👤 Profil bölümi taýýarlanýar.",
        "balance": "💰 Balans bölümi taýýarlanýar.",
        "services": "🛒 Hyzmatlar bölümi taýýarlanýar.",
        "payment": "💳 Töleg bölümi taýýarlanýar.",
        "help": "📞 Kömek üçin admin bilen habarlaşyň."
    }

    await query.edit_message_text(messages.get(query.data, "Saýlaw tapylmady."))

async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    await application.updater.idle()

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()

    import asyncio
    asyncio.run(main())
