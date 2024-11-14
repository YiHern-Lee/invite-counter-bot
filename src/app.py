from telegram.ext import Application

from src.routes.actions import getHandlers
from src.service.query import init_db_cli

def checkRunParams(port: str): 
    if not port.isdigit():
        raise TypeError("Port number should be an integer")

def init_db(args: list[str]):
    db_type = ""
    if len(args) > 0:
        db_type = args[0]
    init_db_cli(db_type, args[1:])
    
def run(token: str, port: str, webhook_url: str, args: list[str]):
    init_db(args)
    checkRunParams(port)

    app = Application.builder().token(token).build()

    app.add_handlers(getHandlers())

    app.run_webhook(
        listen = '0.0.0.0',
        port = port,
        url_path = '/',
        webhook_url = webhook_url
    )
