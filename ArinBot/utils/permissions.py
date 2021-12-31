import discord
from discord import member
from discord.ext import commands
from config import Config

def is_owner(member_id: int) -> bool:
    return member_id in Config.owners

def is_dev(member_id: int) -> bool:
    return member_id in Config.devs

async def check_privs(context: commands.Context, member_id: int) -> bool:
    #if user is unbannable/unkickable/whatever i.e. in list/db, return False - to add later (like disasters in saitama)
    try:
        if member_id is context.author.id:
            await context.reply(f"You can't {context.command.name} your self")
            return  False
        elif member_id == context.bot.user.id:
            await context.reply(f"Huh! you thought I would {context.command.name} my self")
            return False
        elif is_owner(member_id):
            await context.reply(f"I can't {context.command.name} my owner")
            return False
        elif is_dev(member_id):
            await context.reply(f"I can't {context.command.name} my devs")
            return False
    except:
        pass
    
    return True