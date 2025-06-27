from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import hashlib

upload_bp = Blueprint("upload_api", __name__)
upload_api = Api(upload_bp)


def allowed_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
    )


def get_file_md5(file_data):
    return hashlib.md5(file_data).hexdigest()


class UploadImage(Resource):
    @jwt_required()
    def post(self):
        if "image" not in request.files:
            return {"msg": "No image file provided"}, 400

        file = request.files["image"]

        if file.filename == "":
            return {"msg": "No selected file"}, 400

        if not allowed_image(file.filename):
            return {"msg": "File type not allowed"}, 400

        try:
            # Read file data and generate MD5
            file_data = file.read()
            file_md5 = get_file_md5(file_data)

            # Get original file extension
            original_extension = os.path.splitext(secure_filename(file.filename))[1]

            # Create new filename with MD5
            new_filename = f"{file_md5}{original_extension}"

            # Get the full path
            upload_folder = current_app.config["IMAGE_UPLOAD_FOLDER"]
            filepath = os.path.join(upload_folder, new_filename)

            # If file with same MD5 doesn't exist, save it
            if not os.path.exists(filepath):
                with open(filepath, "wb") as f:
                    f.write(file_data)

            # Return the URL for the image
            return {
                "url": f"/static/uploads/images/{new_filename}",
                "filename": new_filename,
            }, 200

        except Exception as e:
            return {"msg": f"Error uploading file: {str(e)}"}, 500


upload_api.add_resource(UploadImage, "/image")
