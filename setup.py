import asyncio
import os

from telegram.ext import Application

from src.telegram_credentials.credentials_loader import getCredentialsMap
from routes.actions import getCommandInstructions

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PATH_TO_KEY = CURRENT_PATH + "/src/telegram_credentials/key.txt"
PATH_TO_CRED = CURRENT_PATH + "/credentials.txt"

TELEGRAM_BOT_API_KEY_DICT_KEY = 'telegram-bot-api-key'

def main():
    credentialsMap = getCredentialsMap(PATH_TO_KEY, PATH_TO_CRED)
    token = credentialsMap.get(TELEGRAM_BOT_API_KEY_DICT_KEY)
    if not token:
        print("Bot token is missing")
        return
    app = Application.builder().token(token).build()
    try:
        asyncio.run(app.bot.set_my_commands(getCommandInstructions()))
    except asyncio.TimeoutError:
        print("Failed to set Commands")

if __name__ == '__main__':
    main()
