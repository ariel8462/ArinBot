import discord
from discord.ext import commands
from config import Config
import json


def set_config() -> str:
    """Sets the bot config using the settings specified in 'config.json'"""
    with open("config.json", 'r') as file:
        data = json.load(file)

    Config.BOT_NAME = data["bot_name"]

    for owner in data["owners"]:
        Config.owners.append(owner)

    for dev in data["devs"]:
        Config.devs.append(dev) 
    
    Config.COMMAND_PREFIX = data["prefix"]

    return data["token"]

def start_bot(Bot: commands.Bot) -> None:
    """Starts the bot"""
    token = set_config()
    intents = discord.Intents.default()
    intents.members = True
    intents.guilds = True
    client = commands.Bot(command_prefix=Config.COMMAND_PREFIX, intents=intents, case_insensitive=True)
    client.add_cog(Bot(client))
    client.run(token)
