import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from texts import *
from codes import (
    code_exists,
    user_used,
    mark_used,
    get_code,
)


waiting_for_code = {}


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


    await asyncio.sleep(1)


    await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=data["channel_id"],
        message_id=data["message_id"]
    )


    await progress.delete()


    mark_used(
        code,
        update.effective_user.id
    )



async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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


        waiting_for_code.pop(user_id)


        await send_file(
            update,
            context,
            code
        )

        return



    await update.message.reply_text(
        UNKNOWN_MESSAGE
    )
