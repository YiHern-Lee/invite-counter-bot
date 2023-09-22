from telegram import Update
from telegram.ext import ContextTypes

from src.db.query import increaseInviteCount, userJoinWithoutInvitation
from src.routes.filters import isGroupBeingMonitored

async def newMemberJoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isGroupBeingMonitored(update):
        return 
    
    from_user = update.message.from_user
    new_chat_members = update.message.new_chat_members

    user_id = update.message.from_user.id if update.message.from_user.id != None else -1
    group_id = update.message.chat.id if update.message.chat.id != None else -1

    if from_user in new_chat_members:
        userJoinWithoutInvitation(groupId=group_id, userId=user_id)
    else:
        increaseInviteCount(groupId=group_id, user=from_user, invitedMembers=new_chat_members)
