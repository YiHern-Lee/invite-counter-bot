from telegram import Update
from telegram.ext import ContextTypes

from src.db.query import getTopNInviters
from src.routes.filters import isGroupChat

LEADERBOARD_OPENING_MSG = "🎉🎉 <b>LEADERBOARD</b> 🎉🎉\n<i>Number of Invites</i>\n"
EMPTY_LEADERBOARD_MSG = "Leaderboard is empty right now!"

DEFAULT_NUMBER_OF_INVITERS = 10

NOT_A_GROUP_CHAT_LINE = "Sorry, this command can only be used in a group chat."

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isGroupChat(update):
        return await update.message.reply_text(NOT_A_GROUP_CHAT_LINE, quote=False)
    
    group_id = update.message.chat.id
    n = _extractNForLeaderboard(context.args)

    top_n_users = getTopNInviters(group_id, n)

    line = ''
    if not top_n_users: 
        line = EMPTY_LEADERBOARD_MSG
    else: 
        line = LEADERBOARD_OPENING_MSG

    for i in range(len(top_n_users)):
        line += str(i + 1) + ". " + top_n_users[i].get("username") + ": " + str(top_n_users[i].get("inviteCount")) + "\n"
    return await update.message.reply_text(line, quote=False, parse_mode='html')

def _extractNForLeaderboard(args: list[str]) -> int:
    # Try to get the first arg
    first_arg = args[0] if len(args) > 0 else '0'
    try:
        n = int(first_arg)
        if n <= 0: 
            n = DEFAULT_NUMBER_OF_INVITERS
        return n
    except:
        return DEFAULT_NUMBER_OF_INVITERS
