import discord
from discord.errors import Forbidden
from discord.ext import commands
from config import Config
from utils.permissions import *

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
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


def setup(client: commands.Bot):
    client.add_cog(Admin(client))
