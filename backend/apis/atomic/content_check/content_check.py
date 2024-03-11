from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)

# Configure logging
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


# Configure logging
API_URL = "https://api-inference.huggingface.co/models/michellejieli/NSFW_text_classifier"
headers = {"Authorization": "Bearer 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"}

@app.route('/post/validate/')
def content_check():
    req_body = request.json
    app.logger.info(req_body)
    response = requests.post(API_URL, headers=headers, json=req_body)
    
    data=response.json()[0]
    sfw = data[0]
    nsfw = data[1]
    
    if sfw['score']<0.3:
        return jsonify(
            {
                "code":200,
                "message": "Content is safe!"
            }
        )
    else:
        return jsonify(
            {
                "code":500,
                "message": "Content violates guidelines!", 
            }
        )


if __name__ == "__main__":
    app.logger.info("Transformer API is running at port 5108")
    app.run(host='0.0.0.0', port=5108, debug=True)




# output = content_check({
# 	"inputs": "I like you. I love you",
# })

# print(output)