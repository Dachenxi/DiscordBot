import logging
from modules import bot

logger = logging.getLogger(__name__)

def setup_event():
    @bot.event
    async def on_command_error(ctx, error):
        logger.info(f"Kesalahan pada perintah : {error}")
        
    @bot.event
    async def on_ready():
        logger.info(f"Berhasil masuk ke user {bot.user.name}")
        