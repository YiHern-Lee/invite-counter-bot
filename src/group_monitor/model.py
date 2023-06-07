import atexit
import os

PATH_TO_GROUP_LIST = os.path.dirname(os.path.abspath(__file__)) + '/group_list.txt'

class GroupListHandler:
    def __init__(self):
        self._group_list = self._loadGroupList()
        atexit.register(self._saveGroupList)

    def isGroupInList(self, groupId: int) -> bool:
        return groupId in self._group_list
    
    def addGroupToList(self, groupId: int):
        self._group_list.add(groupId)

    def removeGroupFromList(self, groupId: int):
        if groupId in self._group_list:
            self._group_list.remove(groupId)

    def _loadGroupList(self) -> set[int]:
        group_list = set()
        try:
            with open(PATH_TO_GROUP_LIST, 'rt') as f:
                for line in f.readlines():
                    try:
                        group_id = int(line)
                        group_list.add(group_id)
                    except:
                        continue
        except:
            pass
        return group_list
    
    def _saveGroupList(self):
        with open(PATH_TO_GROUP_LIST, 'wt') as f:
            for group_id in self._group_list:
                f.write(str(group_id) + '\n')
        f.close()
