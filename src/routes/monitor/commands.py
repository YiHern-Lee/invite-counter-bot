from telegram import Update
from telegram.ext import ContextTypes

from src.service.query import isGroupBeingMonitored, addGroupToList, removeGroupFromList
from src.service.filters import isGroupChat, isUserAnAdmin

NOT_A_GROUP_CHAT_LINE = "Sorry, invites recording is only for group chats!"
GROUP_NOT_UNDER_MONITORING_LINE = "I am not 🙅‍♂️ monitoring this group!"
GROUP_UNDER_MONITORING_LINE = "I am already monitoring 👀 this group!"
SUCCESS_REMOVE_LINE = "I have removed this group from my list!\nI will stop ⛔️ monitoring this group!"
SUCCESS_ADD_LINE = "I have added this group to my list ✅\nI will start to monitor this group!"
USER_NOT_ADMIN = "Sorry, only an admin of the group can run this command."

async def startRecord(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isGroupChat(update):
        return await update.message.reply_text(NOT_A_GROUP_CHAT_LINE, quote=False)
    
    if not await isUserAnAdmin(update):
        return await update.message.reply_text(USER_NOT_ADMIN, quote=False)
    
    group_id = update.message.chat.id
    
    if isGroupBeingMonitored(group_id):
        return await update.message.reply_text(GROUP_UNDER_MONITORING_LINE, quote=False)
    
    addGroupToList(group_id)

    return await update.message.reply_text(SUCCESS_ADD_LINE, quote=False)

async def stopRecord(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isGroupChat(update):
        return await update.message.reply_text(NOT_A_GROUP_CHAT_LINE, quote=False)
    
    if not await isUserAnAdmin(update):
        return await update.message.reply_text(USER_NOT_ADMIN, quote=False)

    group_id = update.message.chat.id
        
    if not isGroupBeingMonitored(group_id):
        return await update.message.reply_text(GROUP_NOT_UNDER_MONITORING_LINE, quote=False)
    
    removeGroupFromList(group_id)

    return await update.message.reply_text(SUCCESS_REMOVE_LINE, quote=False)
