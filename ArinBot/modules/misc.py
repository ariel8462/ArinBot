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
            await context.reply("Not enough permissions to change nickname or the user is an admin")
            return
        except Exception as e:
            await context.reply(e)
            return

        if not nick:
            await context.reply(f"Resetted the nickname of {member.name}")
            return

        await context.reply(f"Changed the nickname of {member.name}")

    @commands.command(aliases=["count", "member_count"])
    async def members(self,  context: commands.Context):
        """Sends the member count"""
        await context.send(f"The server has {context.guild.member_count} members")

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
    async def invite(self, context: commands.Context):
        """Sends a bot invite link"""
        await context.reply(discord.utils.oauth_url(self.client.user.id))


def setup(client: commands.Bot):
    client.add_cog(Misc(client))
