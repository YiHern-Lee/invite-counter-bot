from pymongo import MongoClient
from pymongo.database import Database
from src.model.model import DBCli, overrides

_DB_NAME = "inviteCountDb"
_INVITES_COLLECTION = "invites"
_GROUP_MON_COLLECTION = "groups"
_USERS_COLLECTION = "users"
_ALL_COLLECTIONS = [_INVITES_COLLECTION, _GROUP_MON_COLLECTION,  _USERS_COLLECTION]

_default_loc = "mongodb://localhost:27017/"

class MongoDBClient(DBCli):
    def __init__(self, loc):
        if loc == "":
            loc = _default_loc
        self.cli = MongoClient(loc)

    @overrides(DBCli)
    def addUserToDB(self, groupId: int, userId: int, data: dict):
        db = self._get_db()
        invites = db[_INVITES_COLLECTION]
        invites.update_one(
            {"group_id": str(groupId)},
            {"$set": {f"users.{str(userId)}": data}},
            upsert=True # 1 to insert document if empty
        )

    @overrides(DBCli)
    def updateUserInDB(self, groupId: int, userId:int, data: dict):
        db = self._get_db()
        invites = db[_INVITES_COLLECTION]
        invites.update_one(
            {"group_id": str(groupId)},
            {"$set": {f"users.{str(userId)}": data}},
            upsert=True
        )

    @overrides(DBCli)
    def getUserInviteData(self, groupId: int, userId: int) -> dict:
        db = self._get_db()
        invites = db[_INVITES_COLLECTION]

        result = invites.find_one(
            {"group_id": str(groupId)},
            {f"users.{str(userId)}": 1, "_id": 0} # projection of 1 to include, 0 to exclude
        )
        if not result:
            return {}

        user_data = result.get("users", {}).get(str(userId), {})
        return user_data

    @overrides(DBCli)
    def getAllUserData(self, groupId: int) -> list[dict[str, any]]:
        db = self._get_db()
        invites = db[_INVITES_COLLECTION]
        result = invites.find_one(
            {"group_id": str(groupId)},
            {"group_id": 1, "users": 1, "_id": 0}  # Project only the 'users' field and exclude '_id'
        )
        if not result:
            return []
        users_res = []
        users_data = result.get("users", {})
        for _, user_data in users_data.items():
            users_res.append(user_data)
        return users_res

    @overrides(DBCli)
    def userJoin(self, groupId: int, userId: int):
        db = self._get_db()
        users = db[_USERS_COLLECTION]
        users.update_one(
            {"group_id": str(groupId)},
            {"$set": {f"users.{str(userId)}": True}},
            upsert=True
        )

    @overrides(DBCli)
    def hasUserJoined(self, groupId: int, invitedUserId: int) -> bool: 
        db = self._get_db()
        users = db[_USERS_COLLECTION]
        result = users.find_one(
            {"group_id": str(groupId), f"users.{str(invitedUserId)}": {"$exists": True}},
            {"_id": 0}
        )
        return True if result else False

    @overrides(DBCli)
    def migrateDataHandler(self, oldGroupId: int, newGroupId: int):
        db = self._get_db()
        for collection_key in _ALL_COLLECTIONS:
            collection = db[collection_key]
            collection.update_one(
                {"group_id", str(oldGroupId)},
                {"$set": {"group_id": str(newGroupId)}},
                upsert=True
            )

        

    @overrides(DBCli)
    def isGroupInList(self, groupId: int) -> bool:
        db = self._get_db()
        groups = db[_GROUP_MON_COLLECTION]
        result = groups.find_one(
            {"group_id": str(groupId)},
            {"_id": 0}
        )
        return True if result else False

    @overrides(DBCli)
    def addGroupToList(self, groupId: int):
        db = self._get_db()
        groups = db[_GROUP_MON_COLLECTION]
        groups.update_one(
            {"group_id": str(groupId)},
            {"$set": {f"group_id": str(groupId)}},
            upsert=True # 1 to insert document if empty
        )

    @overrides(DBCli)
    def removeGroupFromList(self, groupId: int):
        db = self._get_db()
        groups = db[_GROUP_MON_COLLECTION]
        groups.delete_one(
            {"group_id": str(groupId)}
        )

    def _get_db(self) -> Database:
        return self.cli[_DB_NAME]

def get_mongodb_cli(args: list[str]) -> MongoDBClient:
    loc = ""
    if len(args) > 0:
        loc = args[0]
    return MongoDBClient(loc)
