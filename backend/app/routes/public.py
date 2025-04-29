from flask_restful import Api, Resource
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from flask_login import login_user

from app.models import User

public_api_bp = Blueprint("api", __name__)

api = Api(public_api_bp)


class Hello(Resource):
    def get(self):
        return jsonify([{"message": "Hello World"}])


class Login(Resource):
    def post(self):
        try:
            data = request.json
            if not data:
                return jsonify({"msg": "Missing or invalid JSON payload"}), 400

            username = data.get("username")
            password = data.get("password")
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                token = create_access_token(
                    identity=username,
                    additional_claims={"is_admin": bool(user.is_admin)},
                )
                login_user(user)  # Optional with Flask-Login
                return {"access_token": token}, 200

            return {"msg": "Bad username or password"}, 401
        except Exception as e:
            print(f"Error during login: {e}")
            return {"msg": "Internal server error"}, 500


class AdminOnly(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("is_admin"):
            return {"msg": "Welcome to the admin dashboard!"}, 200
        return {"msg": "Admin access only"}, 403


api.add_resource(Hello, "/hello")
api.add_resource(Login, "/login")
api.add_resource(AdminOnly, "/admin")
