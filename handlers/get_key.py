from telegram.ext import CallbackQueryHandler
from database.db import Session
from database.models import User
from utils.qr_code import generate_qr_code
from utils.vless import generate_vless_string

async def get_key(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user or not user.is_active or not user.vless_key:
        await query.message.reply_text("You don't have an active VLESS key.")
        session.close()
        return
    
    #vless_string = generate_vless_string(user.vless_key)
    #qr_code = generate_qr_code(vless_string, user.id)
    await query.message.reply_photo(
        photo=qr_code,
        caption=f"Your VLESS key:\n{vless_string}"
    )
    session.close()

def register_handler(app):
    app.add_handler(CallbackQueryHandler(get_key, pattern="get_key"))