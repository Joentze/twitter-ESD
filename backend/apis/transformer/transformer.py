from transformers import pipeline
import requests


API_URL = "https://api-inference.huggingface.co/models/michellejieli/NSFW_text_classifier"
headers = {"Authorization": f"Bearer {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}"}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
data = query("Can you please let us know more details about your ")



classifier = pipeline("sentiment-analysis", model="michellejieli/NSFW_text_classification")
classifier("I see you’ve set aside this special time to humiliate yourself in public.")

