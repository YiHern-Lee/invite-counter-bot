import atexit

from src.db.pyson import GroupListHandler

GROUP_LIST_HANDLER = GroupListHandler()

def isGroupInList(groupId: int) -> bool:
    return GROUP_LIST_HANDLER.isGroupInList(groupId)

def addGroupToList(groupId: int):
    GROUP_LIST_HANDLER.addGroupToList(groupId)

def removeGroupFromList(groupId: int):
    GROUP_LIST_HANDLER.removeGroupFromList(groupId)

def updateGroupId(oldGroupId: int, newGroupId: int):
    GROUP_LIST_HANDLER.updateGroupId(oldGroupId, newGroupId)

def saveGroupMonitoringList():
    GROUP_LIST_HANDLER.saveGroupList()

atexit.register(saveGroupMonitoringList)