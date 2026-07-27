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


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text
    user_id = update.effective_user.id


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



        mark_used(
            code,
            user_id
        )


        await update.message.reply_text(
            PREPARING
        )


        await asyncio.sleep(2)


        await update.message.reply_text(
            SENDING
        )


        return



    await update.message.reply_text(
        UNKNOWN_MESSAGE
    )
