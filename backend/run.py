from app import create_app, db
import os

app = create_app()


def create_admin():
    with app.app_context():
        db.create_all()
        from app.models import User

        admin_username = "admin"
        admin_password = "admin123"
        admin_email = "admin@quizmaster.com"
        admin_full_name = "Quiz Admin"
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username=admin_username,
                password=admin_password,
                email=admin_email,
                full_name=admin_full_name,
                is_admin=True,
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin/admin123")
        else:
            print("Admin user already exists.")


if __name__ == "__main__":

    create_admin()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
