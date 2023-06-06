from telegram import Update

def isGroupChat(update: Update) -> bool:
    return update.message.from_user.id != update.message.chat.id
