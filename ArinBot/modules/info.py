import discord
from discord.ext import commands
from utils.info import *

class Info(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(aliases=["whois"])
    async def info(self, context: commands.Context, member: discord.Member = None) -> None:
        if context.message.reference and not member:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author
        elif not member:
            member = context.author
        
        embed: discord.Embed = discord.Embed(title="", description=member.mention, color=member.color)
        embed.set_author(name=member, icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Joined", value=member.joined_at.strftime('%d.%m.%Y'))
        embed.add_field(name="Registered", value=member.created_at.strftime('%d.%m.%Y'))
        embed.add_field(name=f"Roles[{len(member.roles) - 1}]", value=get_roles_mention(member), inline=False)

        acknowledgements_string = get_acknowledgements(member, context)
        
        if acknowledgements_string:
            embed.add_field(name="Acknowledgements", value=acknowledgements_string)

        embed.set_footer(text=f"ID: {member.id}")

        await context.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(Info(client))
