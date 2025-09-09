import logging
import random
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

nest_asyncio.apply()

# Логирование (для отладки)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# База мемов
memes = [
    {"name": "Dancing Cat", "video": "https://example.com/cat.mp4", "points": 10},
    {"name": "Doge Wow", "video": "https://example.com/doge.mp4", "points": 15},
    {"name": "Epic Fail", "video": "https://example.com/fail.mp4", "points": 5},
]

# Очки пользователей {chat_id: {user_id: score}}
user_scores = {}

# Команда /meme
async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.first_name

    meme = random.choice(memes)

    if chat_id not in user_scores:
        user_scores[chat_id] = {}
    if user_id not in user_scores[chat_id]:
        user_scores[chat_id][user_id] = 0

    user_scores[chat_id][user_id] += meme["points"]

    caption = (
        f"🎉 Congratulations {username}!\n\n"
        f"You got the meme *{meme['name']}* 🎬\n"
        f"Earned: *{meme['points']}* points\n"
        f"Total score: *{user_scores[chat_id][user_id]}*"
    )

    await context.bot.send_video(
        chat_id=chat_id,
        video=meme["video"],
        caption=caption,
        parse_mode="Markdown"
    )

# Команда /null
async def null(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id in user_scores and user_id in user_scores[chat_id]:
        user_scores[chat_id][user_id] = 0
        await update.message.reply_text("Your score has been reset to 0.")
    else:
        await update.message.reply_text("You don’t have a score yet to reset.")

# Асинхронный main
async def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler("null", null))  # маленькими буквами привычнее

    await app.run_polling()

# Запуск
asyncio.run(main())
