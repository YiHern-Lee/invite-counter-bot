from telegram import Update

def isGroupChat(update: Update) -> bool:
    return update.message.from_user.id != update.message.chat.id

async def isUserAnAdmin(update: Update) -> bool:
    admins = await update.effective_chat.get_administrators()
    for admin in admins:
        if admin.user == update.message.from_user:
            return True
    return False
