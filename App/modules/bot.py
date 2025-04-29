import logging
import discord
import json
import asyncio
from discord.ext import commands
from discord import Message, Activity, ActivityType

logger = logging.getLogger(__name__)

with open("App/settings/bot.json", "r") as file:
    data = json.load(file)
    prefix = data["PREFIX"]

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
                except:
                    logger.info(f"Error ketika memprosses pesan. Pesan yang diterima {message.content}")


bot = Bot(command_prefix=prefix,
          self_bot=True,
          activity=Activity(type=ActivityType.playing,
                            application_id=874575612075999272,
                            name="MakeSelfBot",
                            state="Idle"
                            ),
          help_command=None,
          status=discord.Status.idle)