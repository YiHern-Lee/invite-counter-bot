from telegram.ext import Application

from src.routes.getActions import getHandlers

def checkRunParams(port: str): 
    if not port.isdigit():
        raise TypeError("Port number should be an integer")

    
def run(token: str, port: str, webhook_url: str):
    checkRunParams(port)
    app = Application.builder().token(token).build()

    app.add_handlers(getHandlers())

    app.run_webhook(
        listen = '0.0.0.0',
        port = port,
        url_path = '/',
        webhook_url = webhook_url
    )
