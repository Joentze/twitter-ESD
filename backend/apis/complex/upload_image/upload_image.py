from io import BufferedReader

from flask import Flask, request, jsonify
from flask_cors import CORS
from requests import post
from requests_toolbelt.multipart.encoder import MultipartEncoder
app = Flask(__name__)
CORS(app)

ASSET_API_ENDPOINT = "http://localhost:5105"
IMAGE_API_ENDPOINT = "http://localhost:5110"


@app.route('/upload', methods=['POST'])
def upload_image():
    """uploads image to minio bucket and updates sql table"""
    try:
        if "file" in request.files:
            print(request.headers)
            file = request.files['file']
            data = MultipartEncoder(
                fields={"file": (file.filename, file.stream, file.mimetype)})
            headers = {}
            for name, header in request.headers:
                headers[name] = header
            asset_response = post(headers={**headers, "Content-Type": data.content_type, "Content-Length": str(data.len)}, url=f"{ASSET_API_ENDPOINT}/upload",
                                  data=data, timeout=5000)
            object_id = asset_response.json()["data"]["object_name"]
            print(object_id)
            uploader_uid = request.form["uploader_uid"]
            print(uploader_uid)

            image_response = post(headers=dict(request.headers),
                                  url=f"{IMAGE_API_ENDPOINT}/image/{object_id}", json={"uploader_uid": uploader_uid}, timeout=5000)
            print(image_response)
            return jsonify({"code": 201, "data": image_response.json()["data"]}), 201

    except Exception as e:
        print(e)
        return jsonify({"code": 500, "message": "There was a server error!"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5106, debug=True)
