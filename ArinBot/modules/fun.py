import discord
from discord.ext import commands
import random
from config import Config
import utils.fun as fun

class Fun(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    async def decide(self, context: commands.Context) -> None:
        """Decides. replies yes/no"""
        await context.reply(random.choice(["yes", "no"]))

    @commands.command(aliases=["coinflip"])
    async def coin(self, context: commands.Context) -> None:
        """Tosses a coin"""
        await context.reply(random.choice(["head", "tails"]))

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

def setup(client: commands.Bot):
    client.add_cog(Fun(client))
