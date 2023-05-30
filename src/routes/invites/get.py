from telegram import Update
from telegram.ext import ContextTypes

from src.db.query import getTopNInviters

NUMBER_OF_INVITERS = 10

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    group_id = update.message.chat.id
    top_n_users = getTopNInviters(group_id, NUMBER_OF_INVITERS)
    line = ""
    if not top_n_users:
        line = "Leaderboard is empty right now!"
    for i in range(len(top_n_users)):
        line += str(i + 1) + ". " + top_n_users[i].get("username") + ": " + str(top_n_users[i].get("inviteCount")) + "\n"
    await update.message.reply_text(line, quote=False)
