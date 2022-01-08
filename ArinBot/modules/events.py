import discord
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, CommandNotFound, DisabledCommand, MissingPermissions
from config import Config

class Events(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error: commands.errors) -> None:
        """Executes if a command errors out"""
        if isinstance(error, CommandNotFound):
            await context.reply("The command specified was not found.")
        elif isinstance(error, MissingPermissions):
            await context.reply("You don't have enough permissions for this command.")
        elif isinstance(error, DisabledCommand):
            pass
        elif isinstance(error, CheckFailure):
            pass
        else:
            await context.reply(error)
        return

    @commands.Cog.listener()
    async def on_command_completion(self, context: commands.Context) -> None:
        """On each command completion, prints details about the command author in order to help in cases of spam"""
        print(f"[X] {context.author.name} ({context.author.id}) used {Config.COMMAND_PREFIX}{context.command}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        print(f"[+] {member.name} ({member.id}) joined")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Adds the role 'muted-<BOT_NAME>' for future mutes"""
        print(f"[+] Joined '{guild.name}'")

        muted_role: discord.role.Role = next((r for r in guild.roles if r.name == f"muted-{Config.BOT_NAME}"), None)

        if muted_role:
            return
        else:
            muted_role = await guild.create_role(name=f"muted-{Config.BOT_NAME}", permissions=discord.Permissions(2147746368))

        for channel in guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

        print(f"[+] Added role for future mutes in '{guild.name}'")


def setup(client: commands.Bot):
    client.add_cog(Events(client))
