import discord
from discord.errors import Forbidden
from discord.ext import commands
from utils.permissions import *
from config import Config

# to do - tmute (Work in Progress)
class Mute(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, context: commands.Context, member: discord.Member = None, *, reason: str = "Reason not specified") -> None:
        if not member:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}mute <username/id>")
            return

        if not await check_privs(context, member.id):
            return

        muted_role: discord.role.Role = next((r for r in context.guild.roles if r.name == f"muted-{Config.BOT_NAME}"), None)

        if not muted_role:
            await context.reply(f"Are you sure you have added a 'mute-{Config.BOT_NAME}' role, {Config.COMMAND_PREFIX}addrolemute")
            return

        try:
            await member.add_roles(muted_role, reason=reason)
        except Forbidden:
            await context.reply("Not enough permissions to mute or the user is an admin")
            return
        await context.reply("Muted user!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, context: commands.Context, member: discord.Member = None, *, reason: str = "Reason not specified") -> None:
        if not member:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}unmute <username/id>")
            return

        if not await check_privs(context, member.id):
            return

        muted_role: discord.role.Role = next((r for r in context.guild.roles if r.name == f"muted-{Config.BOT_NAME}"), None)

        if not muted_role:
            await context.reply(f"Are you sure you have added a 'muted-{Config.BOT_NAME}' role, {Config.COMMAND_PREFIX}addrolemute")
            return

        if not muted_role in member.roles:
            await context.reply("The user is not even muted")
            return

        try:
            await member.remove_roles(muted_role, reason=reason)
        except Forbidden:
            await context.reply("Not enough permissions to mute or the user is an admin")
            return
        await context.reply("Unmuted user!")
        
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrolemute(self, context: commands.Context) -> None:
        guild: discord.Guild = context.guild
        muted_role: discord.role.Role = next((r for r in context.guild.roles if r.name == f"muted-{Config.BOT_NAME}"), None)

        if muted_role:
            await context.reply("The role already exists")
            return
        else:
            muted_role = await guild.create_role(name=f"muted-{Config.BOT_NAME}", permissions=discord.Permissions(2147746368))

        for channel in context.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

        await context.reply(f"Added role mute-{Config.BOT_NAME}")


def setup(client: commands.Bot):
    client.add_cog(Mute(client))
