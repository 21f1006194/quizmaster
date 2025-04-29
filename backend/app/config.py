import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "4ce4ba18b8dedb84629da4be421c1d2d"
    JWT_SECRET_KEY = "edb84629da4be421c1d2d4ce4ba18b8d"
    STATIC_FOLDER = "static"
    FILE_UPLOAD_FOLDER = "static/uploads/files"
    IMAGE_UPLOAD_FOLDER = "static/uploads/images"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_FILE_EXTENSIONS = ["pdf"]
    ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


# creatw the file_upload_folder and image_upload_folder if not exist inside the static folder
base_path = os.path.abspath(os.path.dirname(__file__))
file_upload_folder = os.path.join(base_path, Config.FILE_UPLOAD_FOLDER)
image_upload_folder = os.path.join(base_path, Config.IMAGE_UPLOAD_FOLDER)

for folder in [file_upload_folder, image_upload_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created {folder}")
