import os
import joblib
import json
from django.conf import settings

# Load models at startup
models_dir = os.path.join(settings.BASE_DIR, "chatbot", "models")
vectorizer = joblib.load(os.path.join(models_dir, "vectorizer.joblib"))
clf = joblib.load(os.path.join(models_dir, "classifier.joblib"))

with open(os.path.join(models_dir, "responses.json")) as f:
    responses = json.load(f)


def get_chatbot_response(user_message: str) -> str:
    if not user_message.strip():
        return responses.get("fallback")

    X = vectorizer.transform([user_message])
    probs = clf.predict_proba(X)[0]
    intent = clf.classes_[probs.argmax()]
    confidence = probs.max()

    if confidence < 0.5:  # threshold (tune this)
        return responses["fallback"]

    return responses.get(intent, responses["fallback"])

