# chatbot/management/commands/train_chatbot.py
import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

class Command(BaseCommand):
    help = "Train a simple intent classifier for the chatbot"

    def handle(self, *args, **options):
        # Simple training dataset (expand this for better results)
        training_data = {
            "greet": [
                "hi", "hello", "hey", "good morning", "good evening"
            ],
            "appointment": [
                "book appointment", "i want to book an appointment",
                "schedule appointment", "can i book a doctor"
            ],
            "doctor": [
                "doctor", "doctors", "available doctors",
                "which doctors are available", "do you have a cardiologist",
                "we need a neurologist", "pediatrician", "orthopaedic doctor",
                "list of doctors", "who are your doctors"
            ],
            "location": [
                "where is the hospital", "hospital location", "address",
                "addres", "adress", "location", "how to reach",
                "directions to hospital"
            ],

            "timings": [
                "opening hours", "what time are you open", "visiting hours",
                "when are doctors available"
            ],
            "emergency": [
                "emergency number", "in case of emergency", "ambulance"
            ],
            "surgery_instructions": [
                "pre surgery instructions", "how to prepare for surgery",
                "post surgery care", "after surgery what to do"
            ],
            "billing": [
                "billing", "how to pay my bill", "insurance", "charges"
            ],
            "thanks": [
                "thanks", "thank you", "thank you so much"
            ]
        }

        responses = {
            "greet": "Hello! I'm the hospital assistant. How can I help you today?",
            "appointment": "You can book appointments online or call +1 (123) 456-7890 (9AM-5PM, Mon-Sat). Would you like help scheduling?",
            "doctor": "We have specialists in Cardiology, Neurology, Orthopaedics, Oncology and more. Which specialty do you need?",
            "timings": "Outpatient services: 9:00 AM - 5:00 PM (Mon-Sat). Emergency is 24/7.",
            "location": "Our address: 123 Healthcare Avenue, Metropolis. Need directions?",
            "emergency": "If this is an emergency, call +1 (123) 999-0000 immediately or go to the nearest emergency department.",
            "surgery_instructions": "Pre-op: Do not eat/drink 8 hours before surgery. Bring ID and medication list. Post-op: follow surgeon's instructions and attend follow-ups. For specifics, tell me the surgery type.",
            "billing": "For billing queries call +1 (123) 456-7891 or visit the billing desk. We accept insurance and card.",
            "thanks": "You're welcome! Anything else I can help with?",
            "fallback": "Sorry, I didn't understand. Could you rephrase or ask about appointment, doctors, timings, or emergency?"
        }

        X = []
        y = []
        for intent, phrases in training_data.items():
            for p in phrases:
                X.append(p)
                y.append(intent)

        vectorizer = TfidfVectorizer(ngram_range=(1,2))
        X_vec = vectorizer.fit_transform(X)
        clf = MultinomialNB()
        clf.fit(X_vec, y)

        models_dir = os.path.join(settings.BASE_DIR, "chatbot", "models")
        os.makedirs(models_dir, exist_ok=True)
        joblib.dump(vectorizer, os.path.join(models_dir, "vectorizer.joblib"))
        joblib.dump(clf, os.path.join(models_dir, "classifier.joblib"))

        with open(os.path.join(models_dir, "responses.json"), "w") as f:
            json.dump(responses, f, indent=2)

        self.stdout.write(self.style.SUCCESS("Trained model saved to chatbot/models/"))
