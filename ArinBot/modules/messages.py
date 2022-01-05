import discord
from discord.ext import commands
from config import Config
from discord.errors import Forbidden, NotFound, HTTPException

class Messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def pin(self, context: commands.Context, *, message_id: int = None) -> None:
        """Pins a message"""
        if context.message.reference is not None:
            message_id = context.message.reference.message_id
        
        if not message_id:
            await context.reply(f"No message id spcified:\n{Config.COMMAND_PREFIX}pin <message id>\n{Config.COMMAND_PREFIX}pin as a reply to a message")
            return
        
        try:
            message: discord.Message = await context.channel.fetch_message(message_id)
        except NotFound:
            await context.reply("No such message found, are you sure the id is correct?")
        
        if message.pinned:
            await context.reply("The message is already pinned")
            return

        try:
            await message.pin()
        except NotFound:
            await context.reply("Message was not found")
        except Forbidden:
            await context.reply("I don't have enough permissions to pin messages :(")
        except HTTPException:
            await context.reply("Failed, check if there are over 50 pinned messages")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unpin(self, context: commands.Context, *, message_id: int = None) -> None:
        """Unpins a message"""
        if context.message.reference is not None:
            message_id = context.message.reference.message_id
        
        if not message_id:
            await context.reply(f"No message id spcified:\n{Config.COMMAND_PREFIX}unpin <message id>\n{Config.COMMAND_PREFIX}unpin as a reply to a message")
            return
        
        try:
            message: discord.Message = await context.channel.fetch_message(message_id)
        except NotFound:
            await context.reply("No such message found, are you sure the id is correct?")
        
        if not message.pinned:
            await context.reply("The message is not even pinned")
            return

        try:
            await message.unpin()
            await context.reply("Unpinned message successfully")
        except NotFound:
            await context.reply("Message was not found")
        except Forbidden:
            await context.reply("I don't have enough permissions to unpin messages :(")
        except Exception as e:
            await context.reply(e)
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unpin_all(self, context: commands.Context) -> None:
        """Unpins all messages in the current channel"""
        pinned_messages = await context.channel.pins()

        try:
            for message in pinned_messages:
                await message.unpin()
        except Forbidden:
            await context.reply("I don't have enough permissions to unpin messages :(")
            return
        except Exception as e:
            await context.reply(e)
            return
        
        await context.reply("Successfully unpinned all messages")

    @commands.command(aliases=["del"])
    @commands.has_permissions(manage_messages=True)
    async def delete(self, context: commands.Context, *, message_id: int = None) -> None:
        """Deletes the specified message"""
        if context.message.reference is not None:
            message_id = context.message.reference.message_id
        
        if not message_id:
            await context.reply(f"No message id spcified:\n{Config.COMMAND_PREFIX}delete <message id>\n{Config.COMMAND_PREFIX}delete as a reply to a message")
            return
        
        try:
            message: discord.Message = await context.channel.fetch_message(message_id)
        except NotFound:
            await context.reply("No such message found, are you sure the id is correct?")

        try:
            await message.delete()
        except Forbidden:
            await context.reply("I don't have enough permissions to delete messages :(")
        except Exception as e:
            await context.reply(e)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, context: commands.Context, count: int) -> None:
        try:
            await context.message.delete()
            await context.channel.purge(limit=count)
        except Exception as e:
            await context.reply(e)
            return
        
        await context.send(f"Successfully purged **{count}** messages")


def setup(client: commands.Bot):
    client.add_cog(Messages(client))
