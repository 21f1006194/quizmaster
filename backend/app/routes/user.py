from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Api, Resource
from flask import Blueprint
from app.models import User

user_bp = Blueprint("user_api", __name__)

user_api = Api(user_bp)


class ProfileInfo(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"msg": "User not found"}, 404
        return {
            "user_id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "date_of_birth": str(user.date_of_birth),
            "role": "admin" if user.is_admin else "user",
        }, 200


user_api.add_resource(ProfileInfo, "/profileinfo")
