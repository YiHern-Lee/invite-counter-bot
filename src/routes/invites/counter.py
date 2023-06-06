from telegram import Update
from telegram.ext import ContextTypes

from src.db.query import increaseInviteCount, userJoinWithoutInvitation

async def newMemberJoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from_user = update.message.from_user
    new_chat_members = update.message.new_chat_members

    user_id = update.message.from_user.id
    group_id = update.message.chat.id
    username = update.message.from_user.username

    if from_user in new_chat_members:
        userJoinWithoutInvitation(groupId=group_id, userId=user_id)
    else:
        increaseInviteCount(groupId=group_id, userId=user_id, username=username, invitedMembers=new_chat_members)
