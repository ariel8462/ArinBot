import discord
from discord import member
from discord.ext import commands
from config import Config

def is_owner(context: commands.Context) -> bool:
    """Checks if the user is the owner"""
    return context.author.id in Config.owners

def is_sudo(context: commands.context) -> bool:
    """Checks if the user is a sudo (dev/owner)"""
    return context.author.id in Config.owners or context.author.id in Config.devs

def can_ban(context: commands.Context) -> bool:
    """Checks if the user has enough permissions to ban members"""
    member: discord.Member = context.author
    return member.guild_permissions.ban_members or is_sudo(context)

def can_kick(context: commands.Context) -> bool:
    """Checks if the user has enough permissions to kick members"""
    member: discord.Member = context.author
    return member.guild_permissions.kick_members or is_sudo(context)

async def check_privs(context: commands.Context, member_id: int) -> bool:
    """Check if the bot can act on this user"""

    member: discord.Member = await context.guild.fetch_member(member_id)

    try:
        if member_id is context.author.id:
            await context.reply(f"You can't {context.command.name} your self")
            return  False
        elif member_id == context.bot.user.id:
            await context.reply(f"Huh! you thought I would {context.command.name} my self")
            return False
        elif member_id in Config.owners:
            await context.reply(f"I can't {context.command.name} my owner")
            return False
        elif member_id in Config.devs:
            await context.reply(f"I can't {context.command.name} my devs")
            return False
        elif member.guild_permissions.administrator:
            await context.reply(f"The user is an administrator, I can't {context.command.name} them")
            return False
    except:
        pass
    
    return True
