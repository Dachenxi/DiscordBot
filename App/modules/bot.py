import logging
import discord
import asyncio
from discord.ext import commands
from discord import Message, Activity, ActivityType
from modules.json_helper import get_value_json

logger = logging.getLogger(__name__)
prefix = "!"

class Bot(commands.Bot):
    async def on_message(self, message: Message):
        if not message.guild:
            return
        
        if message.author.id == self.user.id:
            if message.content.startswith(prefix):
                try:
                    await message.delete()
                    await asyncio.sleep(0.5)
                    parts = message.content[1:].split()
                    command_name = parts[0]
                    logger.info(f"Menerima perintah !{command_name}")
                    
                    command = self.get_command(command_name)
                    if command:
                        try:
                            args = parts[1] if len(parts) > 1 else ''
                            if args:
                                await command(message, args)
                            else:
                                await command(message)
                        except Exception as e:
                            logger.info("Error ketika mencoba mengirim perintah")
                    else:
                        await message.reply("Tidak ada command dengan nama itu!")
                except Exception as e:
                    logger.info(f"Error ketika memprosses pesan. Pesan yang diterima {message.content} dengan error {e}")


bot = Bot(command_prefix=prefix,
          self_bot=True,
          activity=Activity(type=ActivityType.custom, name="!help"),
          help_command=None,
          status=discord.Status.idle)