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

        if not json:
            await context.reply("Anime not found")
            return
        else:
            json = json["data"]["Media"]

        try:
            json['description'] = clean_html(json['description'])
        except:
            pass
        
        anime_studios= ""

        for studio in json['studios']['nodes']:
            anime_studios += f"{studio['name']}, "
        studios_string = anime_studios[:-2]

        embed: discord.Embed = discord.Embed(title=f"{json['title']['romaji']}",
        description=f"Type: {json['format']}\nStatus: {json['status']}\nEpisodes: {json['episodes']}\nDuration: \
        {json['duration']}\nScore: {json['averageScore']}\nGenres: {', '.join(json['genres'])}\nStudios: \
        {studios_string}\n\n{json['description']}")
        
        try:
            embed.color=int(json['coverImage']['color'][1:], 16)
        except TypeError:
            embed.color=0x3577ff

        if json['bannerImage']:
            embed.set_image(url=json['bannerImage'])

        try:
            embed.set_thumbnail(url=json['coverImage']['extraLarge'])
        except:
            pass
        
        await context.send(embed=embed)

    @commands.command()
    async def manga(self, context: commands.Context, *, manga: str) -> None:
        """Shows details about the specified manga"""
        variables = {'search': manga}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'query': manga_query, 'variables': variables}) as resp:
                json = await resp.json()

        if not json:
            await context.reply("Manga not found")
            return
        else:
            json = json["data"]["Media"]

        try:
            json['description'] = clean_html(json['description'])
        except:
            pass

        embed: discord.Embed = discord.Embed(title=f"{json['title']['romaji']}",
        description=f"Type: {json['format']}\nStatus: {json['status']}\nChapters: {json['chapters']}\nVolumes: \
        {json['volumes']}\nScore: {json['averageScore']}\nGenres: {', '.join(json['genres'])}\n\n{json['description']}")
        
        try:
            embed.color=int(json['coverImage']['color'][1:], 16)
        except TypeError:
            embed.color=0x3577ff

        if json['bannerImage']:
            embed.set_image(url=json['bannerImage'])

        try:
            embed.set_thumbnail(url=json['coverImage']['extraLarge'])
        except:
            pass
        
        await context.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(Anime(client))
