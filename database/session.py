import os

DB_FILE = os.path.join(os.path.dirname(__file__), "users.txt")

def add_user(user_id: int):
    users = set(get_all_users())
    if user_id not in users:
        with open(DB_FILE, "a", encoding="utf-8") as f:
            f.write(str(user_id) + "\n")

def get_all_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]
