import atexit
import os

from src.db.main import _findPathToDB

### 
# Stores all users that has ever joined a particular group

# CACHE_MAP is a dictionary with key-value of ('groupId', set of 'userId')
# Data will be stored into text files upon termination of app
# TODO Add configuration setting to not save data and only persist data during run time of the bot
CACHE_MAP = {}

PATH_TO_DATA = os.path.dirname(os.path.abspath(__file__)) + '/data/'

def _loadCache(groupId: int): 
    new_cache = set()
    path_to_cache = _findPathToDB(groupId) + str(groupId) + '-users.txt'
    try:
        with open(path_to_cache, 'rt') as f:
            for line in f.readlines():
                try:
                    user_id = int(line)
                    new_cache.add(user_id)
                except:
                    continue
    except:
        pass
    CACHE_MAP[groupId] = new_cache
    return CACHE_MAP[groupId]

def _getGroupCache(groupId: int) -> set[int]:
    if groupId not in CACHE_MAP:
        CACHE_MAP[groupId] = _loadCache(groupId)
    return CACHE_MAP[groupId]

def hasUserJoined(groupId: int, invitedUserId: int) -> bool: 
    cache = _getGroupCache(groupId)
    
    # User has never been in the group
    if invitedUserId not in cache:
        cache.add(invitedUserId)
        return False
    
    return True

def _saveCache():
    for group_id, cache in CACHE_MAP.items():
        path_to_cache = _findPathToDB(group_id) + str(group_id) + '-users.txt'
        with open(path_to_cache, 'wt') as f:
            for userId in cache:
                f.write(str(userId) + '\n')
        f.close()

atexit.register(_saveCache)
