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

        with open(
            "codes.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return {}


main_menu = [
    ["📦 دریافت سفارش", "💎 خدمات و قیمت‌ها"],
    ["📖 راهنما", "💬 پشتیبانی"],
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = ReplyKeyboardMarkup(
        main_menu,
        resize_keyboard=True
    )

    await update.message.reply_text(
        WELCOME,
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id


    # پشتیبانی
    if text == "💬 پشتیبانی":

        await update.message.reply_text(
            SUPPORT
        )


    # خدمات
    elif text == "💎 خدمات و قیمت‌ها":

        await update.message.reply_text(
            SERVICES
        )


    # راهنما
    elif text == "📖 راهنما":

        await update.message.reply_text(
            HELP
        )


    # دریافت سفارش
    elif text == "📦 دریافت سفارش":

        waiting_for_code[user_id] = True

        await update.message.reply_text(
            ENTER_CODE
        )


    # هر چیز دیگر
    else:


        # اگر کاربر منتظر کد است
        if waiting_for_code.get(user_id):

            code = text.upper()

            codes = load_codes()


            if code in codes:


                waiting_for_code.pop(
                    user_id,
                    None
                )


                await update.message.reply_text(
                    PREPARING
                )


            else:


                # اینجا پاک نمی‌کنیم
                # دوباره اجازه ورود کد می‌دهیم

                await update.message.reply_text(
                    "❌ کد وارد شده اشتباه یا منقضی است.\n\n"
                    "🔑 لطفاً دوباره کد سفارش خود را وارد کنید."
                )



        # اگر اصلاً داخل بخش دریافت نیست
        else:


            await update.message.reply_text(
                "🔔 این پیام قابل پردازش نیست.\n\n"
                "برای دریافت سفارش لطفاً ابتدا گزینه:\n\n"
                "📦 دریافت سفارش\n\n"
                "را انتخاب کنید."
            )



app = Application.builder().token(BOT_TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        button_handler
    )
)


app.run_polling()
