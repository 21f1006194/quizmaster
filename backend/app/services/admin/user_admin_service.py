from app.models.user import User


def get_all_users():
    users = User.query.all()
    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "qualification": user.qualification,
        }
        for user in users
        if not user.is_admin
    ]
