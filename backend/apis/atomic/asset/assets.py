"""uploads files to minio bucket"""
import os
import io
import uuid
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
    MINIO_ENDPOINT = "localhost:9000"
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
            return {"object_name": object_name}, 201
    except S3Error:
        return 500


@app.route("/src", methods=["GET"])
def get_url():
    """gets the presigned url from the object name"""
    object_name = request.args.get("name")
    if object_name:
        response = minio_client.presigned_get_object(
            bucket_name="images", object_name=object_name)
        return {"url": response}, 200
    else:
        return 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5105, debug=True)
