import atexit
import os
from threading import Lock

from pysondb import db

PATH_TO_DATA = os.path.dirname(os.path.abspath(__file__)) + '/data/'

class DataHandler:
    def __init__(self, groupId: int):
        self._like_count_handler = LikeCountHandler(groupId)
        self._group_user_handler = GroupUserHandler(groupId)

    def addToDb(self, data: dict):
        self._like_count_handler.addToDb(data)

    def updateDb(self, dataId: int, data: dict):
        self._like_count_handler.updateDb(dataId, data)

    def getUserData(self, userId: int) -> dict:
        return self._like_count_handler.getUserData(userId)
    
    def getAllUserData(self) -> list[dict[str, any]]:
        return self._like_count_handler.getAllUserData()
    
    def userJoin(self, userId: int):
        self._group_user_handler.userJoin(userId)

    def hasUserJoined(self, userId: int) -> bool:
        return self._group_user_handler.hasUserJoined(userId) 

class LikeCountHandler:
    def __init__(self, groupId: int):
        self._mutex = Lock()
        self._group_id = groupId
        self._db = self._createDb()
    
    def _createDb(self) -> db.JsonDatabase:
        path_to_db =  _findPathToData(self._group_id) + str(self._group_id) + '.json'
        return db.getDb(path_to_db)
    
    def addToDb(self, data: dict):
        self._mutex.acquire()
        self._db.add(data)
        self._mutex.release()

    def updateDb(self, dataId: int, data: dict):
        self._mutex.acquire()
        self._db.updateById(dataId, data)
        self._mutex.release()

    def getUserData(self, userId: int) -> dict:
        user_data = self._db.getBy({'userId': userId})
        if not user_data or 'id' not in user_data[0]:
            return {}
        return user_data[0]
    
    def getAllUserData(self) -> list[dict[str, any]]:
        return self._db.getAll()

class GroupUserHandler:
    def __init__(self, groupId: int):
        self._mutex = Lock()
        self._group_id = groupId
        self._user_set = self._loadUserSet()
        atexit.register(self._saveUserSet)

    def _loadUserSet(self) -> set[int]:
        new_set = set()
        path_to_set = _findPathToData(self._group_id) + str(self._group_id) + '-users.txt'
        try:
            with open(path_to_set, 'rt') as f:
                for line in f.readlines():
                    try:
                        user_id = int(line)
                        new_set.add(user_id)
                    except:
                        continue
        except:
            pass
        return new_set
    
    def userJoin(self, userId: int):
        self._mutex.acquire()
        if userId not in self._user_set:
            self._user_set.add(userId)
        self._mutex.release()

    def hasUserJoined(self, userId: int) -> bool:
        return userId in self._user_set
    
    def _saveUserSet(self):
        path_to_set = _findPathToData(self._group_id) + str(self._group_id) + '-users.txt'
        with open(path_to_set, 'wt') as f:
            for userId in self._user_set:
                f.write(str(userId) + '\n')
        f.close()

def _findPathToData(groupId: int) -> str:
    # Checks if path to folder exists; if false, create folder
    path_to_group_data = PATH_TO_DATA + str(groupId) + '/'
    if not os.path.exists(path_to_group_data): 
        os.makedirs(path_to_group_data)
    return path_to_group_data
