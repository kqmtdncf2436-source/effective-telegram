import json
import os

from state import waiting_for_code
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN
from texts import *


def load_codes():
    if os.path.exists("codes.json"):
        with open("codes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


main_menu = [
    ["📦 دریافت سفارش", "💎 خدمات و قیمت‌ها"],
    ["📖 راهنما", "💬 پشتیبانی"],
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        main_menu,
        resize_keyboard=True,
    )

    await update.message.reply_text(
        WELCOME,
        reply_markup=keyboard,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "💬 پشتیبانی":
        await update.message.reply_text(SUPPORT)

    elif text == "💎 خدمات و قیمت‌ها":
        await update.message.reply_text(SERVICES)

    elif text == "📖 راهنما":
        await update.message.reply_text(HELP)

    elif text == "📦 دریافت سفارش":
        waiting_for_code[user_id] = True

        await update.message.reply_text(
            ENTER_CODE
        )

    else:

        if waiting_for_code.get(user_id):

            code = text.upper()

            codes = load_codes()

            if code in codes:

                waiting_for_code.pop(user_id)

                await update.message.reply_text(
                    PREPARING
                )

            else:

                await update.message.reply_text(
                    "❌ کد وارد شده معتبر نیست.\n\n"
                    "🔑 لطفاً دوباره کد سفارش خود را وارد کنید."
                )

        else:

            await update.message.reply_text(
                "🔔 برای استفاده از کد سفارش، ابتدا روی گزینه:\n\n"
                "📦 دریافت سفارش\n\n"
                "بزنید و سپس کد را وارد کنید."
            )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        button_handler,
    )
)

app.run_polling()
