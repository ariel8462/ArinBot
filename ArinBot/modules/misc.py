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
    async def nickname(self, context: commands.Context, member: discord.Member, nick: str = None) -> None:
        try:
            await member.edit(nick=nick)
        except Forbidden:
            await context.reply("Not enough permissions to change nickname | or the user is an admin")
            return
        except Exception as e:
            await context.reply(e)
            return

        if nick is None:
            await context.reply(f"Resetted the nickname of {member.name}")
            return

        await context.reply(f"Changed the nickname of {member.name}")

    @commands.command(aliases=["count", "member_count"])
    async def members(self,  context: commands.Context):
        await context.send(f"The server has {context.guild.member_count} members")

    #allow only devs and owners to ping, in order to avoid spam
    @commands.command()
    @commands.check(is_sudo)
    async def ping(self, context: commands.Context) -> None:
        start_time = time.time()
        message = await context.send("Pinging...")
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000, 3)
        await message.edit(content=str(ping_time) + " ms")


def setup(client: commands.Bot):
    client.add_cog(Misc(client))
