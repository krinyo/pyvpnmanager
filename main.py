from telegram.ext import Application
from config.settings import BOT_TOKEN
from handlers.start import register_handler as start_handler
from handlers.request_access import register_handler as request_handler
from handlers.get_key import register_handler as key_handler
from handlers.default import register_handler as default_handler
from handlers.error import error_handler
import logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    start_handler(app)
    request_handler(app)
    key_handler(app)
    default_handler(app)
    app.add_error_handler(error_handler)
    
    app.run_polling()

if __name__ == "__main__":
    main()