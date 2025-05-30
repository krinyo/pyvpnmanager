from telegram.ext import CallbackQueryHandler, MessageHandler, filters
from database.db import Session
from database.models import User, Request
from config.settings import ADMIN_ID

async def request_access(update, context):
    query = update.callback_query
    user_id = update.effective_user.id
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user and user.is_active:
        await query.message.reply_text("Вы уже зарегистрированы в системе")
        return
    await query.answer()
    await query.message.reply_text("Оставьте комментарий к заявке:")
    context.user_data["awaiting_comment"] = True

async def handle_comment(update, context):
    if not context.user_data.get("awaiting_comment"):
        return
    
    user_id = update.effective_user.id
    username = update.effective_user.username or "No username"
    comment = update.message.text
    session = Session()
    
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if not user:
        user = User(telegram_id=user_id, username=username)
        session.add(user)
        session.commit()
    
    request = session.query(Request).filter_by(user_id=user.id, status="pending").first()
    if request:
        await update.message.reply_text("Ваш запрос уже в обработке.")
        session.close()
        context.user_data["awaiting_comment"] = False
        return
    
    request = Request(user_id=user.id, comment=comment)
    session.add(request)
    session.commit()
    
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New request from @{username}:\nComment: {comment}\nID: {user.id}"
    )
    await update.message.reply_text("Запрос отправлен на обработку администратором.")
    session.close()
    context.user_data["awaiting_comment"] = False

def register_handler(app):
    app.add_handler(CallbackQueryHandler(request_access, pattern="request_access"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comment))