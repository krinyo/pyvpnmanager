from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Запросить доступ", callback_data="request_access"),
            InlineKeyboardButton("Получить ключ", callback_data="get_key"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в очко! Используй кнопки ниже:",
        reply_markup=reply_markup
    )

def register_handler(app):
    app.add_handler(CommandHandler("start", start))