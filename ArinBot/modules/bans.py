import discord
from discord.errors import Forbidden
from discord.ext import commands
from config import Config
from utils.permissions import *
from utils.bans import *

#add temp ban
class Bans(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.check(can_ban)
    async def ban(self, context: commands.Context, member: discord.Member = None, *, reason: str = "Reason not specified") -> None:
        if context.message.reference is not None:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author

        if member is None:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}ban <username/id>\n{Config.COMMAND_PREFIX}ban as a reply")
            return

        if not await check_privs(context, member.id):
            return

        try:
            if await is_banned(context, member):
                await context.reply("User is already banned!")
                return
        except TypeError:
            pass

        try:
            if type(member) is discord.user.User:
                await context.guild.ban(member)
            else:
                await member.ban(reason=reason)
        except Forbidden:
            await context.reply("Not enough permissions to ban | or the user is an admin")
            return
        await context.reply("Banned user!")

    @commands.command()
    @commands.check(can_kick)
    async def kick(self, context: commands.Context, member: discord.Member = None, *, reason: str = "Reason not specified") -> None:
        if context.message.reference is not None:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author

        if member is None:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}kick <username/id>\n{Config.COMMAND_PREFIX}kick as a reply")
            return

        if not await check_privs(context, member.id):
            return

        try:
            if type(member) is discord.user.User:
                if context.guild.get_member(member.id) is None:
                    await context.reply("The user is not even in the server")
                    return
                else:
                    await context.guild.kick(member)
            else:
                await member.kick(reason=reason)
        except Forbidden:
            await context.reply("Not enough permissions to kick | or the user is an admin")
            return
        await context.reply("Kicked user!")

    @commands.command()
    @commands.check(can_ban)
    async def unban(self,  context: commands.Context, member: discord.Member = None, *, reason=None) -> None:
        if context.message.reference is not None:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author
            
        if member is None:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}unban <username/id>\n{Config.COMMAND_PREFIX}unban as a reply")
            return

        try:
            if not await is_banned(context, member):
                await context.reply("The user is not even banned!")
                return
        except TypeError:
            pass

        try:
            if type(member) is discord.user.User:
                await context.guild.unban(member)
            else:
                await member.unban(reason=reason)
        except Forbidden:
            await context.reply("Not enough permissions to unban! assign me a better role")
            return
        await context.reply("Unbanned user!")


    @commands.command()
    @commands.check(is_sudo)
    async def gban(self, context: commands.Context, member: discord.Member = None, *, reason: str = None) -> None:
        if member is None:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}gban <username/id>\n")
            return

        if not await check_privs(context, member.id):
            return

        if member.id in Config.globally_banned:
            await context.reply("The user is already globally banned")
            return
        
        for guild in self.client.guilds:
            try:
                await guild.ban(member)
            except Forbidden:
                continue
            except Exception as e:
                await context.reply(e)
        
        Config.globally_banned.append(member.id)
        await context.reply(f"Banned {member.name} globally")

def setup(client: commands.Bot):
    client.add_cog(Bans(client))
