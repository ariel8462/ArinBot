import discord
from discord.ext import commands
import os
from config import Config
from utils.default import *

#Change name later - from ArinBot to something normal lol
class Bot(commands.Cog):
    def __init__(self, client: commands.Bot, *args, **kwargs):
        self.client = client
        
        super().__init__(*args, **kwargs)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("--- The bot is up ---")
        for file in os.listdir("modules/"):
            if file.endswith(".py"):
                self.client.load_extension(f"modules.{file[:-3]}")


if __name__ == "__main__":
    token = set_config()
    intents = discord.Intents.default()
    intents.members = True
    client = commands.Bot(command_prefix=Config.COMMAND_PREFIX, intents=intents, case_insensitive=True)
    client.add_cog(Bot(client))
    client.run(token)
