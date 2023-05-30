import os
from pysondb import db

DB_MAP = {}

PATH_TO_DATA = os.path.dirname(os.path.abspath(__file__)) + '/data/'

def _findPathToDB(groupId: int) -> str:
    # Checks if path to folder exists; if false, create folder
    path_to_group_data = PATH_TO_DATA + str(groupId) + '/'
    if not os.path.exists(path_to_group_data): 
        os.makedirs(path_to_group_data)
    return path_to_group_data

def _getDB(groupId: int) -> db.JsonDatabase:
    if groupId in DB_MAP:
        return DB_MAP.get(groupId)
    path_to_db = _findPathToDB(groupId) + str(groupId) + ".json"
    new_db = db.getDb(path_to_db)
    DB_MAP[groupId] = new_db
    return new_db

def addToDB(groupId: int, data: dict):
    db_to_add = _getDB(groupId)
    db_to_add.add(data)

def updateDB(groupId: int, dataId: int, data: dict):
    db_to_update = _getDB(groupId)
    db_to_update.updateById(dataId, data)

def getUserData(groupId: int, userId: int) -> dict:
    db_to_get = _getDB(groupId)
    user_data = db_to_get.getBy({"userId": userId})
    if not user_data or "id" not in user_data[0]:
        return {}
    return user_data[0]

def getAllUserData(groupId: int) -> list[dict[str, any]]:
    db_to_get = _getDB(groupId)
    return db_to_get.getAll()
