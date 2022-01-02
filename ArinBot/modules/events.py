import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, DisabledCommand, MissingPermissions
from config import Config

class Events(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error: commands.errors) -> None:
        if isinstance(error, CommandNotFound):
            await context.reply("The command specified was not found.")
        elif isinstance(error, MissingPermissions):
            await context.reply("You don't have enough permissions for this command.")
        elif isinstance(error, DisabledCommand):
            pass
        else:
            await context.reply(error)
        return

    @commands.Cog.listener()
    async def on_command_completion(self, context: commands.Context) -> None:
        """On each command completion, prints details about the command author in order to help in cases of spam"""
        print(f"{context.author.name} ({context.author.id}) used {Config.COMMAND_PREFIX}{context.command}")


def setup(client: commands.Bot):
    client.add_cog(Events(client))
