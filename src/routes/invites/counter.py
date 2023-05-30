from telegram import Update
from telegram.ext import ContextTypes

from src.db.query import increaseInviteCount

async def newMemberInvited(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    group_id = update.message.chat.id
    username = update.message.from_user.username
    increaseInviteCount(groupId=group_id, userId=user_id, username=username, invitedMembers=update.message.new_chat_members)
