import discord
from discord.ext import commands
import feedparser

# to do - make asynchronous
class FreeGame(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(aliases=["free_game"])
    async def FreeGame(self, context: commands.Context) -> None:
        """Sends the most recent game that became free on epic/steam/uplay/etc"""
        feed = feedparser.parse("https://www.indiegamebundles.com/category/free/rss")
        description = feed.entries[0].title
        link = feed.entries[0].link
        await context.send(f"{link} - {description}")
        #beautify later - to do

def setup(client: commands.Bot):
    client.add_cog(FreeGame(client))
