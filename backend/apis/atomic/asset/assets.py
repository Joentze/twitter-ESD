"""uploads files to minio bucket"""
import os
import io
import uuid
from requests import get
from flask import Flask, request, jsonify
from flask_cors import CORS
from minio import Minio
from minio.error import S3Error
from urllib3 import HTTPHeaderDict, BaseHTTPResponse


try:
    MINIO_ENDPOINT = os.environ["MINIO_ENDPOINT"]
    MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
    MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
except KeyError:
    MINIO_ENDPOINT = "host.docker.internal:9000"
    MINIO_ACCESS_KEY = "ROOTNAME"
    MINIO_SECRET_KEY = "CHANGEME123"


minio_client = Minio(endpoint=MINIO_ENDPOINT, secure=False,
                     access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY)
app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["POST"])
def upload_file():
    """uploads single file to minio bucket"""
    try:
        if "file" in request.files:
            file_obj = request.files["file"]
            size = os.fstat(file_obj.fileno()).st_size
            random_id = uuid.uuid4()
            ext = file_obj.filename.split(".")[-1]
            object_name = f"{random_id}.{ext}"
            minio_client.put_object(
                bucket_name="images", object_name=object_name, data=file_obj, length=size)
            return jsonify({"code": 201,
                            "data": {"object_name": object_name}})
    except S3Error:
        return jsonify({"code": 500,
                        "message": "There was an error with uploading object to bucket"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5105, debug=True)
