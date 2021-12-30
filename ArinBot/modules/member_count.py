import discord
from discord.ext import commands

class MemberCount(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(aliases=["count", "member_count"])
    async def members(self,  context: commands.Context):
        await context.send(f"The server has {context.guild.member_count} members")


def setup(client: commands.Bot):
    client.add_cog(MemberCount(client))
