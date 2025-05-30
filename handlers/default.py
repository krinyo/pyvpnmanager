from telegram.ext import MessageHandler, filters

async def default(update, context):
    await update.message.reply_text("Неизвестная команда или текст.")

def register_handler(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, default))
    app.add_handler(MessageHandler(filters.COMMAND, default))