import json
from config import Config

def add_dev(member_id: int) -> None:
    """Adds the dev, updates config"""
    Config.devs.append(member_id)

    with open("config.json", 'r+') as file:
        data = json.load(file)
        data["devs"].append(member_id)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def remove_dev(member_id: int) -> None:
    """Removes the dev, updates config"""
    Config.devs.remove(member_id)

    with open("config.json", 'r+') as file:
        data = json.load(file)
        data["devs"].remove(member_id)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
