
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackContext, filters, CallbackQueryHandler
)
import random
import datetime

# === CONFIGURATION ===
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MAX_GPT_REQUESTS = 10
MAX_IMAGE_REQUESTS = 5

# === DATABASE SIMPLIFIÉE ===
users_data = {}

# === RAPPELS ISLAMIQUES ===
rappels = [
    "🕌 « Ne désespère pas de la miséricorde d’Allah » — Coran 39:53",
    "📿 Le Prophète ﷺ a dit : « Celui qui croit en Allah et au Jour dernier, qu’il dise du bien ou qu’il se taise. »",
    "🤲 Dou'a : Ô Allah, accorde-moi la sagesse et la paix intérieure. Amine.",
    "🌙 « Allah est avec les patients » — Coran 2:153",
]

# === LOGGING ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# === COMMANDES ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    if uid not in users_data:
        users_data[uid] = {"gpt": 0, "image": 0}
    await update.message.reply_text("Salam alaykoum mon frère / ma sœur 🌙")
Je suis HikmaBot, ton assistant intelligent et musulman.
Envoie-moi une question ou utilise /help pour voir mes fonctions.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Commandes disponibles :
"
        "/gpt - Pose une question à l’IA (10/jour)
"
        "/image - Génère une image (5/jour)
"
        "/traduire - Traduction Fr ↔ Ar ↔ En
"
        "/rappel - Rappel islamique du jour"
    )

async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if users_data[uid]["gpt"] >= MAX_GPT_REQUESTS:
        await update.message.reply_text("⚠️ Tu as atteint la limite quotidienne de questions IA.
Abonne-toi pour illimité.")
        return
    users_data[uid]["gpt"] += 1
    await update.message.reply_text("🧠 (Simulation) Réponse de l'IA ici...")

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if users_data[uid]["image"] >= MAX_IMAGE_REQUESTS:
        await update.message.reply_text("⚠️ Limite d’images atteinte pour aujourd’hui.
Passe en premium pour plus.")
        return
    users_data[uid]["image"] += 1
    await update.message.reply_text("🎨 (Simulation) Image générée ici.")

async def rappel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = random.choice(rappels)
    await update.message.reply_text(message)

# === TÂCHE QUOTIDIENNE ===
async def send_daily_reminders(application):
    for uid in users_data:
        try:
            message = random.choice(rappels)
            await application.bot.send_message(chat_id=int(uid), text=f"📿 *Rappel du jour* :
{message}", parse_mode="Markdown")
        except:
            continue

# === MAIN ===
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("gpt", gpt_command))
    application.add_handler(CommandHandler("image", image_command))
    application.add_handler(CommandHandler("traduire", help_command))
    application.add_handler(CommandHandler("rappel", rappel_command))

    # Planifie les rappels chaque jour à 9h (UTC)
    job_queue = application.job_queue
    job_queue.run_daily(send_daily_reminders, time=datetime.time(hour=9, minute=0, tzinfo=datetime.timezone.utc))

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
