from app.models.user import User
from app import db


def get_all_users():
    users = User.query.all()
    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "qualification": user.qualification,
            "isBlocked": user.is_blocked,
        }
        for user in users
        if not user.is_admin
    ]


def block_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise Exception("User not found")
    user.is_blocked = True
    db.session.commit()
    return user


def unblock_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise Exception("User not found")
    user.is_blocked = False
    db.session.commit()
    return user
