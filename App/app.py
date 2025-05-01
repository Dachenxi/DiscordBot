import os
import asyncio
from dotenv import load_dotenv
from modules import bot, setup_logging, setup_cogs
from time import sleep

logger = setup_logging()
load_dotenv("App/.env")
TOKEN = os.getenv("TOKEN")

async def run_bot():
    retries = 0
    max_retries = 5
    while retries < max_retries:
        try:
            logger.info("Meload cog commands")
            await setup_cogs()
            await asyncio.sleep(0.2)
            logger.info("Berhasil meload semua commands")
            await asyncio.sleep(0.2)

            if not TOKEN:
                logger.error("Token discord tidak ditemukan")
                return

            logger.info("Token ditemukan, memulai bot")
            await bot.start(token=TOKEN)

        except Exception as e:
            retries += 1
            logger.warning(f"[RETRY {retries}] Bot error: {e}")
            await asyncio.sleep(5)  # Tunggu 5 detik sebelum retry
        else:
            break  # Keluar dari loop jika tidak error
    else:
        logger.error("Bot gagal dijalankan setelah beberapa percobaan.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        logger.info("Memulai loop utama")
        sleep(0.2)
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        logger.warning("Bot diberhentikan oleh user")
    except asyncio.CancelledError:
        logger.warning("Asyncio task was cancelled.")
    except Exception as e:
        logger.exception(f"Unexpected error in main loop: {e}")
    finally:
        try:
            if not bot.is_closed():
                loop.run_until_complete(bot.close())
        except Exception as e:
            logger.warning(f"Error saat menutup bot: {e}")
        finally:
            logger.info("Closing event loop...")
            loop.close()
