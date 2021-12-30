import discord
from discord.ext import commands
import time

class Ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    async def ping(self, context: commands.Context) -> None:
        start_time = time.time()
        message = await context.send("Pinging...")
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000, 3)
        await message.edit(content=str(ping_time) + " ms")


def setup(client: commands.Bot):
    client.add_cog(Ping(client))
