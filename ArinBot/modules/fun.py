import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    async def decide(self, context: commands.Context) -> None:
        await context.reply(random.choice(["yes", "no"]))

    @commands.command(aliases=["toss"])
    async def coin(self, context: commands.Context) -> None:
        await context.reply(random.choice(["head", "tails"]))


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
