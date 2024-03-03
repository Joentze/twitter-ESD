from transformers import pipeline
import requests

API_URL = "https://api-inference.huggingface.co/models/michellejieli/NSFW_text_classifier"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    
    data=response.json()[0]
    sfw = data[0]
    nsfw = data[1]
    
    if sfw['score']>nsfw['score']:
        return True
    else:
        return False


	
# output = query({
# 	"inputs": "I like you. I love you",
# })

# print(output)
