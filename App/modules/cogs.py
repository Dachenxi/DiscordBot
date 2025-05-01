from modules import bot

async def setup_cogs():
    await bot.load_extension("commands.utilities")
    await bot.load_extension("commands.virtual_farmer")