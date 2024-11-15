def create_new_user_data(userId: int, username: str, name: str, inviteCount: int) -> dict:
    return {"userId": userId,
            "username": username,
            "name": name,
            "inviteCount": inviteCount}