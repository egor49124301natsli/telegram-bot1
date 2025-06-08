def add_user(user_id, is_premium=False):
    from .session import load_users, save_users
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {"is_premium": is_premium}
        save_users(users)

def set_premium(user_id, value=True):
    from .session import load_users, save_users
    users = load_users()
    if str(user_id) in users:
        users[str(user_id)]["is_premium"] = value
        save_users(users)

def is_premium(user_id):
    from .session import load_users
    users = load_users()
    return users.get(str(user_id), {}).get("is_premium", False)
