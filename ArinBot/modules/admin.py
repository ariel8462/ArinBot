import discord
from discord.ext import commands
from config import Config
from utils.permissions import *
from utils.devs import *

#enable and disable do it across the whole bot, not only one server, fix later
class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.check(is_sudo)
    async def disable(self, context: commands.Context, command_name: str = None) -> None:
        """Disables the specified command, only avaiable to devs and owners"""
        if not command_name:
            await context.reply(f"Missing argument - {Config.COMMAND_PREFIX}disable <command name>")
            return
        
        command: commands.Command = self.client.get_command(command_name)

        if not command:
            await context.reply("No such command exists, check your spelling")
            return
        
        if not command.enabled:
            await context.reply("Command is already disabled")
            return

        command.enabled = not command.enabled
        await context.reply("Disabled command successfully")

    @commands.command()
    @commands.check(is_sudo)
    async def enable(self, context: commands.Context, command_name: str = None) -> None:
        """Enables the specified command, only avaiable to devs and owners"""
        if not command_name:
            await context.reply(f"Missing argument - {Config.COMMAND_PREFIX}enable <command name>")
            return
        
        command: commands.Command = self.client.get_command(command_name)

        if not command:
            await context.reply("No such command exists, check your spelling")
            return
        
        if command.enabled:
            await context.reply("Command is already enabled")
            return

        command.enabled = not command.enabled
        await context.reply("Enabled command successfully")

    @commands.command()
    @commands.check(is_sudo)
    async def load(self, context: commands.Context, extension: str) -> None:
        """Loads a module, only avaiable to devs and owners"""
        try:
            self.client.load_extension(f"modules.{extension}")
        except Exception as e:
            await context.reply(e)
            return
        await context.send(f"Loaded extension **{extension}.py**")

    @commands.command()
    @commands.check(is_sudo)
    async def unload(self, context: commands.Context, extension: str) -> None:
        """Unloads a module, only avaiable to devs and owners"""
        try:
            self.client.unload_extension(f"modules.{extension}")
        except Exception as e:
            await context.send(e)
            return
        await context.send(f"Unloaded extension **{extension}.py**")

    @commands.command()
    @commands.check(is_owner)
    async def change_username(self, context: commands.Context, *, username: str) -> None:
        """Changes the username of the bot, only available to the owner"""
        try:
            await self.client.user.edit(username=username)
            await context.send(f"Changed username to **{username}**")
        except Exception as e:
            await context.send(e)

    @commands.command(aliases=["dm"])
    @commands.check(is_owner)
    async def pm(self, context: commands.Context, member: discord.Member, *, message: str) -> None:
        """Sends a private message to the specified user, only available to the owner"""
        try:
            await member.send(message)
            await context.send(f"Successfully sent a private message to **{member.name}**")
        except:
            await context.send("Failed, maybe he blocked pm's from unknown people")

    @commands.command()
    @commands.check(is_owner)
    async def leave(self, context: commands.Context):
        """Forces the bot to leave the current server"""
        try:
            await context.guild.leave()
        except Exception as e:
            await context.send(e)

    @commands.command()
    @commands.check(is_owner)
    async def promote_dev(self, context: commands.Context, member: discord.Member = None) -> None:
        """Makes the specified user a dev"""
        if context.message.reference is not None:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author

        if not member:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}promote_dev <username/id>\n{Config.COMMAND_PREFIX}promote_dev as a reply")
            return

        if member.id in Config.devs:
            await context.reply(f"The user is already a dev")
            return
        elif member.id in Config.owners:
            await context.reply(f"The user is the bot owner")
            return

        add_dev(member.id)
        await context.reply(f"Promoted **{member.name}** to dev")

    @commands.command()
    @commands.check(is_owner)
    async def demote_dev(self, context: commands.Context, member: discord.Member = None) -> None:
        """Demotes the specified user from being a dev"""
        if context.message.reference is not None:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author

        if not member:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}demote_dev <username/id>\n{Config.COMMAND_PREFIX}demote_dev as a reply")
            return

        if member.id not in Config.devs:
            await context.reply(f"The user is already not a dev")
            return

        remove_dev(member.id)
        await context.reply(f"Demoted **{member.name}** from dev")

    @commands.command()
    @commands.check(is_sudo)
    async def group_count(self, context: commands.Context) -> None:
        """Sends the count of groups the bot is in"""
        await context.send(f"I am in **{len(self.client.guilds)}** groups")


def setup(client: commands.Bot):
    client.add_cog(Admin(client))
