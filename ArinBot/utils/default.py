
def get_token() -> str:
    """Returns the bot token"""
    try:
        with open("token.config", 'r') as token_config:
            return token_config.readline()
    except FileNotFoundError:
        print("Enter your bot token at token.config")
        exit()
