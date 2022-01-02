import discord
from discord.errors import Forbidden
from discord.ext import commands
from config import Config
from utils.permissions import *

#enable and disable do it across the whole bot, not only one server, fix later
class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.check(is_sudo)
    async def disable(self, context: commands.Context, command_name: str = None) -> None:
        if command_name is None:
            await context.reply(f"Missing argument - {Config.COMMAND_PREFIX}disable <command name>")
            return
        
        command: commands.Command = self.client.get_command(command_name)

        if command is None:
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
        if command_name is None:
            await context.reply(f"Missing argument - {Config.COMMAND_PREFIX}enable <command name>")
            return
        
        command: commands.Command = self.client.get_command(command_name)

        if command is None:
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
        try:
            self.client.load_extension(f"modules.{extension}")
        except Exception as e:
            await context.reply(e)
            return
        await context.send(f"Loaded extension **{extension}.py**")

    @commands.command()
    @commands.check(is_sudo)
    async def unload(self, context: commands.Context, extension: str) -> None:
        try:
            self.client.unload_extension(f"modules.{extension}")
        except Exception as e:
            await context.send(e)
            return
        await context.send(f"Unloaded extension **{extension}.py**")

    @commands.command()
    @commands.check(is_owner)
    async def change_username(self, context: commands.Context, username: str) -> None:
        try:
            await self.client.user.edit(username=username)
            await context.send(f"Changed username to **{username}**")
        except Exception as e:
            await context.send(e)

def setup(client: commands.Bot):
    client.add_cog(Admin(client))
