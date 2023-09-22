from telegram import Update
from telegram.ext import ContextTypes

START_LINE = """
Hi! I am <b>Invite Counter Bot</b>!

To use me, simply add me into a group chat. 
I will keep track of the number of users invited by each group member! 
Only invites of new users who have <b>never been in the group</b> will be counted.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return await update.message.reply_text(START_LINE, quote=False, parse_mode='html')
    