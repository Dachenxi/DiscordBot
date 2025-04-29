import logging
import discord
import re
from typing import Optional
from discord.ext import commands
from modules import EmbedManager, bot

logger = logging.getLogger(__name__)

class Utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed = EmbedManager(self.bot)
        
    @commands.command(name="ping", aliases=["p"])
    async def ping(self, message: commands.Context):
        """
        Command simple untuk ping atau 
        test koneksi bot ke server discord
        """
        try:
            await message.channel.send("pong")
        except Exception as e:
            logger.warning(f"Kesalahan terjadi dengan error {e}")

    @commands.command(name="me")
    async def me(self, ctx: commands.Context, target: Optional[str] = None):
        """
        Get user info for self or specified user
        Usage: !me [user_id/mention]
        """
        try:
            # If no target, use author
            if not target:
                user: discord.Member = ctx.author
            else:
                # Check if target is a mention
                mention_match = re.match(r'<@!?(\d+)>', target)
                
                if mention_match:
                    # If mention, get ID from regex match
                    user_id = int(mention_match.group(1))
                    user = self.bot.get_user(user_id)
                elif target.isdigit():
                    # If number, convert directly to int
                    user_id = int(target)
                    user = self.bot.get_user(user_id)
                else:
                    await ctx.send("Invalid user format. Use ID or mention.", delete_after=5)
                    return

                if not user:
                    await ctx.send("User not found.", delete_after=5)
                    return

            # Get member object if in guild
            member = ctx.guild.get_member(user.id) if ctx.guild else None

            # Prepare fields for embed
            fields = [
                {"name": "Username", "value": user.name, "inline": True},
                {"name": "User ID", "value": str(user.id), "inline": True},
                {"name": "Bot ?", "value": "Yes" if user.bot else "No", "inline": True}
            ]

            if member:
                # Format roles
                roles = [role.name for role in member.roles[1:]]  # Skip @everyone
                roles_str = ", ".join(roles) if roles else "None"

                # Add member-specific fields
                fields.extend([
                    {"name": "Joined Server", 
                     "value": member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "N/A",
                     "inline": True},
                    {"name": "Nitro Status",
                     "value": "Active since " + member.premium_since.strftime("%Y-%m-%d") if member.premium_since else "No",
                     "inline": True},
                    {"name": "Roles", 
                     "value": roles_str[:1024],  # Discord limit
                     "inline": False},
                ])

            # Add account creation date
            fields.append({
                "name": "Account Created",
                "value": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "inline": False
            })

            # Prepare author and footer
            author = {
                "name": f"{user.name} | {user.nick} | {user.global_name}",
                "icon_url": user.avatar.url if user.avatar else user.default_avatar.url
            }

            footer = {
                "text": f"Diminta Oleh {ctx.author.name}",
                "icon_url": "https://cdn.discordapp.com/attachments/1205777996275912714/1366648003166736384/games.png?ex=6811b5a3&is=68106423&hm=f60651d1110b5bbbc2ba4d7f760b8414a87dae78548ace59524f146d3fbb570c&"
            }

            # Create the embed using EmbedManager
            embed = await self.embed.create_embed(
                title=f"User Information - {user.name}",
                description="",  # Empty description since we're using fields
                color=int(member.color.value) if member else 0x3498db,  # Use member color or default blue
                fields=fields,
                author=author,
                footer=footer,
                thumbnail=user.avatar.url if user.avatar else user.default_avatar.url
            )
            # Send the embed
            if embed is not None:
                await embed.forward(ctx.channel)
            else:
                await ctx.channel.send("Failed to create embed.", delete_after=5)
            
        except Exception as e:
            print(f"Error in me command: {e}")
            await ctx.send("An error occurred while fetching user info.", delete_after=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(Utilities(bot))
    logger.info("Utilies command berhasil di load")