import discord
from discord.errors import Forbidden
from discord.ext import commands
from utils.permissions import *
from config import Config

class Mute(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, context: commands.Context, member: discord.Member = None, *, reason: str = "Reason not specified") -> None:
        """Mutes the specified user"""
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
            await context.reply("I don't have enough permissions to mute :(, move my role higher")
            return
        await context.reply(f"Successfully muted **{member.name}**")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, context: commands.Context, member: discord.Member = None, *, reason: str = "Reason not specified") -> None:
        """Unmutes the specified user"""
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
            await context.reply("I don't have enough permissions to unmute :(")
            return
        await context.reply(f"Successfully unmuted **{member.name}**")
 
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrolemute(self, context: commands.Context) -> None:
        """Adds the role 'muted-<BOT_NAME>' for future mutes"""
        guild: discord.Guild = context.guild
        muted_role: discord.role.Role = next((r for r in context.guild.roles if r.name == f"muted-{Config.BOT_NAME}"), None)

        if muted_role:
            await context.reply("The role already exists")
            return
        else:
            muted_role = await guild.create_role(name=f"muted-{Config.BOT_NAME}", permissions=discord.Permissions(2147746368))

        for channel in context.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

        await context.reply(f"Added the role **mute-{Config.BOT_NAME}**")


def setup(client: commands.Bot):
    client.add_cog(Mute(client))
