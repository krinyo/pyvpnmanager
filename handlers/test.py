from telegram.ext import CommandHandler

async def test(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    context.user_data["last_command"] = "test"
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Привет, {username}! Твой ID: {user_id}"
    )

def register_handler(app):
    app.add_handler(CommandHandler("test", test))