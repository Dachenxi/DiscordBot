import os
import asyncio
from dotenv import load_dotenv
from modules import bot, setup_logging, setup_cogs
from time import sleep
# Setup logging before main operations

logger = setup_logging()
load_dotenv("App/.env")
TOKEN=os.getenv("TOKEN")

async def main():
    try:
        logger.info("Meload cog commands")
        await setup_cogs()
        await asyncio.sleep(0.2)
        logger.info("Berhasil meload semua commands")
        await asyncio.sleep(0.2)
        
        logger.info("Mengecek token discord")
        await asyncio.sleep(0.2)
        if not TOKEN:
            logger.error("Token discord tidak ditemukan")
            await asyncio.sleep(0.2)
            return
        
        logger.info("Token ditemukan, memulai bot")
        await asyncio.sleep(0.2)
        await bot.start(token=TOKEN)
    except Exception as e:
        logger.warning(f"Exception : {e}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        logger.info("Memulai loop utama")
        sleep(0.2)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.warning("Bot diberhentikan oleh user")
    except asyncio.CancelledError:
        logger.warning("Asyncio task was cancelled.")
    except Exception as e:
        logger.exception(f"Unexpected error in main loop: {e}")
    finally:
        if not bot.is_closed():
            loop.run_until_complete(bot.close())
        logger.info("Closing event loop...")
        loop.close()