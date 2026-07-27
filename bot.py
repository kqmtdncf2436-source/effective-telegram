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

from handlers import (
    button_handler,
    add_file,
    handle_forward,
    list_files,
    delete_file,
    stats,
    broadcast,
    edit_file,
    search_file,
)

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


app = Application.builder().token(BOT_TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start,
    )
)

app.add_handler(
    CommandHandler(
        "add",
        add_file,
    )
)

app.add_handler(
    MessageHandler(
        filters.FORWARDED,
        handle_forward,
    )
)

app.add_handler(
    CommandHandler(
        "list",
        list_files,
    )
)


app.add_handler(
    CommandHandler(
        "delete",
        delete_file,
    )
)


app.add_handler(
    CommandHandler(
        "stats",
        stats,
    )
)

app.add_handler(
    CommandHandler(
        "broadcast",
        broadcast,
    )
)

app.add_handler(
    CommandHandler(
        "edit",
        edit_file,
    )
)

app.add_handler(
    CommandHandler(
        "search",
        search_file,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        button_handler,
    )
)

app.run_polling()
