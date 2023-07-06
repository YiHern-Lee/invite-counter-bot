from telegram import Update
from telegram.ext import ContextTypes

from src.db.main import migrateDataHandler
from src.group_monitor.main import updateGroupId

MIGRATE_DATA_PRINT_LINE = 'Migrated data for group_id {} to {}'

async def migrateGroupChat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    old_chat_id = update.message.migrate_from_chat_id
    new_chat_id = update.message.chat.id

    if not old_chat_id:
        # Unable to migrate chat
        return
    
    migrateDataHandler(old_chat_id, new_chat_id)
    updateGroupId(old_chat_id, new_chat_id)
    print(MIGRATE_DATA_PRINT_LINE.format(str(old_chat_id), str(new_chat_id)))
