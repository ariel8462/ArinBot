import discord
from discord.ext import commands
import random
from config import Config
import utils.fun as fun
import aiohttp

class Fun(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def decide(self, context: commands.Context) -> None:
        """Decides. replies yes/no"""
        await context.reply(random.choice(["Yes", "No", "Maybe"]))

    @commands.command(aliases=["flip"])
    async def coin(self, context: commands.Context) -> None:
        """Tosses a coin"""
        await context.reply(random.choice(["Heads", "Tails"]))

    @commands.command()
    async def slap(self, context: commands.Context, member: discord.Member = None) -> None:
        """Slaps a user"""
        if context.message.reference is not None:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author

        if member is None:
            await context.reply(f"No user spcified:\n{Config.COMMAND_PREFIX}slap <username/id>\n{Config.COMMAND_PREFIX}slap as a reply")
            return

        if member.id is self.client.user.id:
            await context.send("Stop slapping me. REEEEEEEEEEEEEE.")
            return

        user1 = context.author.name
        user2 = member.name

        slap_template = random.choice(fun.SLAP_TEMPLATES)
        item = random.choice(fun.ITEMS)
        hit = random.choice(fun.HIT)
        throw = random.choice(fun.THROW)

        reply = slap_template.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)
        await context.send(reply)

    @commands.command()
    async def runs(self, context: commands.Context) -> None:
        """Sends a 'runs' string"""
        await context.send(random.choice(fun.RUN_STRINGS))

    @commands.command()
    async def ud(self, context: commands.Context, *, word: str) -> None:
        """Searches a term on Urban Dictionary"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.urbandictionary.com/v0/define?term={word}") as response:
                text = await response.json()

        try:
            definition = fun.replace_text(text['list'][0]['definition'])
            examples = fun.replace_text(text['list'][0]['example'])
        except IndexError:
            await context.reply("No such term on Urban Dictionary, maybe you made a typo")
            return
        except Exception as e:
            await context.reply(e)
            return
        
        embed = discord.Embed(title=word, description=f"{definition}\n\n*{examples}*", color=discord.Color.orange())
        await context.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
