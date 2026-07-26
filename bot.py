from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN


# منوی اصلی
main_menu = [
    ["📦 دریافت سفارش", "💎 خدمات و قیمت‌ها"],
    ["📖 راهنما", "💬 پشتیبانی"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        main_menu,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "سلام 🌸\n\n"
        "به پخش نهایی خوش آمدید.\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💬 پشتیبانی":
        await update.message.reply_text(
            "💬 برای ارتباط با پشتیبانی:\n\n"
            "@YOUR_USERNAME"
        )

    elif text == "💎 خدمات و قیمت‌ها":
        await update.message.reply_text(
            "💎 بخش خدمات و قیمت‌ها بزودی تکمیل می‌شود."
        )

    elif text == "📖 راهنما":
        await update.message.reply_text(
            "📖 بخش راهنما بزودی تکمیل می‌شود."
        )

    elif text == "📦 دریافت سفارش":
        await update.message.reply_text(
            "📦 لطفاً کد سفارش خود را وارد کنید."
        )


app = Application.builder().token(BOT_TOKEN).build()


app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler)
)


app.run_polling()
