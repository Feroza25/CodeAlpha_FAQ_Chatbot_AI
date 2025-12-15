from flask import Flask, render_template, request, jsonify
from faqs import faqs
import nltk
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

app = Flask(__name__)

# Preprocess text
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

questions = [preprocess(faq["question"]) for faq in faqs]
answers = [faq["answer"] for faq in faqs]

vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    processed_input = preprocess(user_input)

    user_vector = vectorizer.transform([processed_input])
    similarities = cosine_similarity(user_vector, question_vectors)

    best_match = similarities.argmax()
    confidence = similarities[0][best_match]

    if confidence < 0.2:
        return jsonify({"reply": "Sorry, I couldn't understand that. Please try asking something else."})

    return jsonify({"reply": answers[best_match]})

if __name__ == '__main__':
    app.run(debug=True)
