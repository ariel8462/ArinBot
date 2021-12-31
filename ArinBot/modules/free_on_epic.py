import discord
from discord.ext import commands
import feedparser

# to do - make asynchronous
class FreeOnEpic(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(aliases=["free_epic"])
    async def FreeOnEpic(self, context: commands.Context) -> None:
        feed = feedparser.parse("https://www.indiegamebundles.com/category/free/rss")
        description = feed.entries[0].title
        link = feed.entries[0].link
        await context.send(f"{link} - {description}")
        #beautify later - to do

def setup(client: commands.Bot):
    client.add_cog(FreeOnEpic(client))
