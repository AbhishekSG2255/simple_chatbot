from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pathlib import Path
import pickle

# Optional scikit-learn imports
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    _have_sklearn = True
except Exception:
    _have_sklearn = False

BASE = Path(__file__).resolve().parent
FAQ_JSON = BASE / 'faq.json'
FAQ_INDEX = BASE / 'faq_index.pkl'

faq_questions = []
faq_answers = []
vectorizer = None
faq_vectors = None

# Load persisted index if available
if FAQ_INDEX.exists() and _have_sklearn:
    try:
        with open(FAQ_INDEX, 'rb') as f:
            data = pickle.load(f)
            vectorizer = data.get('vectorizer')
            faq_vectors = data.get('vectors')
            faqs = data.get('faqs', [])
            faq_questions = [q['question'] for q in faqs]
            faq_answers = [q['answer'] for q in faqs]
    except Exception:
        # ignore and fallback to JSON
        pass

# If no persisted index, try to build from faq.json
if (not faq_questions) and FAQ_JSON.exists():
    try:
        with open(FAQ_JSON, 'r', encoding='utf-8') as f:
            faqs = json.load(f)
            faq_questions = [q['question'] for q in faqs]
            faq_answers = [q['answer'] for q in faqs]
            if _have_sklearn:
                vectorizer = TfidfVectorizer()
                faq_vectors = vectorizer.fit_transform(faq_questions)
    except Exception:
        faq_questions = []
        faq_answers = []


def get_faq_answer(user_input):
    # If TF-IDF is available, use similarity; otherwise fallback to simple matching
    if _have_sklearn and vectorizer is not None and faq_vectors is not None:
        user_vec = vectorizer.transform([user_input])
        similarity = cosine_similarity(user_vec, faq_vectors)
        idx = similarity.argmax()
        if similarity[0, idx] > 0.3:
            return faq_answers[idx]
        return "Sorry, I don't understand. Can you rephrase?"

    # Fallback: substring/keyword matching
    text = user_input.lower()
    for q, a in zip(faq_questions, faq_answers):
        q_lower = q.lower()
        if q_lower in text:
            return a
        # match if several keywords overlap
        keywords = [w for w in q_lower.split() if len(w) > 3]
        if sum(1 for w in keywords if w in text) >= 2:
            return a
    return "Sorry, I don't understand. Can you rephrase?"


def rule_based_response(user_input):
    text = user_input.lower()
    if "hello" in text or "hi" in text:
        return "Hi! How can I help you?"
    if "bye" in text:
        return "Goodbye!"
    return None


@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"reply": "Invalid JSON"}, status=400)
        user_input = data.get("message", "")

        # Rule-based quick replies
        response = rule_based_response(user_input)
        if response:
            return JsonResponse({"reply": response})

        # Retrieval
        reply = get_faq_answer(user_input)
        return JsonResponse({"reply": reply})

    return JsonResponse({"reply": "Invalid request"}, status=400)


def index(request):
    return render(request, "chatbot/index.html")
