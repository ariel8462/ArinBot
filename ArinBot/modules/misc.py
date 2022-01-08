import discord
from discord.ext import commands
from discord.errors import Forbidden
from config import Config
import time
from utils.permissions import *

class Misc(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    async def disabled(self, context: commands.Context) -> None:
        """Shows all disabled commands"""
        commands = self.client.commands
        diabled_commands_string: str = "The disabled commands are:\n"

        for command in commands:
            if not command.enabled:
                diabled_commands_string += f"\t`{Config.COMMAND_PREFIX}{command.name}`\n"
        if not diabled_commands_string:
            await context.reply("No disabled commands")
            return

        await context.reply(diabled_commands_string)

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, context: commands.Context, member: discord.Member, *, nick: str = None) -> None:
        """Changes the nickname of the specified user, resets the nickname by not specifying one"""
        try:
            await member.edit(nick=nick)
        except Forbidden:
            await context.reply("I don't have enough permissions to change nicknames :(")
            return
        except Exception as e:
            await context.reply(e)
            return

        if not nick:
            await context.reply(f"Resetted the nickname of **{member.name}**")
            return

        await context.reply(f"Changed the nickname of **{member.name}**")

    @commands.command(aliases=["count", "member_count"])
    async def members(self,  context: commands.Context):
        """Sends the member count"""
        await context.send(f"The server has **{context.guild.member_count}** members")

    @commands.command()
    @commands.check(is_sudo)
    async def ping(self, context: commands.Context) -> None:
        """Pings, Checks the connection - only available for devs and owners"""
        start_time = time.time()
        message = await context.send("Pinging...")
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000, 3)
        await message.edit(content=str(ping_time) + " ms")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, context: commands.Context, *, text: str = None) -> None:
        """Echos the text you write after /echo"""
        if text:
            await context.message.delete()
            await context.send(text)
        else:
            await context.reply(f"Text to echo not specified:\n{Config.COMMAND_PREFIX}echo <text>")

    @commands.command()
    async def invite(self, context: commands.Context) -> None:
        """Sends a bot invite link"""
        await context.reply(discord.utils.oauth_url(self.client.user.id))

    @commands.command()
    async def avatar(self, context: commands.Context, member: discord.Member = None) -> None:
        """Sends the avatar of the specified user"""
        if context.message.reference is not None:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author

        if member is None:
            member = context.author
        
        message = discord.Embed(title=str(member), color=discord.Colour.blue())
        message.set_image(url=member.avatar_url)

        await context.send(embed=message)

    @commands.command()
    async def server_avatar(self, context: commands.Context) -> None:
        """Gets the current's server avatar"""
        if not context.guild.icon:
            return await context.send("The server doesn't have an avatar")

        message = discord.Embed(title=str(context.guild.name), color=discord.Colour.blue())
        message.set_image(url=context.guild.icon_url)

        await context.send(embed=message)

    @commands.command()
    async def id(self, context: commands.Context, member: discord.Member = None) -> None:
        """Returns the id of the specified user, by tag/reply"""
        if not member and not context.message.reference:
            await context.reply(context.author.id)
            return
        elif context.message.reference and not member:
            message: discord.Message = await context.channel.fetch_message(context.message.reference.message_id)
            member: discord.User = message.author      

        await context.reply(member.id)  

    @commands.command()
    async def roles(self, context: commands.Context) -> None:
        """Gets all the roles in an hierarchical order"""
        description: str = ""
        count: int = 0
        role: discord.Role
        
        for role in context.guild.roles[::-1]:
            description += f"{role.mention}\n"
            count += 1

        embed = discord.Embed(title=f"Roles[{count}]", color=discord.Colour.blue(), description=description)
        await context.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(Misc(client))
