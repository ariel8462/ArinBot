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
