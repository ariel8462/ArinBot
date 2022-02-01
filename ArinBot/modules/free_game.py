import discord
from discord.ext import commands
import feedparser
import aiohttp

FREE_GAME_SITE_RSS = "https://www.indiegamebundles.com/category/free/rss"

class FreeGame(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(aliases=["free_game"])
    async def FreeGame(self, context: commands.Context) -> None:
        """Sends the most recent game that became free on epic/steam/uplay/etc"""
        async with aiohttp.ClientSession() as session:
            async with session.get(FREE_GAME_SITE_RSS) as response:
                html = await response.text()

        feed = feedparser.parse(html)
        description = feed.entries[0].title
        link = feed.entries[0].link

        #make it look better - to do
        await context.send(f"{link}\n{description}")


def setup(client: commands.Bot):
    client.add_cog(FreeGame(client))
