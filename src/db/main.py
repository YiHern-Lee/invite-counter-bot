import atexit

from src.db.model import DataHandler

DATA_HANDLER_MAP: dict[int, 'DataHandler']
DATA_HANDLER_MAP = {}

def _getDataHandler(groupId: int) -> DataHandler:
    if groupId in DATA_HANDLER_MAP:
        return DATA_HANDLER_MAP.get(groupId)
    DATA_HANDLER_MAP[groupId] = DataHandler(groupId)
    return DATA_HANDLER_MAP.get(groupId)

def _removeDataHandler(groupId: int):
    if groupId in DATA_HANDLER_MAP:
        DATA_HANDLER_MAP.pop(groupId)

def addToDB(groupId: int, data: dict):
    data_handler = _getDataHandler(groupId)
    data_handler.addToDb(data)

def updateDB(groupId: int, dataId: int, data: dict):
    data_handler = _getDataHandler(groupId)
    data_handler.updateDb(dataId, data)

def getUserData(groupId: int, userId: int) -> dict:
    data_handler = _getDataHandler(groupId)
    return data_handler.getUserData(userId)

def getAllUserData(groupId: int) -> list[dict[str, any]]:
    data_handler = _getDataHandler(groupId)
    return data_handler.getAllUserData()

def userJoin(groupId: int, userId: int):
    data_handler = _getDataHandler(groupId)
    data_handler.userJoin(userId)

def hasUserJoined(groupId: int, invitedUserId: int) -> bool: 
    data_handler = _getDataHandler(groupId)
    return data_handler.hasUserJoined(invitedUserId)

def migrateDataHandler(oldGroupId: int, newGroupId: int):
    new_data_handler = _getDataHandler(newGroupId)
    old_data_handler = _getDataHandler(oldGroupId)
    new_data_handler.migrateDataHandler(old_data_handler)
    _removeDataHandler(oldGroupId)

def _saveData():
    for _, data_handler in DATA_HANDLER_MAP.items():
        data_handler._group_user_handler._saveUserSet()

atexit.register(_saveData)
