import logging

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error(f"Ошибка: {context.error}")