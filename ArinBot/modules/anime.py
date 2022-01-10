import discord
from discord.ext import commands
import aiohttp
from utils.anime import *

#add manga function, and maybe character one as well - to do
class Anime(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def anime(self, context: commands.Context, *, anime: str) -> None:
        """Shows details about the specified anime"""
        variables = {'search': anime}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'query': anime_query, 'variables': variables}) as resp:
                json = await resp.json()
                json = json["data"]["Media"]

        if not json:
            await context.reply("No such anime or the site is down")
            return

        try:
            json['description'] = json["description"].replace(
                '<br>', '', 
            ).replace(
                '</br>', '',
            ).replace(
                '<i>', '', 
            ).replace(
                '<i/>', '', 
            ).replace(
                '</i>', '', 
                )
        except:
            pass
        
        studios_string= ""

        for studio in json['studios']['nodes']:
            studios_string += f"{studio['name']}, "
        studios_string = studios_string [:-2]

        embed: discord.Embed = discord.Embed(title=f"{json['title']['romaji']}",
        description=f"Type: {json['format']}\nStatus: {json['status']}\nEpisodes: {json['episodes']}\nDuration: \
        {json['duration']}\nScore: {json['averageScore']}\nGenres: {', '.join(json['genres'])}\nStudios: {studios_string}\n\n{json['description']}",
        color=0x3577ff)

        if json['bannerImage']:
            embed.set_image(url=json['bannerImage'])
        
        await context.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(Anime(client))
