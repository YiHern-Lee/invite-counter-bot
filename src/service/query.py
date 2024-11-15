from src.mongodb.main import get_mongodb_cli
from src.db.main import get_pysondb_cli
from src.model.model import DBCli

from telegram import User

_query_cli: DBCli
_query_cli = DBCli()

def userJoinWithoutInvitation(groupId: int, userId: int):
    if not _query_cli.hasUserJoined(groupId, userId):
        _query_cli.userJoin(groupId, userId)

def increaseInviteCount(groupId: int, user: User, invitedMembers: tuple[User]):
    if user.id == None:
        return
    # Unpack from_user
    userId = user.id

    # Check if any of the newly invited user has ever been in the group
    invite_count = 0
    for member in invitedMembers:
        if not _query_cli.hasUserJoined(groupId, member.id): 
            _query_cli.userJoin(groupId, member.id)
            invite_count += 1

    if invite_count == 0:
        return

    user_invite_data = _query_cli.getUserInviteData(groupId, userId)
    if not user_invite_data:
        _addNewUser(groupId, user, invite_count)
        return
    user_invite_data["inviteCount"] += invite_count
    _query_cli.updateUserInDB(groupId, userId, user_invite_data)

def getTopNInviters(groupId: int, n: int) -> list[dict[str, any]]:
    all_user_data = _query_cli.getAllUserData(groupId)
    if not all_user_data:
        return all_user_data
    sorted_user_data = sorted(all_user_data, key=lambda x: x["inviteCount"], reverse=True)
    return sorted_user_data[:n]

def _addNewUser(groupId: int, user: User, inviteCount: int):
    if user.id == None:
        return
    userId = user.id
    username = user.username
    name = user.full_name

    new_user_data = {"userId": userId,
                     "username": username,
                     "name": name,
                     "inviteCount": inviteCount}
    _query_cli.addUserToDB(groupId, userId, new_user_data)

def isGroupBeingMonitored(groupId: int) -> bool:
    return _query_cli.isGroupInList(groupId)

def addGroupToList(groupId: int):
    _query_cli.addGroupToList(groupId)

def removeGroupFromList(groupId: int):
    _query_cli.removeGroupFromList(groupId)

def migrateDataHandler(self, oldGroupId: int, newGroupId: int):
    _query_cli.migrateDataHandler(oldGroupId, newGroupId)

def init_db_cli(type: str, args: list[str]):
    global _query_cli
    if type == "mongo":
        _query_cli = get_mongodb_cli(args)
    else:
        _query_cli = get_pysondb_cli()
