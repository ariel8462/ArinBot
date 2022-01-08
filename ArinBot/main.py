import discord
from discord.ext import commands
import os
from utils.default import *

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
    start_bot(Bot)
