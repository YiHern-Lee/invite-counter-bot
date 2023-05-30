from telegram.ext import filters

from src.routes.models.Command import Command
from src.routes.models.Message import MessageAction

from src.routes.invites.counter import newMemberInvited
from src.routes.invites.get import leaderboard

def getMessageActions() -> list[MessageAction]:
    # Pack all Message Actions: 
    # Message Actions have the following; 1. filter for messages that trigger the action & 2. function to trigger
    new_member_actions = MessageAction(filters.StatusUpdate.NEW_CHAT_MEMBERS, newMemberInvited)

    return [new_member_actions]

def getCommands() -> list[Command]:
    # Pack all Commands: 
    # Commands have the following; 1. command keyword 'e.g /top' & 2. function to trigger
    leaderboardCmd = Command('top', leaderboard)

    return [leaderboardCmd]