from typing import TypedDict

from app.auth.security import Role, hash_password, verify_password


class UserRecord(TypedDict):
    username: str
    hashed_password: str
    role: Role


_users: dict[str, UserRecord] = {
    "employee_demo": {
        "username": "employee_demo",
        "hashed_password": hash_password("employee123"),
        "role": "employee",
    },
    "admin_demo": {
        "username": "admin_demo",
        "hashed_password": hash_password("admin123"),
        "role": "admin",
    },
}


def authenticate_user(username: str, password: str) -> UserRecord | None:
    user = _users.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user
