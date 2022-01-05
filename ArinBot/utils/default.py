from config import Config
import json

def set_config() -> str:
    """Sets the bot config, using the settings specified in 'config.json'"""
    with open("config.json", 'r') as file:
        data = json.load(file)

    Config.BOT_NAME = data["bot_name"]

    for i in data["owners"]:
        Config.owners.append(i)

    for i in data["devs"]:
        Config.devs.append(i) 
    
    Config.COMMAND_PREFIX = data["prefix"]

    return data["token"]
