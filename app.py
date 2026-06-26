import joblib
import re
import string

# Load model and vectorizer
model = joblib.load("spam_classifier.pkl")
vectorizer = joblib.load("count_vectorizer.pkl")


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


while True:

    message = input("\nEnter a message: ")

    cleaned = clean_text(message)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    if prediction == 1:
        print("🚨 SPAM MESSAGE")
    else:
        print("✅ HAM (Normal Message)")