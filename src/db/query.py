from src.db.main import addToDB, updateDB, getUserInviteData, getAllUserData, userJoin, hasUserJoined

from telegram import User

def userJoinWithoutInvitation(groupId: int, userId: int):
    if not hasUserJoined(groupId, userId):
        userJoin(groupId, userId)

def increaseInviteCount(groupId: int, user: User, invitedMembers: tuple[User]):
    # Unpack from_user
    userId = user.id

    # Check if any of the newly invited user has ever been in the group
    invite_count = 0
    for member in invitedMembers:
        if not hasUserJoined(groupId, member.id): 
            userJoin(groupId, member.id)
            invite_count += 1

    if invite_count <= 0:
        return

    user_invite_data = getUserInviteData(groupId, userId)
    if not user_invite_data:
        _addNewUser(groupId, user, invite_count)
        return
    user_invite_data["inviteCount"] += invite_count
    updateDB(groupId, user_invite_data["id"], user_invite_data)

def getTopNInviters(groupId: int, n: int) -> list[dict[str, any]]:
    all_user_data = getAllUserData(groupId)
    if not all_user_data:
        return all_user_data
    sorted_user_data = sorted(all_user_data, key=lambda x: x["inviteCount"], reverse=True)
    return sorted_user_data[:n]

def _addNewUser(groupId: int, user: User, inviteCount: int):
    userId = user.id
    username = user.username
    name = user.full_name

    new_user_data = {"userId": userId,
                     "username": username,
                     "name": name,
                     "inviteCount": inviteCount}
    addToDB(groupId, new_user_data)
