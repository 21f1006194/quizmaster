from flask_restful import Api, Resource
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import login_user
from sqlalchemy import or_
from app import db
from app.models import User
from datetime import datetime

public_api_bp = Blueprint("api", __name__)

api = Api(public_api_bp)


class Login(Resource):
    def post(self):
        try:
            data = request.json
            if not data:
                return {"msg": "Missing or invalid JSON payload"}, 400

            username = data.get("username")
            password = data.get("password")
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                token = create_access_token(
                    identity=username,
                    additional_claims={"is_admin": bool(user.is_admin)},
                )
                role = "admin" if user.is_admin else "user"
                if user.is_blocked:
                    return {"msg": "User is blocked. Please contact admin."}, 403
                return {
                    "access_token": token,
                    "role": role,
                    "user": user.full_name,
                }, 200

            return {"msg": "Bad username or password"}, 401
        except Exception as e:
            print(f"Error during login: {e}")
            return {"msg": "Internal server error"}, 500


class Register(Resource):
    def post(self):
        try:
            data = request.json
            if not data:
                return {"msg": "Missing or invalid JSON payload"}, 400

            username = data.get("username")
            password = data.get("password")
            c_password = data.get("confirm_password")
            email = data.get("email")
            # email and username should be unique
            user_exist = User.query.filter(
                or_(User.username == username, User.email == email)
            ).count()

            if user_exist > 0:
                return {"msg": "Username or Email already exists"}, 400
            if password != c_password:
                return {"msg": "Passwords do not match"}, 400

            dob = data.get("date_of_birth")
            if dob:
                dob = datetime.strptime(dob, "%Y-%m-%d").date()
            user = User(
                username=username,
                password=password,
                email=email,
                full_name=data.get("full_name"),
                qualification=data.get("qualification"),
                date_of_birth=dob,
                is_admin=False,
            )
            db.session.add(user)
            db.session.commit()

            return {"msg": "User created successfully"}, 201
        except Exception as e:
            print(f"Error during registration: {e}")
            return {"msg": "Internal server error"}, 500


api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
