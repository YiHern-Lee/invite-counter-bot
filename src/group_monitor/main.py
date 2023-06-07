from src.group_monitor.model import GroupListHandler

GROUP_LIST_HANDLER = GroupListHandler()

def isGroupInList(groupId: int) -> bool:
    return GROUP_LIST_HANDLER.isGroupInList(groupId)

def addGroupToList(groupId: int):
    GROUP_LIST_HANDLER.addGroupToList(groupId)

def removeGroupFromList(groupId: int):
    GROUP_LIST_HANDLER.removeGroupFromList(groupId)
