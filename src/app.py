from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes

from src.routes.getActions import getMessageActions, getCommands
from src.routes.models.Command import Command
from src.routes.models.Message import MessageAction

def checkRunParams(port: str): 
    if not port.isdigit():
        raise TypeError("Port number should be an integer")
    
def addHandlers(app: Application, commands: list[Command], msgActions: list[MessageAction]):
    for command in commands:
        word, func = command.getCommand()
        app.add_handler(CommandHandler(word, func))
    for msgAction in msgActions:
        filter_str, func = msgAction.getMessageAction()
        app.add_handler(MessageHandler(filter_str, func))
    
def run(token: str, port: str, webhook_url: str):
    checkRunParams(port)
    app = Application.builder().token(token).build()
    
    commands = getCommands()
    msgActions = getMessageActions()
    
    # Commands
    addHandlers(app, commands, msgActions)

    app.run_webhook(
        listen = '0.0.0.0',
        port = port,
        url_path = '/',
        webhook_url = webhook_url
    )
