import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, DisabledCommand, MissingPermissions

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


def setup(client: commands.Bot):
    client.add_cog(Events(client))
