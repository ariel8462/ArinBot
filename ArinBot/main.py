import discord
from discord.ext import commands
import os

from discord.ext.commands.errors import CommandNotFound, DisabledCommand, MemberNotFound, MissingPermissions
from config import Config

#Change name later - from ArinBot to something normal lol

class ArinBot(commands.Cog):
    def __init__(self, client: commands.Bot, *args, **kwargs):
        self.client = client
        
        super().__init__(*args, **kwargs)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("--- The bot is up ---")
        for file in os.listdir("modules/"):
            if file.endswith(".py"):
                client.load_extension(f"modules.{file[:-3]}")

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


def get_token() -> str:
    """Returns the bot token"""
    try:
        with open("token.config", 'r') as token_config:
            return token_config.readline()
    except FileNotFoundError:
        print("Enter your bot token at token.config")
        exit()

if __name__ == "__main__":
    token = get_token()
    intents = discord.Intents.default()
    intents.members = True
    client = commands.Bot(command_prefix=Config.COMMAND_PREFIX, intents=intents, case_insensitive=True)
    client.add_cog(ArinBot(client))
    client.run(token)
