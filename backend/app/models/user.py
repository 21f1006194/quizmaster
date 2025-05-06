from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        username,
        password,
        email,
        full_name,
        qualification=None,
        date_of_birth=None,
        is_admin=False,
    ):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.qualification = qualification
        self.date_of_birth = date_of_birth
        self.is_admin = is_admin
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
