class DBCli:
    """
        Interface for db client object
    """
    def addUserToDB(self, groupId: int, userId: int, data: dict):
        raise RuntimeError("Need to override method")

    def updateUserInDB(self, groupId: int, userId: int, data: dict):
        raise RuntimeError("Need to override method")

    def getUserInviteData(self, groupId: int, userId: int) -> dict:
        raise RuntimeError("Need to override method")
    
    def getAllUserData(self, groupId: int) -> list[dict[str, any]]:
        raise RuntimeError("Need to override method")

    def userJoin(self, groupId: int, userId: int):
        raise RuntimeError("Need to override method")

    def hasUserJoined(self, groupId: int, invitedUserId: int) -> bool: 
        raise RuntimeError("Need to override method")

    def migrateDataHandler(self, oldGroupId: int, newGroupId: int):
        raise RuntimeError("Need to override method")

    def isGroupInList(self, groupId: int) -> bool:
        raise RuntimeError("Need to override method")

    def addGroupToList(self, groupId: int):
        raise RuntimeError("Need to override method")

    def removeGroupFromList(self, groupId: int):
        raise RuntimeError("Need to override method")
    
def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider
