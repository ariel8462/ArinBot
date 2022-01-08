import discord
from discord.ext import commands
from config import Config
from utils.permissions import *

class Report(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    async def report(self, context: commands.Context, *, reason: str) -> None:
        """Reports a message of a user, works by reply"""
        if not context.message.reference:
            await context.reply(f"No message spcified:\n{Config.COMMAND_PREFIX}report (as a reply to a message) <reason>")
            return

        message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
        user: discord.User = message.author

        if not await check_privs(context, user.id):
            return
        
        embed = discord.Embed(title=":warning: Report Incoming", description=f"Server: **{context.guild.name}**\nReported Message: [message]({message.jump_url})\nReported User: **{user}**\nReason: **{reason}**\nMessage Content: **{message.content}**\nReporting User: **{context.author}**",
        color=discord.Colour.red())

        admin_roles = [role for role in context.guild.roles if role.permissions.administrator]

        for role in admin_roles:
            for member in role.members:
                if not member.bot:
                    await member.send(embed=embed)

        await context.send(f"Successfully reported the message of **{user}**")


def setup(client: commands.Bot):
    client.add_cog(Report(client))
