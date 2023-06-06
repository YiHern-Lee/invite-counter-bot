from src.db.model import DataHandler

DATA_HANDLER_MAP = {}

def _getDataHandler(groupId: int) -> DataHandler:
    if groupId in DATA_HANDLER_MAP:
        return DATA_HANDLER_MAP.get(groupId)
    DATA_HANDLER_MAP[groupId] = DataHandler(groupId)
    return DATA_HANDLER_MAP.get(groupId)

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
