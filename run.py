import os
from src import app
from src.telegram_credentials import credentials_loader
import sys

###
# Do not directly run this file. 
# Use run.sh to start up ngrok and the bot app.
###

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PATH_TO_KEY = CURRENT_PATH + "/src/telegram_credentials/key.txt"
PATH_TO_CRED = CURRENT_PATH + "/credentials.txt"

TELEGRAM_BOT_API_KEY_DICT_KEY = 'telegram-bot-api-key'

def main():
    if len(sys.argv) < 3:
        print("Number of arguments is insufficient.")
        print("Run the program with command line arguments: <port_number> <webhook_url>")
        return
    credentialsMap = credentials_loader.getCredentialsMap(PATH_TO_KEY, PATH_TO_CRED)
    try:
        app.run(credentialsMap[TELEGRAM_BOT_API_KEY_DICT_KEY], sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
