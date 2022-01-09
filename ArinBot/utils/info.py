import discord
from discord.ext import commands
from config import Config

def get_roles_mention(member: discord.Member) -> str:
    """Returns a string with mentions to all the roles the user has"""
    if not len(member.roles) > 1:
        return None

    roles_mention: str = ""
    for role in member.roles[::-1]:
        if role.name != "@everyone":
            roles_mention += f" {role.mention}"

    return roles_mention

def get_acknowledgements(member: discord.member, context: commands.Context) -> str:
    """Returns a string that specifies if the user is an owner/dev/server owner"""
    return_string: str = ""
    if member.id in Config.owners:
        return_string += "Bot Owner"
    elif member.id in Config.devs:
        return_string += "Bot Developer"
    elif member.id == context.bot.user.id:
        return_string += "Hey! it's me"

    if member.id == context.guild.owner_id:
        if len(return_string) > 0:
            return_string += ", Server Owner"
        else:
            return_string += "Server Owner"
    
    if len(return_string) > 0:
        return return_string
    else:
        return None
