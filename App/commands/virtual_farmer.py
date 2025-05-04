import logging
import discord
import asyncio
import random
from discord.ext import commands, tasks
from modules import EmbedManager

logger = logging.getLogger(__name__)

class VirtualFarmer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed = EmbedManager(self.bot)
        self._farm_current = 0
        self._farm_count = 0
    
    @tasks.loop(seconds=0)
    async def farm_loop(self, delay, farm_button: discord.Button, sell_button: discord.Button):
        try:
            if self._farm_current >= self._farm_count:
                self._farm_count = 0
                self.farm_loop.cancel()
                logger.warning("farm_loop sudah selesai")
                return
            
            elif self._farm_current % 20 == 0:
                logger.info(f"Farming {self._farm_current} dari {self._farm_count}")
            
            else:
                await farm_button.click()
                await asyncio.sleep(random.randint(1, 3))
                await sell_button.click()
                await asyncio.sleep(random.randint(1, 3))
                await asyncio.sleep(delay)
            
            self._farm_current += 1
        except Exception:
            logger.exception(f"Error pada farm_loop: ")
        
            
            
    
    @commands.command(name="farming")
    async def farming(self, message: discord.Message, count: int, delay: int, message_id: str):
        try:
            target_farm = await message.channel.fetch_message(int(message_id))
            if not target_farm:
                await message.channel.send("Tolong reply message embed dengan Farm dan Sell button", delete_after=2)
                return
            
            if self.farm_loop.is_running():
                await message.channel.send("farm_loop sudah berjalan", delete_after=2)
                return
            
            for component in target_farm.components:
                for row in component.children:
                    if row.label == "Farm":
                        farm_button = row
                    if row.label == "Sell":
                        sell_button = row
            
            if farm_button and sell_button:
                self._farm_count = int(count)
                self._farm_current = 0
                self.farm_loop.start(int(delay), farm_button, sell_button)
                await message.channel.send(f"farm_loop dimulai dengan total {count} kali", delete_after=2)
                logger.warning(f"farm_loop dimulai dengan total {count} kali dan delay {delay}")
            
            else:
                await message.channel.send("Terjadi kesalahan ketika ingin memulai darm loop", delete_after=2)
                logger.warning("Terjadi kesalahan ketika ingin memulai darm loop")
        
        except Exception as e:
            logger.error(f"Error pada command farm: {e}")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(VirtualFarmer(bot))
    logger.info("VirtualFarmer command berhasil di load")              