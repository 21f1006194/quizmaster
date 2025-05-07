from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import validates


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)

    quiz_attempts = db.relationship("QuizAttempt", backref="user", lazy=True)

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
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates("date_of_birth")
    def validate_date_of_birth(self, key, date_of_birth):
        """Ensure DOB is before the current year."""
        current_year = datetime.now().year
        if date_of_birth and date_of_birth.year >= current_year:
            raise ValueError("Date of birth must be before this year.")
        return date_of_birth

    @validates("username")
    def validate_username(self, key, username):
        """Allow only letters, numbers, and underscores."""
        if bool(re.match(r"^\w{3,50}$", username)):
            return username
        raise ValueError(
            "Invalid username. Only letters, numbers, and underscores are allowed."
        )

    @validates("email")
    def validate_email(self, key, email):
        """Validate email format using email_validator."""
        validate_email(email, check_deliverability=False)
        return email
