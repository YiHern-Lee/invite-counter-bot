import atexit

from src.db.group_monitor import addGroupToList, isGroupInList, removeGroupFromList, updateGroupId
from src.db.pyson import DataHandler
from src.model.model import DBCli, overrides

DATA_HANDLER_MAP: dict[int, 'DataHandler']
DATA_HANDLER_MAP = {}

class PysonDBCli(DBCli):

    @overrides(DBCli)
    def addUserToDB(self, groupId: int, _: int, data: dict):
        addUserToDB(groupId, data)

    @overrides(DBCli)
    def updateUserInDB(self, groupId: int, _: int, data: dict):
        dataId = data.get("id", 0)
        if dataId == 0:
            return
        updateUserInDB(groupId, dataId, data)

    @overrides(DBCli)
    def getUserInviteData(self, groupId: int, userId: int) -> dict:
        return getUserInviteData(groupId, userId)
    
    @overrides(DBCli)
    def getAllUserData(self, groupId: int) -> list[dict[str, any]]:
        return getAllUserData(groupId)

    @overrides(DBCli)
    def userJoin(self, groupId: int, userId: int):
        userJoin(groupId, userId)

    @overrides(DBCli)
    def hasUserJoined(self, groupId: int, invitedUserId: int) -> bool: 
        return hasUserJoined(groupId, invitedUserId)

    @overrides(DBCli)
    def migrateDataHandler(self, oldGroupId: int, newGroupId: int):
        migrateDataHandler(oldGroupId, newGroupId)
        updateGroupId(oldGroupId, newGroupId)

    @overrides(DBCli)
    def isGroupInList(self, groupId: int) -> bool:
        return isGroupInList(groupId)

    @overrides(DBCli)
    def addGroupToList(self, groupId: int):
        addGroupToList(groupId)

    @overrides(DBCli)
    def removeGroupFromList(self, groupId: int):
        removeGroupFromList(groupId)

def get_pysondb_cli() -> PysonDBCli:
    return PysonDBCli()

def _getDataHandler(groupId: int) -> DataHandler:
    if groupId in DATA_HANDLER_MAP:
        return DATA_HANDLER_MAP.get(groupId)
    DATA_HANDLER_MAP[groupId] = DataHandler(groupId)
    return DATA_HANDLER_MAP.get(groupId)

def _removeDataHandler(groupId: int):
    if groupId in DATA_HANDLER_MAP:
        DATA_HANDLER_MAP.pop(groupId)

def addUserToDB(groupId: int, data: dict):
    data_handler = _getDataHandler(groupId)
    data_handler.addToDb(data)

def updateUserInDB(groupId: int, dataId: int, data: dict):
    data_handler = _getDataHandler(groupId)
    data_handler.updateDb(dataId, data)

def getUserInviteData(groupId: int, userId: int) -> dict:
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
