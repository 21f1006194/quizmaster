from app import db


class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("quiz_attempt.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    option_id = db.Column(
        db.Integer, db.ForeignKey("option.id"), nullable=True
    )  # Nullable if not attempted
    is_attempted = db.Column(db.Boolean, default=False)

    ## TODO: Add a validator to check the is_attempted field is True if option_id is not None
