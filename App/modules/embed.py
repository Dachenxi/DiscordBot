import json
import discord
import re
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timezone
from typing import List, Optional, Dict, Union
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("App/.env")
webhook_url = os.getenv("WEBHOOK_URL")

class EmbedManager:
    def __init__(self, bot: commands.Bot):
        """
        Initialize the EmbedManager with a Discord webhook URL and bot instance.
        
        Args:
            bot (commands.Bot): The Discord bot instance
            webhook_url (str): The Discord webhook URL
        """
        self.bot = bot
        self.webhook_url = webhook_url
        self.webhook = DiscordWebhook(url=webhook_url)
        self.stored_message_id = None
        
        # Extract channel ID from webhook URL
        webhook_pattern = r'https://discord\.com/api/webhooks/(\d+)/.*'
        match = re.match(webhook_pattern, webhook_url)
        if match:
            self.channel_id = int(match.group(1))
        else:
            raise ValueError("Invalid webhook URL format")
    
    async def create_embed(self, 
                         title: str,
                         description: str,
                         color: int = 0x00ff00,
                         fields: Optional[List[Dict[str, str]]] = None,
                         author: Optional[Dict[str, str]] = None,
                         footer: Optional[Dict[str, str]] = None,
                         thumbnail: Optional[str] = None,
                         image: Optional[str] = None) -> Optional[discord.Message]:
        """
        Create and send a new embed message.
        
        Args:
            title (str): Embed title
            description (str): Embed description
            color (int): Embed color in hex format
            fields (List[Dict]): List of fields, each containing name and value
            author (Dict): Author information with name and icon_url
            footer (Dict): Footer information with text and icon_url
            thumbnail (str): URL for thumbnail
            image (str): URL for main image
            
        Returns:
            discord.Message: The created message object, or None if failed
        """
        # Create new embed
        embed = DiscordEmbed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.now(timezone.utc)
        )
        
        # Add fields if provided
        if fields:
            for field in fields:
                embed.add_embed_field(
                    name=field['name'],
                    value=field['value'],
                    inline=field.get('inline', False)
                )
        
        # Add author if provided
        if author:
            embed.set_author(
                name=author.get('name', ''),
                icon_url=author.get('icon_url', '')
            )
        
        # Add footer if provided
        if footer:
            embed.set_footer(
                text=footer.get('text', ''),
                icon_url=footer.get('icon_url', '')
            )
        
        # Add thumbnail and image if provided
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if image:
            embed.set_image(url=image)
        
        # Add embed to webhook and send
        self.webhook.remove_embeds()
        self.webhook.add_embed(embed)
        response = self.webhook.execute()
        
        # Extract message ID from response and get Message object
        if response.status_code == 200:
            try:
                message_data = json.loads(response.text)
                self.stored_message_id = message_data['id']
                
                # Get the webhook channel
                webhook = await self.bot.fetch_webhook(self.channel_id)
                channel = webhook.channel
                
                # Fetch the message object
                if channel:
                    try:
                        return await channel.fetch_message(int(self.stored_message_id))
                    except (discord.NotFound, discord.HTTPException) as e:
                        print(f"Error fetching message: {e}")
                        return None
                
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error processing webhook response: {e}")
                return None
        return None
    
    async def edit_embed(self,
                        message: Union[discord.Message, str],
                        **kwargs) -> Optional[discord.Message]:
        """
        Edit an existing embed message.
        
        Args:
            message (Union[discord.Message, str]): Message object or ID to edit
            **kwargs: Same parameters as create_embed
            
        Returns:
            discord.Message: The edited message object, or None if failed
        """
        # Get message ID from input
        if isinstance(message, discord.Message):
            msg_id = str(message.id)
        else:
            msg_id = message or self.stored_message_id
            
        if not msg_id:
            raise ValueError("No message ID provided or stored")
            
        # Create webhook with message ID
        self.webhook = DiscordWebhook(url=self.webhook_url, id=msg_id)
        
        # Create new embed with updated content
        embed = DiscordEmbed(
            title=kwargs.get('title', ''),
            description=kwargs.get('description', ''),
            color=kwargs.get('color', 0x00ff00),
            timestamp=datetime.now(timezone.utc)
        )
        
        # Update fields if provided
        if 'fields' in kwargs:
            for field in kwargs['fields']:
                embed.add_embed_field(
                    name=field['name'],
                    value=field['value'],
                    inline=field.get('inline', False)
                )
        
        # Update other properties if provided
        if 'author' in kwargs:
            embed.set_author(
                name=kwargs['author'].get('name', ''),
                icon_url=kwargs['author'].get('icon_url', '')
            )
            
        if 'footer' in kwargs:
            embed.set_footer(
                text=kwargs['footer'].get('text', ''),
                icon_url=kwargs['footer'].get('icon_url', '')
            )
            
        if 'thumbnail' in kwargs:
            embed.set_thumbnail(url=kwargs['thumbnail'])
            
        if 'image' in kwargs:
            embed.set_image(url=kwargs['image'])
        
        # Update webhook with new embed
        self.webhook.remove_embeds()
        self.webhook.add_embed(embed)
        response = self.webhook.edit()
        
        if response.status_code == 200:
            # Get the webhook channel
            webhook = await self.bot.fetch_webhook(self.channel_id)
            channel = webhook.channel
            
            # Fetch the updated message object
            if channel:
                try:
                    return await channel.fetch_message(int(msg_id))
                except (discord.NotFound, discord.HTTPException) as e:
                    print(f"Error fetching edited message: {e}")
                    return None
        return None
    
    async def delete_embed(self, message: Union[discord.Message, str]) -> bool:
        """
        Delete an embed message.
        
        Args:
            message (Union[discord.Message, str]): Message object or ID to delete
            
        Returns:
            bool: Success status of the deletion
        """
        # Get message ID from input
        if isinstance(message, discord.Message):
            msg_id = str(message.id)
        else:
            msg_id = message or self.stored_message_id
            
        if not msg_id:
            raise ValueError("No message ID provided or stored")
            
        self.webhook = DiscordWebhook(url=self.webhook_url, id=msg_id)
        response = self.webhook.delete()
        
        if response.status_code == 204:  # Discord returns 204 for successful deletion
            self.stored_message_id = None
            return True
        return False