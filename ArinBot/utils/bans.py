import discord
from discord.ext import commands

async def is_banned(context: commands.Context, member: discord.Member) -> bool:
    try:
        await context.guild.fetch_ban(member)
    except discord.NotFound:
        return False
    return True
