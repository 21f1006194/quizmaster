from flask_jwt_extended import get_jwt, jwt_required
from functools import wraps
from flask_restful import Api, Resource
from flask import Blueprint, request
from app.models import User

admin_bp = Blueprint("admin_api", __name__)

admin_api = Api(admin_bp)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"msg": "Admin access only"}, 403
        return fn(*args, **kwargs)

    return wrapper


class UserList(Resource):
    @admin_required
    def get(self):
        users = User.query.all()
        return {"users": [user.full_name for user in users]}, 200


admin_api.add_resource(UserList, "/userlist")
