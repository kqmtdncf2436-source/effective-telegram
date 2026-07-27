import asyncio

from config import ADMIN_ID
from telegram import Update
from telegram.ext import ContextTypes

from texts import *




from codes import (
    code_exists,
    user_used,
    mark_used,
    get_code,
    save_code,
    get_all_codes,
    delete_code,
    update_title,
    get_all_users,
)


waiting_for_code = {}

admin_state = {}

admin_temp = {}



async def send_file(update, context, code):

    data = get_code(code)

    if not data:
        return


    progress = await update.message.reply_text(
        PREPARING_20
    )

    await asyncio.sleep(2)

    await progress.edit_text(
        PREPARING_40
    )

    await asyncio.sleep(2)

    await progress.edit_text(
        PREPARING_60
    )

    await asyncio.sleep(2)

    await progress.edit_text(
        PREPARING_80
    )

    await asyncio.sleep(2)

    await progress.edit_text(
        SENDING
    )

    await asyncio.sleep(4)


    await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=data["channel_id"],
        message_id=data["message_id"]
    )


    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "✅ فایل تحویل شد\n\n"
            f"👤 کاربر:\n"
            f"{update.effective_user.first_name}\n\n"
            f"🆔 آیدی:\n"
            f"{update.effective_user.id}\n\n"
            f"🔑 کد:\n"
            f"{code}\n\n"
            f"📁 فایل:\n"
            f"{data.get('title','بدون نام')}"
        )
    )


    await progress.delete()


    mark_used(
        code,
        update.effective_user.id
    )



async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    admin_state[ADMIN_ID] = "waiting_forward"


    await update.message.reply_text(
        ADMIN_START
    )


async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    codes = get_all_codes()

    if not codes:

        await update.message.reply_text(
            "📭 هنوز هیچ فایلی ثبت نشده است."
        )

        return

    text = "📦 لیست فایل‌های ثبت شده\n\n"

    i = 1

    for code, data in codes.items():

        text += (
            f"{i}️⃣\n"
            f"🔑 کد: {code}\n"
            f"📁 عنوان: {data.get('title','بدون عنوان')}\n"
            f"👥 تعداد استفاده: {len(data.get('used', []))}\n\n"
        )

        i += 1
        
    await update.message.reply_text(text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    codes = get_all_codes()

    total_files = len(codes)

    users = set()
    downloads = 0

    for data in codes.values():

        downloads += len(data.get("used", []))

        for user in data.get("used", []):
            users.add(user)


    await update.message.reply_text(
        "📊 آمار ربات\n\n"
        f"📦 تعداد فایل‌ها: {total_files}\n\n"
        f"👥 کاربران یکتا: {len(users)}\n\n"
        f"📥 تعداد دانلودها: {downloads}"
    )

async def search_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    args = context.args

    if not args:
        await update.message.reply_text(
            "❌ مثال:\n/search ABC"
        )
        return

    keyword = " ".join(args).upper()

    codes = get_all_codes()

    result = ""

    i = 1

    for code, data in codes.items():

        title = data.get("title", "").upper()

        if keyword in code or keyword in title:

            result += (
                f"{i}️⃣\n"
                f"🔑 {code}\n"
                f"📁 {data.get('title','بدون عنوان')}\n\n"
            )

            i += 1


    if result == "":

        await update.message.reply_text(
            "❌ چیزی پیدا نشد."
        )

    else:

        await update.message.reply_text(
            result
        )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    args = context.args

    if not args:

        await update.message.reply_text(
            "❌ مثال:\n/broadcast سلام به همه"
        )

        return

    text = " ".join(args)

    users = get_all_users()

    sent = 0

    failed = 0

    for uid in users:

        try:

            await context.bot.send_message(
                chat_id=int(uid),
                text=text
            )

            sent += 1

        except:

            failed += 1


    await update.message.reply_text(
        f"✅ ارسال تمام شد\n\n"
        f"📨 موفق: {sent}\n"
        f"❌ ناموفق: {failed}"
    )

async def edit_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "⏳ این بخش را بعداً کامل می‌کنیم."
    )
    

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    args = context.args

    if not args:

        await update.message.reply_text(
            "❌ کد فایل را بعد از دستور وارد کن.\n\nمثال:\n/delete ABC123"
        )

        return


    code = args[0].upper()


    if delete_code(code):

        await update.message.reply_text(
            "🗑 فایل حذف شد.\n\n"
            f"🔑 کد:\n{code}"
        )

    else:

        await update.message.reply_text(
            "❌ این کد پیدا نشد."
        )



async def edit_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    args = context.args

    if len(args) < 2:

        await update.message.reply_text(
            "❌ مثال:\n/edit ABC123 عنوان جدید"
        )

        return

    code = args[0].upper()

    new_title = " ".join(args[1:])

    if update_title(code, new_title):

        await update.message.reply_text(
            "✅ عنوان فایل بروزرسانی شد."
        )

    else:

        await update.message.reply_text(
            "❌ کد پیدا نشد."
        )

async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    if admin_state.get(ADMIN_ID) != "waiting_forward":
        return


    message = update.message


    if message.forward_origin is None:

        await message.reply_text(
            "❌ لطفاً پست کانال را فوروارد کن."
        )

        return


    origin = message.forward_origin


    try:

        channel_id = origin.chat.id
        message_id = origin.message_id

    except:

        await message.reply_text(
            "❌ اطلاعات پست دریافت نشد."
        )

        return



    admin_temp[ADMIN_ID] = {

        "channel_id": channel_id,
        "message_id": message_id

    }


    admin_state[ADMIN_ID] = "waiting_code"


    await message.reply_text(
        "✅ فایل شناسایی شد.\n\n"
        "🔑 حالا کد فایل را وارد کن."
    )



async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text
    user_id = update.effective_user.id



    # ثبت کد توسط ادمین

    if (
        user_id == ADMIN_ID
        and admin_state.get(ADMIN_ID) == "waiting_code"
    ):

        code = text.upper()

        data = admin_temp.get(ADMIN_ID)


        if not data:

            await update.message.reply_text(
                "❌ اطلاعات فایل پیدا نشد."
            )

            return


        save_code(
            code,
            data["channel_id"],
            data["message_id"]
        )


        admin_state.pop(
            ADMIN_ID,
            None
        )


        admin_temp.pop(
            ADMIN_ID,
            None
        )


        await update.message.reply_text(
            "✅ فایل ثبت شد.\n\n"
            f"🔑 کد:\n{code}"
        )


        return



    if text == "💬 پشتیبانی":

        await update.message.reply_text(
            SUPPORT
        )

        return



    if text == "💎 خدمات و قیمت‌ها":

        await update.message.reply_text(
            SERVICES
        )

        return



    if text == "📖 راهنما":

        await update.message.reply_text(
            HELP
        )

        return



    if text == "📦 دریافت سفارش":

        waiting_for_code[user_id] = True


        await update.message.reply_text(
            ENTER_CODE
        )

        return



    if waiting_for_code.get(user_id):

        code = text.upper()


        if not code_exists(code):

            await update.message.reply_text(
                INVALID_CODE
            )

            return



        if user_used(code, user_id):

            await update.message.reply_text(
                USED_CODE
            )

            return



        waiting_for_code.pop(
            user_id
        )


        await send_file(
            update,
            context,
            code
        )

        return



    await update.message.reply_text(
        UNKNOWN_MESSAGE
    )
