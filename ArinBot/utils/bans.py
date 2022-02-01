import discord
from discord.ext import commands

async def is_banned(context: commands.Context, member: discord.Member) -> bool:
    """Checks if the specified user is banned from the server"""
    try:
        await context.guild.fetch_ban(member)
    except discord.NotFound:
        return False
    return True
