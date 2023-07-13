from telegram import BotCommand
from telegram.ext import filters, BaseHandler, CommandHandler, MessageHandler

from src.routes.basics.actions import migrateGroupChat
from src.routes.basics.commands import start
from src.routes.invites.counter import newMemberJoin
from src.routes.invites.get import leaderboard
from src.routes.monitor.commands import startRecord, stopRecord

def getHandlers() -> list[BaseHandler]:
    # Message Handlers
    return [
        CommandHandler('top', leaderboard),
        CommandHandler('start', start),
        CommandHandler('startrec', startRecord),
        CommandHandler('stoprec', stopRecord),
        
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, newMemberJoin),
        MessageHandler(filters.StatusUpdate.MIGRATE, migrateGroupChat)
    ]

def getCommandInstructions() -> list[tuple[str, str]]:
    return [
        BotCommand('start', 'Instructions for using this bot'),
        BotCommand('top', 'Use /top <n>\nList the top n inviters in the group'),
        BotCommand('startrec', 'Begin monitoring group for invites'),
        BotCommand('stoprec', 'Stop monitoring group for ivnites')
    ]
