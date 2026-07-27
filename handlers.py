from telegram import Update
from telegram.ext import ContextTypes

from texts import *

waiting_for_code = {}

main_menu = [
    ["📦 دریافت سفارش", "💎 خدمات و قیمت‌ها"],
    ["📖 راهنما", "💬 پشتیبانی"],
]


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id

    if text == "💬 پشتیبانی":
        await update.message.reply_text(SUPPORT)
        return

    if text == "💎 خدمات و قیمت‌ها":
        await update.message.reply_text(SERVICES)
        return

    if text == "📖 راهنما":
        await update.message.reply_text(HELP)
        return

    if text == "📦 دریافت سفارش":
        waiting_for_code[user_id] = True

        await update.message.reply_text(
            ENTER_CODE
        )
        return

    if waiting_for_code.get(user_id):

        code = text.upper()

        await update.message.reply_text(
            f"کد دریافت شد:\n\n{code}\n\n(مرحله بعد فایل ارسال خواهد شد)"
        )

        waiting_for_code.pop(user_id)

        return

    await update.message.reply_text(
        "🔔 ابتدا روی گزینه\n\n"
        "📦 دریافت سفارش\n\n"
        "بزنید."
    )
