import os


def load_admin_users():
    raw = os.getenv("ADMIN_USERS", "")
    users = {}
    for entry in raw.split(","):
        if ":" in entry:
            username, password = entry.split(":", 1)
            users[username.strip()] = password.strip()
    if not users:
        users = {"admin": "admin123"}
    return users
