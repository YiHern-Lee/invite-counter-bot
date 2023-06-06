from src.db.main import addToDB, updateDB, getUserData, getAllUserData, userJoin, hasUserJoined

from telegram import User

def userJoinWithoutInvitation(groupId: int, userId: int):
    if not hasUserJoined(groupId, userId):
        userJoin(groupId, userId)

def increaseInviteCount(groupId: int, userId: int, username: str, invitedMembers: tuple[User]):
    # Check if any of the newly invited user has ever been in the group
    invite_count = 0
    for member in invitedMembers:
        if not hasUserJoined(groupId, member.id): 
            userJoin(groupId, member.id)
            invite_count += 1

    if invite_count <= 0:
        return

    user_data = getUserData(groupId, userId)
    if not user_data:
        _addNewUser(groupId, userId, username, invite_count)
        return
    user_data["inviteCount"] += invite_count
    updateDB(groupId, user_data["id"], user_data)

def getTopNInviters(groupId: int, n: int) -> list[dict[str, any]]:
    all_user_data = getAllUserData(groupId)
    if not all_user_data:
        return all_user_data
    sorted_user_data = sorted(all_user_data, key=lambda x: x["inviteCount"], reverse=True)
    return sorted_user_data[:n]

def _addNewUser(groupId: int, userId: int, username: str, inviteCount: int):
    new_user_data = {"userId": userId,
                     "username": username,
                     "inviteCount": inviteCount}
    addToDB(groupId, new_user_data)
